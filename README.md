# octocli

CLI tool for managing FastAPI SQLAlchemy models — add, remove and inspect columns from the terminal.

## Installation

```bash
pip install octocli
```

## Usage

```bash
# Interactive mode
octo <directory> <tablename>

# Read model file
octo <directory> <tablename> read

# List columns
octo <directory> <tablename> list

# Add a column
octo <directory> <tablename> add <column> <type>
octo <directory> <tablename> add age int --nullable

# Remove a column
octo <directory> <tablename> rm <column>
```

## License

MIT © Samuel Bagatelli
