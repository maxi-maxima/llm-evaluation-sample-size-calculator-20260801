# LLM Evaluation Sample Size Calculator

Prompt and model changes often ship after tiny evals that cannot detect real regressions. This CLI estimates how many samples you need per candidate and what the run will cost.

## Why now

AI agent teams are moving from demos to production gates. Cost control, eval quality, and model routing decisions are now discussed together, especially as CLI agents and automated reviewers run continuously.

## Install and run

```bash
python -m llm_evaluation_sample_size_calculator_20260801.cli --baseline 0.72 --target 0.80 --input-tokens 1500 --output-tokens 600 --input-price 1 --output-price 5
python -m unittest discover -s tests
```

## Example

```json
{
  "samples_per_candidate": 470,
  "candidates": 2,
  "estimated_cost_usd": 3.48
}
```

## Roadmap

- CSV scenario comparison
- Non-binary score support
- CI budget gate mode
