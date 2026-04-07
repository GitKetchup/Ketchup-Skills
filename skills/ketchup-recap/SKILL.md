---
name: ketchup-recap
version: 1.0.0
description: Generate video recaps of code changes using Ketchup
---

# Ketchup Recap Skill

Generate cinematic video recaps of recent code changes. This skill powers the
"rapid-recap" pipeline — turning git commits into narrated product videos in
under 3 minutes.

## How It Works

1. **Extract** recent commits locally (privacy-first — zero source code leaves the machine)
2. **Cluster** commits into user-facing features using AI
3. **Narrativize** the features into a voiceover script
4. **Render** a cinematic video via Remotion (free) or FAL.ai (paid)

## Quick Start

### Via CLI
```bash
# Generate a weekly recap video
ketchup cloud recap --days 7

# Daily recap, skip video (analysis only)
ketchup cloud recap --days 1 --no-video

# Wait for the video to finish
ketchup cloud recap --wait
```

### Via MCP (AI Assistant)
Tell your AI assistant:
> "Generate a recap of what I built this week"

The Ketchup MCP server will:
1. Extract commits from the local repo
2. POST scrubbed metadata to Ketchup Cloud
3. Return a video URL when ready

### Via Web
Navigate to your project in the Ketchup web app and click "Quick Recap".

## What Gets Sent to the Cloud

**Only scrubbed metadata.** For each commit:
- SHA hash
- Commit message (first 200 characters)
- Author name
- Date
- File count, additions, and deletions

**Never sent:** source code, file contents, diffs, file paths, or secrets.

## Commit Taxonomy

The AI clusters commits using this taxonomy:

| Type | Description | Example |
|------|-------------|---------|
| `feature` | New user-facing functionality | "Add login page" |
| `fix` | Bug fix | "Fix crash on empty input" |
| `refactor` | Code restructuring | "Extract auth into module" |
| `enhancement` | Improvement to existing feature | "Improve search speed" |
| `cleanup` | Remove dead code, formatting | "Remove unused imports" |

Even messy commits ("wip", "fix stuff", "asdf") are clustered by AI using
commit metadata patterns (timing, file counts, additions/deletions ratios).

## Configuration

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `KETCHUP_API_URL` | No | API base URL (default: https://app.gitketchup.com) |

### `.ketchup` Config
Created by `ketchup sync` — links the local repo to a Ketchup project:
```json
{
  "projectId": "your-project-uuid",
  "projectName": "My App"
}
```

## Integration with Other Skills

- **ketchup-classify**: Uses the same commit taxonomy for consistency
- **ketchup-diff-analyzer**: Provides deeper analysis for individual diffs
- **Remotion Skills**: Video rendering follows Remotion best practices
