"""
Ketchup Classify — Standalone commit classifier script.

Wraps the CLI engine's commit_classifier and feature_discovery modules
for use as a standalone skill or via AI agents.

Usage:
    python classify.py --repo /path/to/repo --days 30 --features --json
"""

import os
import sys
import json
import argparse
import subprocess
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# Add parent paths so we can import from ketchup-cli engine if installed
CLI_ENGINE_PATH = os.environ.get("KETCHUP_ENGINE_PATH")
if CLI_ENGINE_PATH:
    sys.path.insert(0, CLI_ENGINE_PATH)


# ─── Git Extraction ──────────────────────────────────────────────────────────

def extract_commits(repo_path: str, days: int = 30) -> List[Dict[str, Any]]:
    """Extract commits from a git repo using git log."""
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    result = subprocess.run(
        [
            "git", "log",
            f"--since={since_date}",
            "--format=%H|%an|%aI|%s",
            "--no-merges",
        ],
        capture_output=True,
        text=True,
        cwd=repo_path,
    )

    if result.returncode != 0:
        print(f"❌ git log failed: {result.stderr}", file=sys.stderr)
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "sha": parts[0],
                "author": parts[1],
                "date": parts[2],
                "message": parts[3],
            })

    return commits


def extract_merge_prs(repo_path: str, days: int = 30) -> List[Dict[str, Any]]:
    """Extract PR metadata from merge commits."""
    import re

    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    result = subprocess.run(
        [
            "git", "log",
            f"--since={since_date}",
            "--merges",
            "--format=%H|%an|%aI|%s",
        ],
        capture_output=True,
        text=True,
        cwd=repo_path,
    )

    if result.returncode != 0:
        return []

    pr_pattern = re.compile(
        r"Merge pull request #(\d+) from (\S+)"
    )
    squash_pattern = re.compile(
        r"^(.+?)\s*\(#(\d+)\)$"
    )

    prs = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue

        sha, author, date, message = parts

        # Try "Merge pull request #N from user/branch" format
        match = pr_pattern.match(message)
        if match:
            prs.append({
                "number": int(match.group(1)),
                "branch": match.group(2),
                "title": message,
                "author": author,
                "merged_at": date,
                "sha": sha,
            })
            continue

        # Try "Title (#N)" squash merge format
        match = squash_pattern.match(message)
        if match:
            prs.append({
                "number": int(match.group(2)),
                "branch": None,
                "title": match.group(1),
                "author": author,
                "merged_at": date,
                "sha": sha,
            })

    return prs


# ─── Classification Engine ───────────────────────────────────────────────────

def classify_commits_standalone(commits: List[Dict]) -> List[Dict]:
    """
    Classify commits using the engine if available, otherwise fallback.
    """
    try:
        from services.commit_classifier import classify_commits
        results = classify_commits(commits)
        return [c.to_dict() for c in results]
    except ImportError:
        # Fallback: inline rule-based classification
        return _fallback_classify(commits)


def discover_features_standalone(classified: List[Dict]) -> List[Dict]:
    """Discover features using engine if available, otherwise fallback."""
    try:
        from services.feature_discovery import discover_features
        results = discover_features(classified)
        return [f.to_dict() for f in results]
    except ImportError:
        return _fallback_discover(classified)


# ─── Fallback Classifiers (no engine dependency) ─────────────────────────────

import re

_CC_REGEX = re.compile(
    r"^(?P<type>feat|fix|refactor|chore|docs|test|style|ci|build|perf)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?"
    r":\s*(?P<desc>.+)",
    re.IGNORECASE,
)

_TYPE_MAP = {"feat": "feature", "improvement": "feature"}

_KEYWORD_MAP = [
    # Order matters: more specific patterns first to avoid false positives
    (["doc", "readme", "typo", "comment"], "docs"),
    (["test", "spec", "coverage"], "test"),
    (["merge ", "chore", "bump", "release", "update dep"], "chore"),
    (["fix ", "bug ", "patch ", "resolve ", "hotfix"], "fix"),
    (["refactor", "restructure", "cleanup", "simplif"], "refactor"),
    (["add ", "implement", "introduce", "new ", "create "], "feature"),
]


