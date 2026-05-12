import os
import re
import yaml
import subprocess
from pathlib import Path

# --- GLOBAL EXCLUSION LIST (matched by folder NAME anywhere in the tree) ---
EXCLUDE_NAMES = {
    "node_modules", "venv", ".venv", "vendor", "vendors", "bin", "obj",
    "target", ".git", "dist", "build", ".next", ".aws", "pkg",
    "bower_components", "jspm_packages", ".yarn", ".pnp",
    "third_party", "thirdparty", "__pycache__", ".tox", ".eggs",
}

# Folder names that are strong hints of vendored/bundled deps when combined
# with other signals (e.g. they're nested under public/assets/static).
# These names rarely contain first-party source code worth linting.
DEPENDENCY_NAME_HINTS = {
    "lib", "libs", "js", "css", "scripts", "static", "assets",
    "plugins", "images", "img", "fonts", "media", "uploads",
    "external", "extern", "generated", "gen", "out",
}

# Parent path segments that, when appearing in the path, suggest a public
# asset tree rather than first-party source code
ASSET_PARENT_HINTS = {"public", "assets", "static", "resources", "web", "wwwroot"}

# Folders whose contents are almost always served-as-is static assets.
# When their direct children are predominantly dep-hint folders, the whole
# folder gets excluded (catches the parent of js/css/images in one shot).
WEB_ROOT_NAMES = {"public", "wwwroot"}
WEB_ROOT_DEP_RATIO = 0.6   # ≥ 60 % of subdirs are dep-hints → exclude parent

# Signals that a directory contains bundled/vendored output, not source
MIN_MINIFIED_FILE_COUNT = 3   # ≥ N files with .min.js / .min.css → exclude
MIN_MAP_FILE_COUNT = 3        # ≥ N .map files alongside JS/CSS → exclude
MINIFIED_RATIO_THRESHOLD = 0.7  # ≥ 70 % of JS/CSS files are minified → exclude

# How deep to recurse when scanning for dependency directories
MAX_WALK_DEPTH = 8

# --- LANGUAGE DETECTION ---
EXT_MAP = {
    ".py": "PYTHON", ".js": "JAVASCRIPT", ".ts": "TYPESCRIPT",
    ".jsx": "JAVASCRIPT", ".tsx": "TYPESCRIPT", ".go": "GO",
    ".rs": "RUST", ".java": "JAVA", ".cs": "CSHARP",
    ".md": "MARKDOWN", ".json": "JSON", ".yml": "YAML",
    ".yaml": "YAML", ".sql": "SQL", ".html": "HTML",
    ".sh": "BASH", ".bash": "BASH", ".zsh": "BASH",
    ".tf": "TERRAFORM", ".hcl": "TERRAFORM",
    ".php": "PHP", ".rb": "RUBY", ".kt": "KOTLIN", ".swift": "SWIFT",
    ".cpp": "CPP", ".cc": "CPP", ".cxx": "CPP", ".c": "C",
}


# ---------------------------------------------------------------------------
# Dependency-folder detection
# ---------------------------------------------------------------------------

def _sample_files(path: Path) -> list[Path]:
    """Return direct-child files of a directory, ignoring permission errors."""
    try:
        return [c for c in path.iterdir() if c.is_file()]
    except PermissionError:
        return []


def _is_minified(filename: str) -> bool:
    name = filename.lower()
    return bool(re.search(r'\.min\.(js|css|mjs)$', name))


def _has_asset_parent(rel_path: Path) -> bool:
    """True if any parent segment of rel_path is in ASSET_PARENT_HINTS."""
    return any(part.lower() in ASSET_PARENT_HINTS for part in rel_path.parts[:-1])


def _child_dirs(path: Path) -> list[Path]:
    """Return direct-child directories, ignoring permission errors."""
    try:
        return [c for c in path.iterdir() if c.is_dir()]
    except PermissionError:
        return []


def _looks_like_web_root(folder: Path) -> bool:
    """
    True if the folder is named like a web root (public/, wwwroot/) AND most
    of its direct child directories look like asset folders. Catches the
    parent of js/css/images/fonts in a single exclusion.
    """
    if folder.name.lower() not in WEB_ROOT_NAMES:
        return False
    subdirs = _child_dirs(folder)
    if not subdirs:
        return False
    dep_like = sum(1 for d in subdirs if d.name.lower() in DEPENDENCY_NAME_HINTS)
    return dep_like / len(subdirs) >= WEB_ROOT_DEP_RATIO


