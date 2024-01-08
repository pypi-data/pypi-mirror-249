# dotclear-backup-parser

`dotclear-backup-parser` is a Python module to parse [Dotclear](https://dotclear.org/) backup files (like `2024-01-07-11-22-dotclear-backup.txt`).

## Note

As there are no format specification for dotclear backup format, there is no way to "validate" parsed data are correct. Please always check your data.

## Example

You load the backup content in a `parser` object:

```python
import dotclear_backup_parser

# Load dotclear backup content.
with open("2024-01-07-11-22-dotclear-backup.txt") as fp:
    parser = dotclear_backup_parser.load(fp)
```

Then you can iterate over tables found in the backup file: 

```python
for table in parser:
    
    print(table.name, len(table.rows))
    
    for column_name in table.column_names:
        
        print(f"  {column_name}")
```

Tables are `DcBackupTable` object having three properties:

* name (`str`): Table name.
* column_names (`list[str]`): Name of the columns of the table.
* rows (`list[list[str]]`): List of rows, each row is a list of value (same length as `column_names`).

Read the source for more information.
