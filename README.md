# NQ-Signal-Research-Node
### Autonomous Evaluation of Institutional Futures Signals

This repository serves as a research node for analyzing **NQ Futures** data using localized Agentic AI. It moves beyond simple technical analysis by utilizing LLMs as "Judge Agents" to validate institutional order flow.

## 🔬 Research Focus
- **Model Benchmarking:** Comparing sub-70B local models (GGUF/EXL2) against institutional signal logic.
- **Hallucination Mitigation:** Implementing **PydanticAI** to force structured, verifiable JSON outputs for trading execution.
- **Latency Analysis:** Measuring the "Tick-to-Thought" speed on an optimized RTX 3090 environment.

## 📊 Evaluation Framework
The node ingests Rithmic/Thinkorswim data logs and outputs a "Confidence Score" based on historical #BASHT alerts and institutional volume clusters.
