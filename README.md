# heargent: Surprise-Gated Selective Initiation for Proactive LLM Agents

**Author:** Patrick Gergen  
**Paper:** `paper/heargent-paper-v2.pdf`  
**License:** MIT (2026)

## Overview

An empirical study of surprise-gated selective initiation mechanisms for proactive LLM agents. The core finding: structurally sound mechanism design can gate unnecessary model calls, but prompt-level improvements alone do not overcome architectural trade-offs.

**Binding result:** N=40 externally-authored traces, mechanism-diagnostic outcome with safety regression analysis.

## Structure

- **`paper/heargent-paper-v2.pdf`** — Final submission-ready paper (15 pages)
- **`code/`** — Agent harness, embedding predictor, test-trace generation
- **`runs/`** — Pre-registered milestones, locked paper-lines, data artifacts
- **`LICENSE`** — MIT (2026 Patrick Gergen)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent harness (requires Anthropic API key)
python -m heargent.harness

# Generate test traces (requires Claude API)
python -m heargent.traces
```

## Key Files

- **`runs/19`** — M11a pre-registration (locked decision tree)
- **`runs/22-v4-prompt-n40-extension-extension.md`** — Final N=40 milestone
- **`data/`** — Raw trace JSON, prediction, and decision logs

## Citation

If you use this work, please cite:

```bibtex
@article{gergen2026heargent,
  author = {Patrick Gergen},
  title = {Surprise-Gated Selective Initiation with a Claude-API Arbiter: A Negative Result on Targeted Prompt Revision at N=40 Fresh Externally-Authored Traces},
  journal = {arXiv preprint},
  year = {2026},
  note = {Submitted to cs.AI}
}
```

## Contact

Patrick Gergen — patrick_gergen@hotmail.com