def _score_as_dependency(folder: Path, rel_path: Path) -> bool:
    """
    Return True if the folder looks like it contains third-party/bundled code
    rather than first-party source that should be linted.

    Order matters: path/name-based rules run BEFORE file-content rules so that
    folders containing only subdirectories (e.g. public/js/lib/...) are still
    caught — a previous version bailed out early when a folder had no direct
    files, which let nested asset trees slip through.
    """
    name = folder.name.lower()

    # 1. Hard-coded exclusion by name (e.g. node_modules, vendor, .git)
    if name in EXCLUDE_NAMES:
        return True

    # 2. Path-based: dep-hint name nested under an asset-parent path.
    #    Example: resources/web/public/js  →  "js" + parent "public" → exclude
    if name in DEPENDENCY_NAME_HINTS and _has_asset_parent(rel_path):
        return True

    # 3. Path-based: a web-root folder (public/, wwwroot/) whose children are
    #    mostly asset-named folders. Excludes the whole subtree in one go.
    if _looks_like_web_root(folder):
        return True

    # 4. File-content heuristics for everything else
    files = _sample_files(folder)
    if not files:
        return False

    js_css_files = [f for f in files if f.suffix.lower() in (".js", ".css", ".mjs")]
    minified = [f for f in files if _is_minified(f.name)]
    map_files = [f for f in files if f.suffix.lower() == ".map"]

    if len(minified) >= MIN_MINIFIED_FILE_COUNT:
        return True
    if js_css_files and len(minified) / len(js_css_files) >= MINIFIED_RATIO_THRESHOLD:
        return True
    if len(map_files) >= MIN_MAP_FILE_COUNT and js_css_files:
        return True

    return False


def walk_for_exclusions(repo_root: Path, max_depth: int = MAX_WALK_DEPTH):
    """
    Recursively walk the repo and return:
      - name_exclusions : set of bare directory names safe to exclude globally
      - path_exclusions : list of relative posix paths that need regex exclusion
    """
    name_exclusions: set[str] = set()
    path_exclusions: list[str] = []

    def _walk(current: Path, depth: int):
        if depth > max_depth:
            return
        try:
            children = [c for c in current.iterdir() if c.is_dir()]
        except PermissionError:
            return

        for child in children:
            rel = child.relative_to(repo_root)
            rel_posix = rel.as_posix()

            if _score_as_dependency(child, rel):
                # If the bare name is unambiguously a dep folder, use the
                # cheaper name-level exclusion; otherwise pin the full path.
                if child.name.lower() in EXCLUDE_NAMES:
                    name_exclusions.add(child.name)
                else:
                    path_exclusions.append(rel_posix)
                # Don't recurse into excluded subtrees
                continue

            _walk(child, depth + 1)

    _walk(repo_root, 1)
    return sorted(name_exclusions), sorted(path_exclusions)


# ---------------------------------------------------------------------------
# Language detection (walks the tree, skips known dep folders)
# ---------------------------------------------------------------------------

def detect_languages(repo_root: Path, excluded_names: set[str],
                     excluded_paths: list[str]) -> set[str]:
    """Return a set of MegaLinter linter-group names for detected languages."""
    excluded_path_patterns = [re.compile(rf'^{re.escape(p)}(/|$)') for p in excluded_paths]
    groups: set[str] = {"REPOSITORY", "COPYPASTE", "CREDENTIALS", "GIT"}

    for dirpath, dirnames, filenames in os.walk(repo_root):
        current = Path(dirpath)
        rel = current.relative_to(repo_root).as_posix()

        # Prune excluded directories in-place so os.walk won't descend
        dirnames[:] = [
            d for d in dirnames
            if d.lower() not in excluded_names
            and not any(p.match(f"{rel}/{d}".lstrip("./")) for p in excluded_path_patterns)
        ]

        for fname in filenames:
            fpath = Path(fname)
            if fpath.name.lower() == "dockerfile":
                groups.add("DOCKERFILE")
            if fpath.suffix in EXT_MAP:
                groups.add(EXT_MAP[fpath.suffix])

    return groups


# ---------------------------------------------------------------------------
# Grafana stack availability check
# ---------------------------------------------------------------------------

LOKI_CONTAINER = "loki"
METRICS_CONTAINER = "victoriametrics"
LOKI_URL = "http://loki:3100/loki/api/v1/push"
METRICS_URL = "http://victoriametrics:8428/write"


