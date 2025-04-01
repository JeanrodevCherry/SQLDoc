import os
import sys
import sqlparse
from sqlparse.tokens import Keyword, DDL, Name
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
        lines = []
        # lines.append("```mermaid")
        # lines.append("erDiagram")
        for elem in self.parsed_sql:
            table_name, attributes = self._parse_statement(elem)
            lines.append(f"# {table_name}")
            lines.append(f"## {attributes}")
        # lines.append("````")
        return lines

    def _parse_statement(self, element):
        # search_ = re.search(r"CREATE TABLE (.*) \(.*\", element.value)
        pattern = re.compile(
            r"(?i)"  # case-insensitive
            r"CREATE\s+TABLE\s+"
            r"([^\s(]+)"  # capture the table name
            r"\s*\(\s*"
            r"([^)]*)"  # capture everything until the last ')'
            r"\)\s*;?"
        )
        search_ = pattern.search(element.value)
        # pdb.set_trace()
        table_name = search_.group(1)
        attributes = search_.group(2)

        return (table_name, attributes)

    def __str__(self):
        return str(self.to_markdown())
