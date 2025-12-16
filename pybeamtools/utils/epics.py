import os
from pathlib import Path

import re
from typing import List, Dict, Optional, Any, Generator
from dataclasses import dataclass, field as dfield


# --- Data Structures ---

@dataclass
class EpicsField:
    name: str
    value: str


@dataclass
class EpicsRecord:
    type: str
    name: str
    fields: Dict[str, str] = dfield(default_factory=dict)
    infos: Dict[str, str] = dfield(default_factory=dict)
    aliases: List[str] = dfield(default_factory=list)

    def __repr__(self):
        return f"<Record {self.type}('{self.name}') fields={len(self.fields)}>"


# --- Tokenizer ---

class Token:
    def __init__(self, type_: str, value: str, line: int):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line})"


def tokenize(text: str) -> Generator[Token, None, None]:
    token_specs = [
        ('COMMENT', r'#.*'),
        ('STRING', r'"(?:\\.|[^"\\])*"'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('COMMA', r','),
        # NEW WORD REGEX:
        # Matches a sequence of:
        # 1. Standard identifier chars (alphanumeric, _, :, -, ., etc)
        # 2. OR a Macro block like $(...)
        # This ensures 'record(' splits, but '$(P):Rec' stays together.
        ('WORD', r'(?:[a-zA-Z0-9_\-\:\.\[\]<>\+]|\$\([^\)]*\))+'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
    line_num = 1

    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            continue
        elif kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character {value!r} on line {line_num}')
        else:
            if kind == 'STRING':
                value = value[1:-1].replace(r'\"', '"')
            yield Token(kind, value, line_num)

    yield Token('EOF', '', line_num)

# Reuse the data structures (EpicsRecord, EpicsField, Token) and tokenize()
# from the previous step. (Assuming they are imported or defined above)

class EpicsDbParser:
    def __init__(self, include_paths: List[str] = None):
        self.tokens = []
        self.pos = 0
        self.records = []
        self.aliases = []
        # Convert all paths to Path objects for consistency
        self.include_paths = [Path(p) for p in (include_paths or [])]
        self.include_paths.append(Path("."))  # Always search current dir

    def parse(self, text: str, filename: str = "<string>") -> List[EpicsRecord]:
        self.tokens = list(tokenize(text))
        self.pos = 0
        self.records = []
        self.aliases = []

        while self.current().type != 'EOF':
            self._parse_top_level()

        return self.records

    # ... [Same current() and consume() methods as before] ...
    def current(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, expected_type: Optional[str] = None) -> Token:
        token = self.current()
        if expected_type and token.type != expected_type:
            # Just raise error, simplified for brevity
            raise SyntaxError(f"Expected {expected_type}, got {token.type} line {token.line}")
        self.pos += 1
        return token

    def _parse_top_level(self):
        token = self.current()
        if token.type == 'WORD':
            if token.value == 'record':
                self._parse_record()
            elif token.value == 'alias':
                self._parse_alias(global_scope=True)
            elif token.value == 'include':
                self._handle_include()
            elif token.value in ('menu', 'info'):
                self._skip_statement()
            else:
                self.consume()  # Skip unknown/macros
        else:
            self.consume()

    def _handle_include(self):
        self.consume('WORD')  # 'include'
        # The filename token (usually quoted STRING)
        filename_token = self.consume()
        filename = filename_token.value

        found_path = self._resolve_file(filename)

        if found_path:
            with open(found_path, 'r') as f:
                content = f.read()

            # Tokenize the included file
            new_tokens = list(tokenize(content))

            # Remove the EOF token from the new list so it doesn't stop the main loop
            if new_tokens and new_tokens[-1].type == 'EOF':
                new_tokens.pop()

            # INJECTION: Splice new tokens into the stream at current position
            # This flattens the include structure immediately.
            self.tokens[self.pos:self.pos] = new_tokens
        else:
            print(f"Warning: Could not resolve include file '{filename}' at line {filename_token.line}")

    def _resolve_file(self, filename: str) -> Optional[Path]:
        # remove quotes if present
        clean_name = filename.strip('"')
        for path in self.include_paths:
            candidate = path / clean_name
            if candidate.is_file():
                return candidate
        return None

    # ... [Include _parse_record, _parse_field, etc. from previous response] ...
    # (Re-paste the previous record parsing methods here for a full class)
    def _parse_record(self):
        self.consume('WORD')
        self.consume('LPAREN')
        rec_type = self.consume().value
        self.consume('COMMA')
        rec_name = self.consume().value
        self.consume('RPAREN')
        record = EpicsRecord(type=rec_type, name=rec_name)
        if self.current().type == 'LBRACE':
            self.consume('LBRACE')
            while self.current().type != 'RBRACE' and self.current().type != 'EOF':
                self._parse_record_body_item(record)
            self.consume('RBRACE')
        self.records.append(record)

    def _parse_record_body_item(self, record: EpicsRecord):
        token = self.current()
        if token.type == 'WORD':
            if token.value == 'field':
                self._parse_field(record)
            elif token.value == 'info':
                self._parse_info(record)
            elif token.value == 'alias':
                self._parse_alias(record=record)
            else:
                self.consume()  # Skip unknown
        else:
            self.consume()

    def _parse_field(self, record: EpicsRecord):
        self.consume('WORD')
        self.consume('LPAREN')
        name = self.consume().value
        self.consume('COMMA')
        value = self.consume().value
        self.consume('RPAREN')
        record.fields[name] = value

    def _parse_info(self, record: EpicsRecord):
        self.consume('WORD')
        self.consume('LPAREN')
        name = self.consume().value
        self.consume('COMMA')
        value = self.consume().value
        self.consume('RPAREN')
        record.infos[name] = value

    def _parse_alias(self, record: Optional[EpicsRecord] = None, global_scope=False):
        self.consume('WORD')
        self.consume('LPAREN')
        if global_scope:
            target = self.consume().value
            self.consume('COMMA')
            alias = self.consume().value
            self.aliases.append((target, alias))
        else:
            alias = self.consume().value
            if record: record.aliases.append(alias)
        self.consume('RPAREN')

    def _skip_statement(self):
        self.consume('WORD')
        self.consume('LPAREN')
        while self.current().type != 'RPAREN' and self.current().type != 'EOF':
            self.consume()
        self.consume('RPAREN')
        if self.current().type == 'LBRACE':
            self.consume('LBRACE')
            while self.current().type != 'RBRACE' and self.current().type != 'EOF':
                self.consume()
            self.consume('RBRACE')