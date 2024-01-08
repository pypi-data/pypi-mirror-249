"""Dotclear backup parser module.

Dotclear backup parser allow Python developers to parse data from dotclear
backup files (like 2024-01-07-11-22-dotclear-backup.txt) in a manageable object.

Please note that as there are no format specification for dotclear backup
format, there is no way to "validate" parsed data are correct. Please always
check your data.

Dotclear backup files looks like this:

///DOTCLEAR|2.28.1|full

[table_name column1,column2,column3,column4]
"column 1 value","column 2 value","column 3 value","column 4 value"
"column 1 value","column 2 value","column 3 value","column 4 value"
...

Example:
    >>> import dotclear_backup_parser
    >>> with open("2024-01-07-11-22-dotclear-backup.txt") as fp:
    ...     parser = dotclear_backup_parser.load(fp)
    >>> for table in parser:
    ...     print(table.name)
"""
from __future__ import annotations

__version__ = "0.0.1"

import dataclasses
import io
import re
from typing import TextIO

# Dotclear backup header
dc_version_re = re.compile(
    r"^///DOTCLEAR\|(?P<dc_version>[^|]+)\|(?P<backup_type>.+)\n$")

# Table header [name column1,column2,column3]
table_header_re = re.compile(
    r"^\[(?P<table_name>[^ ]+) (?P<columns>[a-z_,]+)]$")

# '"foo", "bar", "truc"' -> ("foo", "bar", "truc")
table_row_sep_re = re.compile(r'"(?P<content>.*?)(?<!\\)"+')


@dataclasses.dataclass
class DcBackupTable:
    """Class representing a table parsed from a Dotclear backup file."""
    name: str
    column_names: list[str]
    rows: list[list[str]]

    def add_rows(self, columns: list[str]):
        """Add given column values as next row.

        Args:
            columns (list[str]): Column values.
        """
        if len(columns) != len(self.column_names):
            msg = ("inconsistent list size between given row and table column "
                   "names")
            raise ValueError(msg)

        self.rows.append(columns)


class DcBackupParser:
    """Main parser class."""
    def __init__(self):
        """Initialize main parser class."""
        self.dc_version: str | None = None
        self.backup_type: str | None = None
        self._cur_table: DcBackupTable | None = None
        self.tables: list[DcBackupTable] = []

    def __iter__(self):
        """Expose tables property in the class iterator for easiness."""
        yield from self.tables

    def table_has_begin(self) -> bool:
        """Return if table parsing has started.

        Returns:
            bool: True if table parsing has started.
        """
        return self._cur_table is not None

    def table_begin(self, name: str, column_names: list[str]):
        """Start a table parsing.

        All rows created after this must have the same size as `column_names`.

        Args:
            name (str): Table name.
            column_names (list[str]): Column names.
        """
        self._cur_table = DcBackupTable(name, column_names, [])

    def add_rows(self, columns: list[str]):
        """Add given column values as a new row in currently parsed table.

        Args:
            columns (list[str]): Column values.

        Raises:
            ValueError: If given column size does not match table column size.
        """
        self._cur_table.add_rows(columns)

    def table_end(self):
        """End current table parsing."""
        self.tables.append(self._cur_table)
        self._cur_table = None

    def load(self, fp: TextIO):
        """Load given Dotclear backup file from its given file descriptor."""
        for line in fp.readlines():
            self._parse_line(line)

    def loads(self, s: str):
        """Load given Dotclear backup file from given string."""
        buf = io.StringIO(s)
        for line in buf.readlines():
            self._parse_line(line)

    def _parse_line(self, line: str):
        """Internal function to parse given line."""
        if match_grp := dc_version_re.match(line):
            self.dc_version = match_grp.group("dc_version")
            self.backup_type = match_grp.group("backup_type")
            return

        if match_grp := table_header_re.match(line):
            name = match_grp.group("table_name")
            column_names = match_grp.group("columns").split(",")
            self.table_begin(name, column_names)
            return

        if self.table_has_begin():
            if line == "\n":
                self.table_end()  # Empty line means table end.
            else:
                columns = []
                for match_grp in table_row_sep_re.finditer(line):
                    content = match_grp.group("content")
                    content = content.replace(r'\"', '"')
                    columns.append(content)
                self.add_rows(columns)
            return


def load(fp: TextIO) -> DcBackupParser:
    """Load given Dotclear backup file from its given file descriptor.

    Args:
        fp (TextIO): A textual file descriptor.

    Returns:
        DcBackupParser: Parsed object containing tables.
    """
    parser = DcBackupParser()

    parser.load(fp)

    return parser