def _fallback_classify(commits: List[Dict]) -> List[Dict]:
    """Simple rule-based classification without engine imports."""
    results = []
    for c in commits:
        msg = c.get("message", "")
        first_line = msg.split("\n")[0].strip()
        lower = first_line.lower()

        # Try conventional commits
        match = _CC_REGEX.match(first_line)
        if match:
            raw_type = match.group("type").lower()
            results.append({
                "sha": c["sha"],
                "type": _TYPE_MAP.get(raw_type, raw_type),
                "scope": match.group("scope"),
                "description": match.group("desc"),
                "risk_level": "low",
                "is_breaking": bool(match.group("breaking")),
                "confidence": 0.95,
                "original_message": msg,
            })
            continue

        # Keyword fallback
        classified = False
        for keywords, ctype in _KEYWORD_MAP:
            if any(kw in lower for kw in keywords):
                results.append({
                    "sha": c["sha"],
                    "type": ctype,
                    "scope": None,
                    "description": first_line,
                    "risk_level": "low",
                    "is_breaking": False,
                    "confidence": 0.7,
                    "original_message": msg,
                })
                classified = True
                break

        if not classified:
            results.append({
                "sha": c["sha"],
                "type": "chore",
                "scope": None,
                "description": first_line,
                "risk_level": "low",
                "is_breaking": False,
                "confidence": 0.4,
                "original_message": msg,
            })

    return results


def _fallback_discover(classified: List[Dict]) -> List[Dict]:
    """Simple scope-based feature grouping without engine imports."""
    from collections import defaultdict

    features_by_scope: Dict[str, List[Dict]] = defaultdict(list)

    for c in classified:
        if c.get("type") not in ("feature", "fix", "perf"):
            continue
        scope = c.get("scope") or "general"
        features_by_scope[scope].append(c)

    features = []
    for scope, commits in features_by_scope.items():
        descs = [c.get("description", "")[:100] for c in commits[:5]]
        features.append({
            "name": scope.replace("-", " ").replace("_", " ").title(),
            "description": "; ".join(descs),
            "type": "feature",
            "commit_shas": [c["sha"] for c in commits],
            "commit_count": len(commits),
            "first_date": commits[-1].get("date") if commits else None,
            "last_date": commits[0].get("date") if commits else None,
            "significance": min(1.0, len(commits) * 0.15 + 0.1),
        })

    return sorted(features, key=lambda f: f["significance"], reverse=True)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🏷️ Ketchup Classify — Commit Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python classify.py --repo . --days 30
  python classify.py --repo . --features --json
  python classify.py --repo . --prs --output results.json
        """,
    )
    parser.add_argument("--repo", default=".", help="Path to git repository")
    parser.add_argument("--days", type=int, default=30, help="Days of history")
    parser.add_argument("--features", action="store_true", help="Discover features")
    parser.add_argument("--prs", action="store_true", help="Extract PR metadata")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--min-confidence", type=float, default=0.0,
                        help="Min confidence threshold")

    args = parser.parse_args()

    # Extract commits
    print(f"📡 Extracting commits from {args.repo} (last {args.days} days)...")
    commits = extract_commits(args.repo, args.days)
    print(f"   Found {len(commits)} commits")

    if not commits:
        print("   No commits found. Nothing to classify.")
        return

    # Classify
    print("🏷️  Classifying...")
    classified = classify_commits_standalone(commits)

    # Filter by confidence
    if args.min_confidence > 0:
        classified = [c for c in classified if c["confidence"] >= args.min_confidence]

    # Summary
    type_counts: Dict[str, int] = {}
    for c in classified:
        type_counts[c["type"]] = type_counts.get(c["type"], 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(type_counts.items(), key=lambda x: -x[1]))
    print(f"   {len(classified)} classified: {summary}")

    result: Dict[str, Any] = {"classified_commits": classified}

    # Feature discovery
    if args.features:
        print("✨ Discovering features...")
        features = discover_features_standalone(classified)
        result["discovered_features"] = features
        for f in features[:5]:
            print(f"   → {f['name']} ({f['commit_count']} commits)")

    # PR extraction
    if args.prs:
        print("📋 Extracting PRs...")
        prs = extract_merge_prs(args.repo, args.days)
        result["pull_requests"] = prs
        print(f"   Found {len(prs)} PRs")

    # Output
    if args.json or args.output:
        json_str = json.dumps(result, indent=2, default=str)
        if args.output:
            with open(args.output, "w") as f:
                f.write(json_str)
            print(f"\n✅ Written to {args.output}")
        else:
            print(json_str)
    elif not args.json:
        print(f"\n✅ Done. Use --json for structured output.")


if __name__ == "__main__":
    main()
