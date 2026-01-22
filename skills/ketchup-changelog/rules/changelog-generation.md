# Changelog Generation Best Practices

When generating changelogs from git commits, follow these guidelines for high-quality output.

## Structure

A good changelog should have:

1. **Version Header**: Clear version number and date
2. **Category Sections**: Group changes by type
3. **Descriptive Entries**: User-focused descriptions
4. **Breaking Changes**: Highlighted prominently

## Categories

Use these standard categories:

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Features marked for removal
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes

## Writing Style

### DO:
- Write from the user's perspective ("You can now...")
- Use active voice ("Added dark mode" not "Dark mode was added")
- Be specific about what changed
- Link to relevant issues/PRs when available
- Highlight breaking changes with ⚠️

### DON'T:
- Include internal implementation details
- Use technical jargon without explanation
- List every single commit (aggregate related changes)
- Forget to mention migration steps for breaking changes

## Commit Analysis

When analyzing commits to generate changelog entries:

1. **Group by Feature**: Combine related commits into single entries
2. **Identify Scope**: Determine which component/area is affected
3. **Determine Impact**: Is this user-facing or internal?
4. **Extract Context**: Use PR descriptions and issue links

## Example Output

```markdown
## [1.2.0] - 2024-01-15

### Added
- Dark mode support across all pages (#123)
- Export to PDF functionality in reports
- Keyboard shortcuts for common actions

### Changed
- Improved loading performance by 40%
- Updated dashboard layout for better readability

### Fixed
- Fixed crash when uploading large files (#456)
- Resolved timezone issues in date picker

### Security
- Patched XSS vulnerability in comments (CVE-2024-1234)
```

## Using with Ketchup Tools

```
1. analyze_complexity - Identify high-impact changes
2. get_contributor_skills - Credit contributors appropriately
3. get_momentum - Add velocity context
4. generate changelog with above context
```