def _containers_on_network(network: str) -> set[str]:
    """
    Return the set of container names currently running on *network*.
    Returns an empty set if Docker is unreachable or the network doesn't exist.
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"network={network}", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=10,
        )
        return {name.strip().lower() for name in result.stdout.splitlines() if name.strip()}
    except Exception:
        return set()


def _check_reporter_services() -> tuple[bool, bool]:
    """
    Check whether the Loki and VictoriaMetrics containers are running on
    megalinter-net.  Returns (loki_ok, metrics_ok).
    """
    running = _containers_on_network("megalinter-net")
    loki_ok = LOKI_CONTAINER in running
    metrics_ok = METRICS_CONTAINER in running
    return loki_ok, metrics_ok


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_megalinter():
    repo_root = Path.cwd()
    project_name = repo_root.name

    print(f"Configuring MegaLinter for '{project_name}'...")
    print("Scanning for dependency/vendor folders to exclude...")

    name_exclusions, path_exclusions = walk_for_exclusions(repo_root)

    if name_exclusions:
        print(f"  Excluding by name : {sorted(name_exclusions)}")
    if path_exclusions:
        print(f"  Excluding by path : {path_exclusions}")

    enabled_groups = detect_languages(
        repo_root,
        excluded_names={n.lower() for n in name_exclusions},
        excluded_paths=path_exclusions,
    )
    print(f"  Detected groups   : {sorted(enabled_groups)}")

    # Build FILTER_REGEX_EXCLUDE from path-based exclusions so MegaLinter
    # skips files inside nested dep folders that can't be expressed as bare names.
    # Anchor each path at a "/" or string-start boundary so e.g. "public/js"
    # matches both "/tmp/lint/public/js/..." and "public/js/..." reliably.
    filter_regex = None
    if path_exclusions:
        alternation = "|".join(re.escape(p) for p in path_exclusions)
        filter_regex = f"(^|/)({alternation})(/|$)"

    config: dict = {
        "FLAVOR": "cupcake",
        "VALIDATE_ALL_CODEBASE": False,
        "SHOW_ELAPSED_TIME": True,
        "PARALLEL": True,
        "IGNORE_GITIGNORED_FILES": True,
        "EXCLUDED_DIRECTORIES": sorted(name_exclusions),
        "ENABLE": sorted(list(enabled_groups)),
    }
    if filter_regex:
        config["FILTER_REGEX_EXCLUDE"] = filter_regex

    config_path = repo_root / ".mega-linter.yml"
    with open(config_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"Config written to: {config_path}")

    # Ensure the shared Docker network exists
    subprocess.run(
        ["docker", "network", "create", "megalinter-net"],
        capture_output=True,
    )

    # Check whether the Grafana stack is reachable before enabling the API
    # reporter.  If either service is down the scan still runs — results are
    # always available in the console output and MegaLinter's log files.
    print("Checking Grafana stack availability...")
    loki_ok, metrics_ok = _check_reporter_services()
    reporting_enabled = loki_ok and metrics_ok

    if reporting_enabled:
        print("  Loki and VictoriaMetrics are reachable — API reporting enabled.")
    else:
        missing = []
        if not loki_ok:
            missing.append("Loki")
        if not metrics_ok:
            missing.append("VictoriaMetrics")
        print(
            f"  Warning: {', '.join(missing)} not found on megalinter-net. "
            "API reporting disabled.\n"
            "  Results will still be available in the console output and "
            "MegaLinter log files."
        )

    docker_cmd = [
        "docker", "run", "--rm",
        "--network", "megalinter-net",
        "-v", "/var/run/docker.sock:/var/run/docker.sock:rw",
        "-v", f"{repo_root}:/tmp/lint:rw",
        "-e", f"PROJECT_NAME={project_name}",
        "-e", f"GITHUB_REPOSITORY={project_name}",
        "oxsecurity/megalinter-cupcake:v9",
    ]

    if reporting_enabled:
        docker_cmd += [
            "-e", "API_REPORTER=true",
            "-e", f"API_REPORTER_URL={LOKI_URL}",
            "-e", f"API_REPORTER_METRICS_URL={METRICS_URL}",
        ]

    print("Running Docker scan...")
    subprocess.run(docker_cmd)


if __name__ == "__main__":
    run_megalinter()
