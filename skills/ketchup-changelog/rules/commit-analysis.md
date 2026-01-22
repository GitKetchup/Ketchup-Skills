# Commit Analysis Best Practices

Guidelines for analyzing git commits to extract meaningful insights.

## Commit Message Parsing

### Conventional Commits

Parse commits following the [Conventional Commits](https://www.conventionalcommits.org/) spec:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance

### Non-Conventional Commits

For repos not using conventional commits:

1. Look for keywords: "fix", "add", "update", "remove", "refactor"
2. Check for issue references: `#123`, `fixes #456`
3. Analyze changed files to infer type
4. Use author patterns (some devs are consistent)

## Semantic Analysis

### Feature Detection

A commit likely adds a feature if:
- Message contains "add", "new", "implement", "introduce"
- Creates new files (not tests)
- Modifies UI components or API endpoints
- Has associated feature flag

### Bug Fix Detection

A commit likely fixes a bug if:
- Message contains "fix", "bug", "issue", "resolve", "patch"
- References an issue number
- Touches error handling code
- Small, focused changes

### Refactoring Detection

A commit is likely refactoring if:
- Message contains "refactor", "cleanup", "reorganize"
- Renames files/functions
- No functional change in tests
- Large file moves

## Risk Assessment

### High Risk Indicators
- Touches authentication/authorization code
- Modifies database schemas
- Changes payment/billing logic
- Large number of files changed
- Late-night commits
- Friday deployments

### Low Risk Indicators
- Documentation only
- Test additions
- Dependency updates (minor)
- Formatting changes

## Commit Quality Metrics

### Good Commits
- Single logical change
- Descriptive message
- Linked to issue/PR
- Includes tests

### Problematic Commits
- "WIP" or "fix" only messages
- Mixing unrelated changes
- No tests for new features
- Giant commits (>500 lines)

## Using Ketchup Tools

```python
# Analyze commit patterns
commits = get_git_log(repo_path)
process_health = analyze_process(commits)

# Check for anti-patterns
if process_health["anti_patterns"]:
    for pattern in process_health["anti_patterns"]:
        print(f"Warning: {pattern['name']} - {pattern['suggestion']}")

# Assess complexity impact
complexity = analyze_complexity(repo_path)
if complexity["summary"]["grade"] in ["D", "F"]:
    print("High complexity detected - review needed")
```

## Grouping Related Commits

When generating changelogs, group commits by:

1. **Feature Branch**: All commits in a merged PR
2. **Issue Reference**: Commits mentioning same issue
3. **File Overlap**: Commits touching same files
4. **Time Window**: Commits within short time span by same author
5. **Semantic Similarity**: Similar commit messages

## Output Format

For each logical change, provide:

```json
{
  "type": "feature|fix|refactor|...",
  "scope": "component or area affected",
  "description": "user-facing summary",
  "commits": ["sha1", "sha2"],
  "risk_level": "low|medium|high",
  "breaking": false,
  "contributors": ["author1", "author2"]
}
```
