# Video Recap Generation Guide

Best practices for generating video recaps from development activity.

## Overview

Ketchup can generate two types of videos:

| Type | Technology | Best For | Tier |
|------|------------|----------|------|
| Motion Graphics | Remotion | Clean, professional look | Free |
| AI Video | FAL.ai | Cinematic, photorealistic | Paid |

## Content Strategy

### What Makes a Good Video Recap

1. **Hook** (0-5s): Grab attention with key achievement
2. **Context** (5-15s): Set the scene - what was the goal?
3. **Highlights** (15-45s): Show 3-5 key changes
4. **Impact** (45-55s): What does this mean for users?
5. **CTA** (55-60s): Next steps, where to learn more

### Content Sources

Extract video content from:
- Feature names and descriptions
- Commit messages (grouped by feature)
- PR descriptions
- Issue titles
- Complexity improvements
- Security fixes

## Script Writing

### Voice & Tone

**DO:**
- User-focused language
- Active voice
- Concrete examples
- Energy and enthusiasm

**DON'T:**
- Technical jargon
- Internal code names
- Boring enumeration
- Passive voice

### Example Script

```
[HOOK]
"Version 2.0 is here - and it's a game changer."

[CONTEXT]
"Over the past month, our team of 5 developers shipped 
47 commits focused on one goal: making your experience 
10x faster."

[HIGHLIGHTS]
"First up: Dashboard performance. We rewrote the core 
rendering engine, cutting load times from 3 seconds to 
under 300 milliseconds."

"Next: Dark mode. Finally. Every screen, every component, 
beautifully dark."

"And for security: We patched 3 vulnerabilities and added 
two-factor authentication."

[IMPACT]
"This isn't just an update - it's a transformation. 
Your workflow just got a whole lot smoother."

[CTA]
"Try it now at yourapp.com"
```

## Visual Design

### Motion Graphics (Remotion)

Best practices for template-based videos:

- **Colors**: Use brand primary + 1-2 accents
- **Typography**: Large, readable text (min 48px for headings)
- **Animations**: Smooth easing, 0.3-0.5s duration
- **Transitions**: Fade or slide, not jarring cuts
- **Pacing**: 3-5 seconds per scene

### AI Video (FAL.ai)

Best practices for AI-generated videos:

- **Prompts**: Be specific about style, mood, lighting
- **Consistency**: Use same style seed across scenes
- **Duration**: Keep clips 5-10 seconds (AI limit)
- **Thumbnails**: Generate concept art as reference

## Using Ketchup Tools

### Generate Script Context

```python
# Gather insights for script
complexity = analyze_complexity(repo_path)
momentum = get_momentum(commits, complexity['summary']['avg'])
contributors = get_contributor_skills(commits)
security = check_security(repo_path)

# Build context
context = {
    "commits_count": len(commits),
    "contributors": contributors['team_size'],
    "complexity_grade": complexity['summary']['grade'],
    "momentum_score": momentum['score'],
    "security_fixed": len(security['vulnerabilities']),
    "features": extract_features(commits)
}
```

### Cloud API (Paid)

```python
# Generate full video via Ketchup Cloud
response = requests.post(
    "https://app.gitketchup.com/api/stories/{id}/generate-media",
    json={
        "outputTypes": ["video"],
        "videoProvider": "fal-kling",  # AI video
        "branding": {
            "primaryColor": "#EB3529",
            "logoUrl": "https://..."
        }
    }
)
```

## Video Specifications

| Platform | Aspect | Resolution | Duration |
|----------|--------|------------|----------|
| YouTube | 16:9 | 1920x1080 | 60-90s |
| LinkedIn | 16:9 | 1920x1080 | 30-60s |
| Twitter/X | 16:9 | 1280x720 | 15-45s |
| TikTok | 9:16 | 1080x1920 | 15-60s |
| Instagram Reels | 9:16 | 1080x1920 | 15-30s |

## Distribution

After generating video:

1. **Download**: Get MP4 from Ketchup dashboard
2. **Thumbnail**: Auto-generated or custom
3. **Captions**: Generate SRT with transcription
4. **Platforms**: Upload to relevant channels
5. **Analytics**: Track views and engagement

## Examples

### Release Announcement
- Style: Energetic, celebratory
- Duration: 45-60s
- Focus: New features, user benefits

### Monthly Recap
- Style: Professional, comprehensive
- Duration: 60-90s
- Focus: All changes, team highlights

### Security Update
- Style: Serious, reassuring
- Duration: 30-45s
- Focus: What was fixed, user safety

### Milestone Celebration
- Style: Fun, team-focused
- Duration: 30-45s
- Focus: Achievement, contributor recognition
