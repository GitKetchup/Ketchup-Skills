"""
Tests for Ketchup Classify skill.
"""

import sys
import os
import unittest

# Add scripts dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from classify import (
    _fallback_classify,
    _fallback_discover,
    extract_merge_prs,
)


class TestFallbackClassifier(unittest.TestCase):
    """Test the standalone rule-based classifier."""

    def test_conventional_commit_feat(self):
        commits = [{"sha": "abc123", "message": "feat(auth): add OAuth login"}]
        result = _fallback_classify(commits)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "feature")
        self.assertEqual(result[0]["scope"], "auth")
        self.assertEqual(result[0]["confidence"], 0.95)
        self.assertFalse(result[0]["is_breaking"])

    def test_conventional_commit_fix(self):
        commits = [{"sha": "def456", "message": "fix: resolve race condition in worker"}]
        result = _fallback_classify(commits)
        self.assertEqual(result[0]["type"], "fix")
        self.assertIsNone(result[0]["scope"])

    def test_conventional_commit_breaking(self):
        commits = [{"sha": "ghi789", "message": "feat(api)!: remove deprecated endpoints"}]
        result = _fallback_classify(commits)
        self.assertTrue(result[0]["is_breaking"])
        self.assertEqual(result[0]["type"], "feature")

    def test_keyword_classification(self):
        commits = [{"sha": "jkl012", "message": "Add new dashboard component"}]
        result = _fallback_classify(commits)
        self.assertEqual(result[0]["type"], "feature")
        self.assertEqual(result[0]["confidence"], 0.7)

    def test_keyword_fix(self):
        commits = [{"sha": "mno345", "message": "Fix login button not responding"}]
        result = _fallback_classify(commits)
        self.assertEqual(result[0]["type"], "fix")

    def test_keyword_docs(self):
        commits = [{"sha": "pqr678", "message": "Update README with new instructions"}]
        result = _fallback_classify(commits)
        self.assertEqual(result[0]["type"], "docs")

    def test_merge_commit(self):
        commits = [{"sha": "stu901", "message": "Merge branch 'main' into feature"}]
        result = _fallback_classify(commits)
        self.assertEqual(result[0]["type"], "chore")

    def test_fallback_unknown(self):
        commits = [{"sha": "vwx234", "message": "WIP stuff"}]
        result = _fallback_classify(commits)
        self.assertEqual(result[0]["type"], "chore")
        self.assertEqual(result[0]["confidence"], 0.4)

    def test_batch_classification(self):
        commits = [
            {"sha": "a1", "message": "feat: new login"},
            {"sha": "a2", "message": "fix: broken CSS"},
            {"sha": "a3", "message": "docs: update changelog"},
            {"sha": "a4", "message": "chore: bump version"},
            {"sha": "a5", "message": "test: add unit tests"},
        ]
        results = _fallback_classify(commits)
        self.assertEqual(len(results), 5)
        types = [r["type"] for r in results]
        self.assertEqual(types, ["feature", "fix", "docs", "chore", "test"])

    def test_empty_message(self):
        commits = [{"sha": "empty", "message": ""}]
        result = _fallback_classify(commits)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "chore")


class TestFallbackDiscovery(unittest.TestCase):
    """Test the standalone feature discovery."""

    def test_scope_grouping(self):
        classified = [
            {"sha": "a1", "type": "feature", "scope": "auth", "description": "add login"},
            {"sha": "a2", "type": "feature", "scope": "auth", "description": "add logout"},
            {"sha": "a3", "type": "feature", "scope": "dashboard", "description": "add charts"},
        ]
        features = _fallback_discover(classified)
        self.assertEqual(len(features), 2)
        names = {f["name"] for f in features}
        self.assertIn("Auth", names)
        self.assertIn("Dashboard", names)

    def test_ignores_non_feature_types(self):
        classified = [
            {"sha": "a1", "type": "docs", "scope": None, "description": "update readme"},
            {"sha": "a2", "type": "chore", "scope": None, "description": "bump deps"},
        ]
        features = _fallback_discover(classified)
        self.assertEqual(len(features), 0)

    def test_includes_fixes(self):
        classified = [
            {"sha": "a1", "type": "fix", "scope": "auth", "description": "fix token refresh"},
        ]
        features = _fallback_discover(classified)
        self.assertEqual(len(features), 1)

    def test_significance_calculation(self):
        classified = [
            {"sha": f"a{i}", "type": "feature", "scope": "big", "description": f"change {i}"}
            for i in range(5)
        ]
        features = _fallback_discover(classified)
        self.assertEqual(len(features), 1)
        self.assertGreater(features[0]["significance"], 0.5)


if __name__ == "__main__":
    unittest.main()
