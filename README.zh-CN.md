# LLM Evaluation Sample Size Calculator

提示词和模型变更常常只跑很小的 eval 就上线，根本无法发现真实回归。这个 CLI 会估算每个候选方案需要多少样本，以及整轮评测大约花多少钱。

## 为什么现在值得做

AI Agent 团队正在从演示走向生产门禁。成本控制、评测质量和模型路由决策正在被放到一起讨论，尤其是 CLI Agent 和自动 Review 长期运行后。

## 安装与运行

```bash
python -m llm_evaluation_sample_size_calculator_20260801.cli --baseline 0.72 --target 0.80 --input-tokens 1500 --output-tokens 600 --input-price 1 --output-price 5
python -m llm_evaluation_sample_size_calculator_20260801.cli --scenarios-csv examples/scenarios.csv
python -m unittest discover -s tests
```

## 示例

```json
{
  "samples_per_candidate": 470,
  "candidates": 2,
  "estimated_cost_usd": 3.48
}
```

## 路线图

- 支持非二元评分
- CI 成本门禁模式
