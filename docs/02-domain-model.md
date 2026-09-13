# Domain Model

## Core Entities

- `User`: the learner.
- `Goal`: high-level target, such as Python Backend Developer.
- `Skill`: measurable knowledge unit, such as `http_status_codes`.
- `Topic`: learning unit that groups skills, such as HTTP Basics.
- `LearningPath`: ordered path toward a goal.
- `LearningPathStep`: one topic inside a path.
- `ContentItem`: explanation or learning material.
- `Exercise`: task mapped to one or more skills.
- `Attempt`: user's submitted answer.
- `Evaluation`: result of checking an attempt.
- `KnowledgeState`: system estimate of user mastery per skill.
- `Recommendation`: next suggested learning action.

## Important Distinction

```text
Content teaches.
Exercises measure.
KnowledgeState estimates understanding.
Recommendations decide what to do next.
```
