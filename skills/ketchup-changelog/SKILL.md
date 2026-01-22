---
name: ketchup-changelog
description: Transform git commits into narrative stories, video recaps, and social content. Automated changelog generation powered by AI with local analysis tools.
---

# Ketchup Changelog Skill

Use this skill when you need to:
- Generate release notes from git commits
- Create video recaps of development progress
- Analyze codebase health, complexity, and momentum
- Detect AI-generated code in PRs
- Get contributor skills and knowledge graphs

## Quick Start

### Install via skills.sh
```bash
npx skills add ketchup-dev/skills --skill ketchup-changelog
```

### Or install MCP Server directly
```bash
pip install ketchup-mcp
ketchup-mcp
```

## Tools Available

### Local Tools (No API key required)

These tools run entirely on your machine and never send code to the cloud.

#### `analyze_complexity`
Analyze code complexity for a repository or directory.

```
Args:
  repo_path: Path to the repository to analyze
  file_extensions: Optional list of extensions (e.g., ["py", "ts"])

Returns:
  - functions: List of functions with complexity metrics
  - summary: Aggregate stats (avg complexity, total LOC, grade)
  - by_language: Breakdown by programming language
```

**Example:**
```
analyze_complexity("/path/to/repo", ["ts", "tsx"])
```

---

#### `check_security`
Scan repository for security vulnerabilities using OSV-Scanner and Safety.

```
Args:
  repo_path: Path to the repository to scan

Returns:
  - vulnerabilities: List with CVE IDs and severity
  - summary: Counts by severity (critical, high, medium, low)
  - grade: Overall security grade (A-F)
```

---

#### `detect_ai_code`
Detect if a file contains AI-generated code using heuristic pattern matching.

```
Args:
  file_path: Path to the file to analyze

Returns:
  - ai_probability: 0.0 to 1.0 likelihood
  - classification: "human", "mixed", or "ai"
  - ai_signals: Evidence of AI generation
  - human_signals: Evidence of human writing
```

---

#### `get_momentum`
Calculate momentum score for a development period.

Momentum = Velocity Growth / Complexity Growth
- Score > 1.0: Ahead of the curve
- Score = 1.0: Keeping pace
- Score < 1.0: Falling behind

```
Args:
  commits: List of commits with {author, message, timestamp}
  current_complexity: Average complexity score
  previous_commits: Optional commits from previous period
  previous_complexity: Optional complexity from previous period

Returns:
  - score: The momentum score
  - grade: Letter grade (A+ to F)
  - velocity_growth: Percentage change in velocity
  - interpretation: Human-readable summary
```

---

#### `analyze_process`
Analyze development process health from commit history.

```
Args:
  commits: List of commits with {author, message, timestamp, type}

Returns:
  - flow_score: 0-100 process health score
  - grade: Letter grade (A-F)
  - activity_breakdown: Commit types distribution
  - anti_patterns: Detected workflow issues
```

---

#### `get_contributor_skills`
Build contributor skills graph from commit history.

```
Args:
  commits: List of commits with {author, message, files}
  username: Optional filter to specific contributor

Returns:
  - contributors: List of contributor profiles
  - team_size: Number of unique contributors
  - bus_factor: Knowledge concentration risk
  - language_distribution: Languages used by team
```

---

### Cloud Tools (Requires API Key)

These tools connect to Ketchup Cloud for pre-computed analytics and story generation.

Set `KETCHUP_API_KEY` environment variable to enable.

#### `get_project_recaps`
Fetch recent recaps/stories for a project.

```
Args:
  repo_full_name: GitHub repo in "owner/repo" format
  limit: Maximum recaps to fetch (default: 5)

Returns:
  - recaps: List of recent recap summaries
  - project_id: The Ketchup project ID
```

---

#### `get_project_momentum`
Get pre-calculated momentum data from Ketchup Cloud (faster than local).

```
Args:
  repo_full_name: GitHub repo in "owner/repo" format

Returns:
  - momentum: Score, grade, interpretation
  - velocity_pulse: Contributor velocity trends
  - health_trend: Codebase health over time
  - overall_grade: Combined grade
```

---

#### `get_project_forensics`
Get forensics summary including complexity hotspots and security issues.

```
Args:
  repo_full_name: GitHub repo in "owner/repo" format

Returns:
  - complexity_hotspots: High-complexity files/functions
  - security_summary: Vulnerability counts by severity
  - quick_wins: Actionable recommendations
```

---

## Get API Key

1. Sign up at https://app.gitketchup.com
2. Go to Settings → API Keys
3. Generate a new key
4. Set `KETCHUP_API_KEY` environment variable

## Example Workflows

### Generate Changelog from Recent Commits

```
1. Use analyze_complexity to assess current codebase
2. Use get_contributor_skills to identify key contributors
3. Use get_momentum to understand development velocity
4. Combine insights into a narrative changelog
```

### Security Audit

```
1. Use check_security to scan for vulnerabilities
2. Use detect_ai_code on suspicious files
3. Use analyze_process to check for anti-patterns
4. Generate security report with findings
```

### Code Review Prep

```
1. Use analyze_complexity on changed files
2. Use detect_ai_code on new additions
3. Highlight high-complexity or AI-generated sections
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `KETCHUP_API_KEY` | API key for cloud features | For cloud tools |
| `KETCHUP_API_URL` | Custom API endpoint | No (defaults to production) |

### MCP Server Options

```bash
# Local mode only
ketchup-mcp

# With cloud API
KETCHUP_API_KEY=your-key ketchup-mcp

# Custom endpoint (for self-hosted)
KETCHUP_API_URL=https://your-instance.com/api ketchup-mcp
```

## Supported Platforms

- **Claude Desktop**: Add to `claude_desktop_config.json`
- **Cursor**: Install via skills command
- **VS Code + Continue**: MCP configuration
- **Custom**: Any MCP-compatible client

## Privacy

- Local tools NEVER send your code to any server
- Cloud tools only send repository metadata (not source code)
- API keys are stored locally and never logged

## Links

- **Website**: https://gitketchup.com
- **Documentation**: https://docs.gitketchup.com
- **Remotion Best Practices**: https://skills.sh/remotion-dev/skills/remotion-best-practices
- **GitHub**: https://github.com/ketchup-dev
- **Support**: support@gitketchup.com
