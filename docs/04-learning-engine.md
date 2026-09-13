# Learning Engine

The learning engine is deterministic first. It should be understandable,
testable, and explainable before ML is introduced.

## Inputs

- learning path;
- topic prerequisites;
- user knowledge state;
- recent attempts;
- exercise difficulty.

## Outputs

- next recommended action;
- target topic or exercise;
- reason.

## Initial Mastery Rule

```text
new_mastery = old_mastery * 0.7 + attempt_score * 0.3
```

Scores are represented from 0 to 100.

## Initial Recommendation Rules

- If a required skill is weak, recommend practice for that skill.
- If a user repeatedly fails, recommend an explanation before more practice.
- If prerequisites are met, unlock the next topic.
- If easy exercises are passed, increase difficulty.
- If harder exercises fail, decrease difficulty.

Every recommendation should have a reason.
