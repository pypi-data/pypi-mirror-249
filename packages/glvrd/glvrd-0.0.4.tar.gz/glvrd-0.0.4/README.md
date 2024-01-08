# glvrd - неофициальный клиент к сервису glvrd.ru

[![Downloads](https://static.pepy.tech/badge/glvrd/month)](https://pepy.tech/project/glvrd)
[![Downloads](https://static.pepy.tech/badge/glvrd)](https://pepy.tech/project/glvrd)
[![codecov](https://codecov.io/gh/pomponchik/glvrd/graph/badge.svg?token=LVGTo8aGM2)](https://codecov.io/gh/pomponchik/glvrd)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/glvrd?branch=main)](https://hitsofcode.com/github/pomponchik/glvrd/view?branch=main)
[![Tests](https://github.com/pomponchik/glvrd/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/glvrd/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/glvrd.svg)](https://pypi.python.org/pypi/glvrd)
[![PyPI version](https://badge.fury.io/py/glvrd.svg)](https://badge.fury.io/py/glvrd)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Это неофициальный и не production-ready клиент для замечательного сервиса проверки текстов - glvrd.ru. Работает в обход API, так что на особую скорость советую не расчитывать.

Устанавливается так:

```bash
pip install glvrd
```

Пример кода:

```python
from glvrd import GlvrdClient

client = GlvrdClient()
text = 'Это неофициальный и не production-ready клиент для замечательного сервиса проверки текстов - glvrd.ru. Работает в обход API, так что на особую скорость советую не расчитывать.'

def print_estimate(estimate, what_is_it):
  print(f'{what_is_it}: {estimate.estimate}/10')
  for error_name, examples in estimate.errors.items():
    print(f'{error_name}:')
    for example in examples:
      print(f'\t{example}')
  print()

print_estimate(client.estimate_clarity(text), 'Чистота')
print_estimate(client.estimate_readability(text), 'Читаемость')
```

... выдаст что-то вроде:

```
Чистота: 8.1/10
Необъективная оценка:
	замечательного
Усилитель:
	особую

Читаемость: 8.8/10
В начале предложения нет глагола:
	Это неофициальный и не production-ready клиент для замечательного сервиса
Подозрение на парцелляцию:
	Работает в обход
```
