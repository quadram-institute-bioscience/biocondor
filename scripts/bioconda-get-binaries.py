#!/usr/bin/env python3
"""
Fetch every Bioconda package listed in a `versions/` directory, starting
with the **latest version first** and proceeding to older versions.
Progress is recorded, so the script can be re-run safely (resumable).

Now continues processing other packages/versions even when individual ones fail.

Usage examples
--------------
# default layout (versions/*.txt â†’ binaries/)
python fetch_bioconda.py

# custom locations and dry-run
python fetch_bioconda.py -v my_lists/ -o out/ --dry-run
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Set, Dict

try:                           # proper version comparison
    from packaging.version import Version, InvalidVersion
except ModuleNotFoundError:    # make the dependency explicit
    sys.exit(
        "Missing dependency 'packaging'. Install with:\n"
        "   pip install packaging"
    )


# ------------------------------------------------------------------ helpers
def _version_key(v: str):
    """Key function that allows PEP-440 comparison but tolerates odd tags."""
    try:
        return (0, Version(v))  # (priority, version_obj) tuple
    except InvalidVersion:
        # fall back to plain string sort for non-standard tags (e.g. 'r123')
        return (1, v)  # lower priority for non-standard versions


def read_versions(path: Path) -> List[str]:
    """Return the non-empty, stripped lines inside *path*."""
    with path.open(encoding="utf-8") as fh:
        return [ln.strip() for ln in fh if ln.strip()]


def get_latest_version(versions: Iterable[str]) -> str | None:
    """
    Identify the latest version in *versions*.

    Uses `packaging.version.Version` when possible, otherwise a fallback
    lexical ordering.
    """
    versions = list(versions)
    return max(versions, key=_version_key) if versions else None


# ------------------------------ resumability bookkeeping (simple & robust)
def _load_log(log_path: Path) -> Set[str]:
    """Return a set { 'package=version', â€¦ } that have already completed."""
    if not log_path.exists():
        return set()
    with log_path.open(encoding="utf-8") as fh:
        return {ln.strip() for ln in fh if ln.strip()}


def _append_log(log_path: Path, entry: str) -> None:
    """Record a finished 'package=version' pair."""
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(entry + "\n")


def _load_failed_log(log_path: Path) -> Set[str]:
    """Return a set { 'package=version', â€¦ } that have failed."""
    if not log_path.exists():
        return set()
    with log_path.open(encoding="utf-8") as fh:
        return {ln.strip() for ln in fh if ln.strip()}


def _append_failed_log(log_path: Path, entry: str) -> None:
    """Record a failed 'package=version' pair."""
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(entry + "\n")


# ------------------------------------------------------------------ main
def main() -> None:
    p = argparse.ArgumentParser(
        prog="fetch_bioconda.py",
        description=(
            "Download bioconda-binaries, beginning with the NEWEST version "
            "of every package and continuing to older ones. "
            "Progress is saved, so interrupted runs pick up where they left off. "
            "Continues processing other packages even when individual ones fail."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "-v",
        "--versions-dir",
        default="versions",
        metavar="DIR",
        help="Directory containing <package>.txt files (one version per line)",
    )
    p.add_argument(
        "-o",
        "--output-dir",
        default="binaries",
        metavar="DIR",
        help="Destination directory passed to bioconda-binaries -o",
    )
    p.add_argument(
        "--resume-file",
        default=".processed.log",
        metavar="FILE",
        help="File that stores finished 'package=version' entries",
    )
    p.add_argument(
        "--failed-file",
        default=".failed.log",
        metavar="FILE",
        help="File that stores failed 'package=version' entries",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without executing bioconda-binaries",
    )
    p.add_argument(
        "--continue-on-error",
        action="store_true",
        default=True,
        help="Continue processing other packages/versions when one fails (default: True)",
    )
    p.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop processing when any package fails (overrides --continue-on-error)",
    )

    args = p.parse_args()

    # Determine error handling behavior
    continue_on_error = args.continue_on_error and not args.stop_on_error

    versions_dir = Path(args.versions_dir).expanduser().resolve()
    out_dir = Path(args.output_dir).expanduser().resolve()
    log_path = Path(args.resume_file).expanduser().resolve()
    failed_path = Path(args.failed_file).expanduser().resolve()

    # create output directory if needed
    out_dir.mkdir(parents=True, exist_ok=True)

    processed = _load_log(log_path)
    failed = _load_failed_log(failed_path)

    # Statistics tracking
    stats = {
        'total_packages': 0,
        'total_versions': 0,
        'successful': 0,
        'failed': 0,
        'skipped_processed': 0,
        'skipped_failed': 0
    }

    package_files = sorted(versions_dir.glob("*.txt"))
    stats['total_packages'] = len(package_files)

    # First, collect all packages and their versions
    packages_data = {}
    for vf in package_files:
        package = vf.stem                       # 3d-dna.txt  -> 3d-dna
        all_versions = read_versions(vf)
        if not all_versions:
            print(f"[WARN] No versions for {package!r}; skipping", file=sys.stderr)
            continue

        stats['total_versions'] += len(all_versions)

        # newest → oldest
        all_versions.sort(key=_version_key, reverse=True)
        packages_data[package] = all_versions

    # Track which packages have at least one successful version
    packages_with_success = set()

    def process_version(package: str, ver: str) -> bool:
        """Process a single package version. Returns True if successful."""
        tag = f"{package}={ver}"

        if tag in processed:
            print(f"  ✅ already done {tag}")
            stats['skipped_processed'] += 1
            return True

        if tag in failed:
            print(f"  ❌ previously failed {tag} (skipping)")
            stats['skipped_failed'] += 1
            return False

        cmd = [
            "bioconda-binaries",
            "--flexible",
            "-o",
            str(out_dir),
            "--verbose",
            tag,
        ]
        print("  ➡️", " ".join(cmd))

        if args.dry_run:
            return True  # simulate success

        result = subprocess.run(cmd)
        if result.returncode:
            print(f"  ❌ failed ({result.returncode}): {tag}", file=sys.stderr)
            _append_failed_log(failed_path, tag)
            failed.add(tag)
            stats['failed'] += 1

            if not continue_on_error:
                print(f"Stopping due to failure with {tag}", file=sys.stderr)
                sys.exit(result.returncode)
            else:
                print(f"  ➡️ continuing with next version/package...")
                return False

        _append_log(log_path, tag)
        processed.add(tag)
        stats['successful'] += 1
        return True

    # PHASE 1: Process latest version of each package
    print("\n" + "="*60)
    print("PHASE 1: Processing latest version of each package")
    print("="*60)
    
    for package, all_versions in packages_data.items():
        latest = all_versions[0]  # already sorted newest first
        print(f"\n{package}: processing latest = {latest}")
        
        if process_version(package, latest):
            packages_with_success.add(package)

    # PHASE 2: Process older versions for packages that have at least one success
    print("\n" + "="*60)
    print("PHASE 2: Processing older versions")
    print("="*60)
    
    for package, all_versions in packages_data.items():
        if package not in packages_with_success:
            print(f"\n{package}: skipping older versions (no successful latest version)")
            continue
            
        if len(all_versions) <= 1:
            continue  # no older versions
            
        print(f"\n{package}: processing {len(all_versions)-1} older versions")
        
        for ver in all_versions[1:]:  # skip first (latest) version
            process_version(package, ver)

    # Print final statistics
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    print(f"Total packages: {stats['total_packages']}")
    print(f"Total versions: {stats['total_versions']}")
    print(f"Successfully processed: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Skipped (already processed): {stats['skipped_processed']}")
    print(f"Skipped (previously failed): {stats['skipped_failed']}")

    if stats['failed'] > 0:
        print(f"\nFailed entries logged to: {failed_path}")
        print("You can review failed packages and potentially retry them later.")

    if stats['successful'] > 0:
        print(f"\nSuccessful entries logged to: {log_path}")

    print("\nAll requested packages processed.")

    # Exit with appropriate code
    if stats['failed'] > 0 and not continue_on_error:
        sys.exit(1)


# ------------------------------------------------------------------ entry-point
if __name__ == "__main__":
    main()
