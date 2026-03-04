# OctoCLI - FastAPI Backend Manager

> Edite projetos com FastAPI diretamente via CLI.

[![PyPI version](https://img.shields.io/pypi/v/octocli)](https://pypi.org/project/octocli)
[![Python](https://img.shields.io/pypi/pyversions/fam)](https://pypi.org/project/fam/)
[![CI](https://github.com/youruser/fam/actions/workflows/ci.yml/badge.svg)](https://github.com/youruser/fam/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## Instalação

```bash
pip install octocli
```

Requer Python >= 3.10. Sem dependências externas.

---

## Uso rápido

```bash
# Modo interativo (menu guiado)
octo models user

# Listar colunas
octo models user list

# Adicionar colunas
octo models user add age int
octo models user add phone str --unique
octo models user add bio str --nullable

# Remover coluna
octo models user rm age
```

---

## Tipos Python → SQLAlchemy

| Python | SQLAlchemy |
|--------|-----------|
| `str` | `String` |
| `int` | `Integer` |
| `float` | `Float` |
| `bool` | `Boolean` |
| `datetime` | `DateTime` |
| `date` | `Date` |
| `bytes` | `LargeBinary` |
| `dict` / `list` | `JSON` |
| `Decimal` | `Numeric` |

Tipos não mapeados são passados diretamente (ex: `UUID`).

---

## Desenvolvimento

```bash
git clone https://github.com/samuelbagatelli/octocli
cd octocli
pip install -e ".[dev]"

# Rodar testes
pytest

# Lint
ruff check src/ tests/
```

---

## Publicação (release)

```bash
# 1. Atualize a versão em src/fam/__init__.py e pyproject.toml
# 2. Atualize o CHANGELOG.md
# 3. Crie e envie a tag — o CI publica automaticamente no PyPI
git tag v0.2.0
git push origin v0.2.0
```

O CI usa [OIDC trusted publishing](https://docs.pypi.org/trusted-publishers/) —
não é necessário armazenar `PYPI_API_TOKEN` em secrets.

---

## Licença

MIT © Samuel Bagatelli
