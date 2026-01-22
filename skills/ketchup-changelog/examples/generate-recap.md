# Example: Generate a Release Recap

This example shows how to use Ketchup tools to generate a comprehensive release recap.

## Scenario

You've just finished a sprint and want to:
1. Analyze what was built
2. Assess code quality
3. Generate a changelog
4. Create a video recap

## Step 1: Analyze the Codebase

First, check the current state of the codebase:

```
Use analyze_complexity on /path/to/repo
```

**Expected output:**
```json
{
  "summary": {
    "total_functions": 234,
    "avg_complexity": 8.5,
    "grade": "B",
    "total_loc": 15420
  },
  "by_language": {
    "typescript": { "functions": 180, "avg_complexity": 7.2 },
    "python": { "functions": 54, "avg_complexity": 12.1 }
  }
}
```

## Step 2: Check Security

Scan for vulnerabilities:

```
Use check_security on /path/to/repo
```

**Expected output:**
```json
{
  "vulnerabilities": [
    {
      "id": "CVE-2024-1234",
      "severity": "high",
      "package": "lodash",
      "fixed_in": "4.17.21"
    }
  ],
  "summary": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 5
  },
  "grade": "B"
}
```

## Step 3: Calculate Momentum

Check development velocity:

```
Use get_momentum with:
- commits: [last 2 weeks of commits]
- current_complexity: 8.5
- previous_commits: [prior 2 weeks]
- previous_complexity: 9.2
```

**Expected output:**
```json
{
  "score": 1.35,
  "grade": "A",
  "velocity_growth": 0.20,
  "complexity_growth": -0.08,
  "interpretation": "Excellent momentum! Team is shipping 20% faster while reducing complexity by 8%."
}
```

## Step 4: Get Contributor Skills

Identify who built what:

```
Use get_contributor_skills with commits from the sprint
```

**Expected output:**
```json
{
  "contributors": [
    {
      "username": "alice",
      "commits": 23,
      "primary_languages": ["typescript", "react"],
      "areas": ["frontend", "components"]
    },
    {
      "username": "bob",
      "commits": 18,
      "primary_languages": ["python"],
      "areas": ["backend", "api"]
    }
  ],
  "team_size": 5,
  "bus_factor": 3
}
```

## Step 5: Analyze Process Health

Check for workflow issues:

```
Use analyze_process with sprint commits
```

**Expected output:**
```json
{
  "flow_score": 85,
  "grade": "B+",
  "activity_breakdown": {
    "features": 45,
    "fixes": 30,
    "refactors": 15,
    "chores": 10
  },
  "anti_patterns": [
    {
      "name": "friday_deploys",
      "count": 2,
      "suggestion": "Consider deploying earlier in the week"
    }
  ]
}
```

## Step 6: Generate Changelog

Using all the above context, generate a changelog:

```markdown
## Sprint 23 Release - January 2024

### Highlights
- 🚀 **Momentum Score: A (1.35)** - Team exceeded velocity targets
- 👥 **5 Contributors** - Alice, Bob, Carol, Dave, Eve
- 📊 **41 Commits** - 45% features, 30% fixes

### Added
- Dark mode support across all pages (@alice)
- Real-time notifications system (@bob)
- Export to CSV functionality (@carol)

### Fixed
- Dashboard loading performance improved 40%
- Fixed timezone bugs in date picker
- Resolved memory leak in image processor

### Security
- ⚠️ Updated lodash to patch CVE-2024-1234
- Added rate limiting to API endpoints

### Code Quality
- Complexity reduced from 9.2 to 8.5 (-8%)
- Security grade improved from C to B
- Bus factor: 3 (healthy knowledge distribution)

### Contributors
| Name | Commits | Focus |
|------|---------|-------|
| Alice | 23 | Frontend |
| Bob | 18 | Backend |
| Carol | 12 | Features |
| Dave | 8 | DevOps |
| Eve | 5 | Testing |
```

## Step 7: Generate Video (Cloud)

If you have an API key, trigger video generation:

```
Use Ketchup Cloud API:
POST /api/stories/{id}/generate-media
{
  "outputTypes": ["video"],
  "videoProvider": "remotion",
  "branding": { "primaryColor": "#EB3529" }
}
```

## Full Prompt

You can ask Claude to do all of this at once:

```
Analyze the repository at /path/to/repo and generate a comprehensive 
release recap including:
1. Code complexity analysis
2. Security scan results
3. Development momentum
4. Contributor breakdown
5. Formatted changelog in markdown

Use the Ketchup tools to gather this information.
```
