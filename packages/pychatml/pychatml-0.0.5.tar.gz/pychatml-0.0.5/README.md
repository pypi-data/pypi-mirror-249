# pychatml

The `pychatml` package allows you to convert chat interfaces from and to the ChatML format.

## Installation

You can install the `pychatml` package using pip:

```shell
pip install pychatml
```

## What

Makes it easy to integrate between different chat formats and models.

```python
from pychatml.llama2_converter import Llama2

PROMPT = """[INST] Hi, how are you? [/INST] Good thanks! 
[INST] Can you help me with this math program? [/INST]"""

converter = Llama2()

converter.to_chatml(PROMPT)
```
```json
[
    {"role": "user", "content": "Hi, how are you?"},
    {"role": "assistant", "content": "Good thanks!"},
    {"role": "user", "content": "Can you help me with this math program?"},
]
```

#### Supported formats


 - [x] Llama 2
 - [x] Anthropic
 - [x] Alpaca
 - [ ] Vicuna/ShareGPT

## Why?

![Motivation tweet](https://github.com/deployradiant/pychatml/assets/6087389/003d8898-d647-46d3-90cb-0051a8860519)
https://github.com/OpenAccess-AI-Collective/axolotl/pull/982

## Questions?

Create an issue or discussion in this repository.

Or, reach out to our team! [@jakob_frick](https://twitter.com/frick_jakob/), [@__anjor](https://twitter.com/__anjor), [@maxnajork](https://twitter.com/maxnajork) on X or [team@radiantai.com](mailto:team@radiantai.com).

## Contributing Guidelines

Thank you for your interest in contributing to our project! Before you begin writing code, it would be helpful if you read these [contributing guidelines](CONTRIBUTING.md). Following them will make the contribution process easier and more efficient for everyone involved.

Please note that the project is released with an [MIT License](https://opensource.org/licenses/MIT).

