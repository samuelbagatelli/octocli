# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OctoCLI is a Python CLI tool (`octo`) for managing SQLAlchemy models in FastAPI applications. It allows creating, reading, modifying, and deleting model files from the command line.

## Commands

```bash
# Install package locally for development
pip install -e .

# Run the CLI
octo --version

# Model commands (primary functionality)
octo model create <tablename>     # Create model from template
octo model read <tablename>        # Print model file contents
octo model delete <tablename>     # Delete model file
octo model list <tablename>       # List columns in table format
octo model add <tablename> --name <col> --type <type>  # Add column
octo model remove <tablename> --name <col>            # Remove column
```

## Architecture

### Entry Point
- `src/octocli/cli.py` - argparse-based CLI, entry point is `octocli.cli:main` (maps to `octo` command)
- `src/octocli/__init__.py` - version definition

### Core Module
- `src/octocli/model.py` - Core `Model` class that:
  - Generates model files from templates
  - Parses and modifies SQLAlchemy `Mapped[...]` column definitions
  - Maps Python types to SQLAlchemy types via `SQLTYPES` dict
  - Uses regex to parse column definitions in model files

### Templates
Located in `src/octocli/templates/`:
- `models/standard.py` - SQLAlchemy model template with `PrefixBase` inheritance, standard columns (id, created_at, updated_at, deleted)
- `prefix/prefix_base.py` - Abstract base class with table prefix support
- `settings/database.py` - SQLAlchemy engine/session setup
- `settings/config.py` - Pydantic settings for DB and RabbitMQ
- `routers/router.py` - FastAPI router template (CRUD endpoints)

### Model Generation Pattern
Models use `__incomplete_tablename__` and inherit from `PrefixBase`, which prepends a configurable table prefix from `SettingsPrefix`.

### Type Mapping
The `SQLTYPES` dict in `model.py` maps Python types to SQLAlchemy types:
`str`→`String`, `int`→`Integer`, `float`→`Float`, `bool`→`Boolean`, `datetime`→`DateTime`, `date`→`Date`, `bytes`→`LargeBinary`, `dict`/`list`→`JSON`

## Testing Report (2026-03-20)

### Errors Found

1. **`octo model ls` - AttributeError** (FIXED)
   - Command: `octo model ls <tablename>`
   - Error: `AttributeError: 'Model' object has no attribute 'list_columns'`
   - Location: `src/octocli/cli.py:79` - calls `model.list_columns()` which doesn't exist
   - Fix: Renamed `lscols()` method to `list_columns()` in `src/octocli/model.py:204`

2. **`octo model ls` - KeyError: 'nullable'** (FIXED)
   - Command: `octo model ls <tablename>`
   - Error: `KeyError: 'nullable'` when accessing column data
   - Location: `src/octocli/model.py:214` - `parsecols()` didn't extract `nullable` from args
   - Fix: Added `nullable` field extraction in `parsecols()` method

3. **`octo init` - Not Implemented**
   - Command: `octo init`
   - Error: Prints "Not implemented yet"
   - The init command has no implementation

### Documentation Discrepancies

The documented commands in CLAUDE.md don't match the actual CLI structure:

| Documented | Actual |
|------------|--------|
| `octo model create` | `octo model add` |
| `octo model read` | `octo model show` |
| `octo model delete` | `octo model rm` |
| `octo model list` | `octo model ls` |
| `octo model add` (with --name --type) | `octo column add` (with --type) |
| `octo model remove` | `octo column rm` |

## Standard Testing Procedure

When asked to test the application, follow this procedure:

1. **Create virtual environment and install:**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install -e .
   ```

2. **Test all CLI commands:**
   ```bash
   octo --version                    # Verify installation
   octo model add <tablename>        # Create a model
   octo model ls <tablename>         # List columns
   octo model show <tablename>       # Show model contents
   octo column add <t> <c> --type    # Add a column
   octo column rm <t> <c>            # Remove a column
   octo model rm <tablename>         # Delete model
   octo init                         # Init command (unimplemented)
   ```

3. **Clean up:**
   ```bash
   rm -rf .venv models/
   ```

4. **Document results:** Update this file with any errors found and fixes applied.
