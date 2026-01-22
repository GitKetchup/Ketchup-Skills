# Momentum Scoring Guide

Understanding and using the momentum score to assess development velocity.

## What is Momentum?

Momentum measures whether a team is:
- **Accelerating**: Shipping faster while managing complexity
- **Maintaining**: Consistent pace
- **Decelerating**: Slowing down or accumulating debt

## The Formula

```
Momentum = Velocity Growth / Complexity Growth
```

Where:
- **Velocity Growth** = (Current Commits / Previous Commits) - 1
- **Complexity Growth** = (Current Avg Complexity / Previous Avg Complexity) - 1

## Interpreting Scores

| Score | Grade | Interpretation |
|-------|-------|----------------|
| > 1.5 | A+ | Exceptional - shipping fast, low debt |
| 1.2 - 1.5 | A | Excellent - ahead of the curve |
| 1.0 - 1.2 | B | Good - keeping pace |
| 0.8 - 1.0 | C | Fair - slight slowdown |
| 0.6 - 0.8 | D | Concerning - accumulating debt |
| < 0.6 | F | Critical - velocity declining |

## Factors Affecting Momentum

### Positive Factors
- Consistent commit frequency
- Refactoring that reduces complexity
- Good test coverage
- Clear feature boundaries
- Efficient code reviews

### Negative Factors
- Technical debt accumulation
- Large, complex features
- Frequent reverts
- High bug rate
- Context switching

## Using the Tool

```python
from ketchup_mcp import get_momentum

# Basic usage
result = get_momentum(
    commits=current_period_commits,
    current_complexity=12.5
)

print(f"Momentum: {result['score']:.2f}")
print(f"Grade: {result['grade']}")
print(f"Interpretation: {result['interpretation']}")

# With comparison period
result = get_momentum(
    commits=current_period_commits,
    current_complexity=12.5,
    previous_commits=last_month_commits,
    previous_complexity=11.0
)
```

## Trend Analysis

Track momentum over time to identify patterns:

```
Week 1: 1.2 (A)
Week 2: 1.1 (B)
Week 3: 0.9 (C)
Week 4: 0.7 (D)
```

**Trend**: Declining - investigate causes

Common causes of declining momentum:
1. Sprint scope creep
2. Unplanned tech debt work
3. Team changes
4. External dependencies

## Team Insights

Use momentum with contributor skills:

```python
momentum = get_momentum(commits, complexity)
skills = get_contributor_skills(commits)

# Identify if momentum correlates with team changes
if momentum['score'] < 0.8:
    if skills['team_size'] changed:
        print("Momentum drop may be due to team changes")
    if skills['bus_factor'] < 2:
        print("Low bus factor - knowledge concentration risk")
```

## Reporting

When presenting momentum to stakeholders:

### Good Report
```
Development Momentum: A (1.25)

Summary: Team is shipping 25% faster than last period while 
maintaining code quality. Complexity increased only 5% despite 
adding 3 major features.

Contributors: 5 active (+1 from last period)
Key achievements: Authentication revamp, Dashboard v2
```

### Concerning Report
```
Development Momentum: D (0.65)

Summary: Velocity dropped 35% this period. Complexity increased 
20% due to legacy migration work.

Recommendations:
1. Allocate time for tech debt reduction
2. Break large features into smaller increments
3. Review and improve code review process
```

## Best Practices

1. **Measure consistently**: Same time periods, same metrics
2. **Context matters**: Low momentum during refactoring is okay
3. **Don't game it**: Splitting commits artificially defeats purpose
4. **Combine with quality**: Momentum + test coverage + security
5. **Team discussion**: Use as conversation starter, not judgment
