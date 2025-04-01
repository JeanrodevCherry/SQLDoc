import os
import sys
import sqlparse
from sqlparse.tokens import Keyword, DDL, Name
from sqlparse.sql import Identifier, IdentifierList, Parenthesis
import pdb
import re


class SQLParser:
    """Parser for the .sql file"""

    def __init__(self, filename):
        """Directly parse the file on __init__"""
        self.filename = filename
        self.parsed_sql = self._parse_sql(filename)

    def _parse_sql(self, filename):
        """Parse the file here"""
        with open(filename, "r") as opened_file:
            buff_ = opened_file.read()
            return sqlparse.parse(buff_)

    def to_markdown(self):
        """Handle conversion to markdown"""
        lines = []
        # lines.append("```mermaid")
        # lines.append("erDiagram")
        for elem in self.parsed_sql:
            table_name, attributes = self._parse_statement(elem)
            lines.append(f"# {table_name}")
            for attrib in attributes:
                lines.append(f"## {attrib}")
        # lines.append("````")
        return lines

    def _parse_statement(self, element):
        if element.get_type() == "CREATE":
            table_name = None
            columns = []
            table_seen = False
            for token in element.tokens:
                if token.ttype is Keyword and token.value.upper() == "TABLE":
                    # found "TABLE"
                    table_seen = True
                    continue
                if table_seen and isinstance(token, Identifier):
                    # We should have the table name
                    table_name = token.get_name()
                    table_seen = False  # reset
            for token in element.tokens:
                if isinstance(token, Parenthesis):
                    # This should hold something like (col1 INT, col2 VARCHAR(100), ...)
                    # Let's parse the contents
                    columns_block = (
                        token.value
                    )  # e.g. "(col1 INT, col2 VARCHAR(100), ...)"
                    # remove parentheses
                    inner = columns_block.strip()[1:-1].strip()
                    col_statements = sqlparse.parse(inner)
                    raw_cols = _split_on_top_level_commas(inner)
                    for col_def in raw_cols:
                        col_def = col_def.strip()
                        # Possibly parse foreign key lines, constraints, etc.
                        # For a simple column:
                        columns.append(col_def)
                    break  # we found the column block

            # return {"table_name": table_name, "columns": columns}
            return table_name, columns

    def __str__(self):
        return str(self.to_markdown())


def _split_on_top_level_commas(text):
    """
    Splits a string on commas that are not nested inside parentheses.
    E.g. "col1 INT, col2 VARCHAR(100), FOREIGN KEY (x) REFERENCES ..."
    => ["col1 INT", "col2 VARCHAR(100)", "FOREIGN KEY (x) REFERENCES ..."]
    """
    parts = []
    start = 0
    depth = 0
    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(text[start:i])
            start = i + 1
    parts.append(text[start:])
    return parts
