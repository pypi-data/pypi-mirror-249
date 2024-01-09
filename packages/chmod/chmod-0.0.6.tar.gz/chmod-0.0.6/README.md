# chmod-calculator

[![Tests](https://github.com/harrysharma1/chmod-calculator/actions/workflows/workflow.yml/badge.svg)](https://github.com/harrysharma1/chmod-calculator/actions/workflows/workflow.yml)

This is a python module for calculating chmod.
This is my first module so it will have some bugs.

## How to use

After running `pip install chmod you` can use it in Python

```python
import chmod
a = chmod.ChmodConversion()
# Octal to Symbolic
print(a.int_to_perm(172))
# Symbolic to Octal
print(a.perm_to_int("--xrwx-w-"))
```
