# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [0.1.1]

### Added - 2026-03-04
- Resolvendo bugs de CI/CD

---

## [0.1.0] — 2026-03-04

### Added
- Comando `octo` disponível como entry point após instalação
- Suporte ao estilo **moderno** (`Mapped` + `mapped_column`) do SQLAlchemy
- Subcomando `list` — lista colunas com tipo, opcional e estilo
- Subcomando `add` — adiciona coluna com opções `--nullable`, `--primary-key`, `--unique`, `--index`, `--autoincrement`
- Subcomando `rm` — remove coluna por nome com validação
- Modo interativo (`octo <directory> <tablename>` ou `fam <directory> <tablename> i`) com menu passo a passo
- Mapeamento de tipos Python → SQLAlchemy (`str→String`, `int→Integer`, etc.)
- Suite de testes com pytest cobrindo todos os casos de uso principais
- CI/CD via GitHub Actions com matriz Python 3.10 / 3.11 / 3.12
- Publicação automática no PyPI via OIDC trusted publishing ao criar tag `v*.*.*`

[Unreleased]: https://github.com/samuelbagatelli/octocli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/samuelbagatelli/octocli/releases/tag/v0.1.0
