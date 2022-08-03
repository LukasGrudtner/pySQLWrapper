from __future__ import annotations
import datetime


class PostgreSQLWrapper:
    def __init__(self) -> None:
        self._query = None

    def insert_into(self, table: str, columns: list, values: list) -> PostgreSQLWrapper:
        self._query = f'INSERT INTO {table} ({format_columns(columns)}) VALUES ({format_values(values)})'
        return self

    def update(self, table: str) -> PostgreSQLWrapper:
        self._query = f'UPDATE {table}'
        return self

    def set(self, columns: list, values: list) -> PostgreSQLWrapper:
        assert len(columns) == len(values)
        self._query += f' SET ' + format_set_values(columns, values)

        return self

    def returning(self, column: str) -> PostgreSQLWrapper:
        self._query += f' RETURNING {column}'
        return self

    def on_conflict(self, columns: list) -> PostgreSQLWrapper:
        self._query += f' ON CONFLICT ({format_columns(columns)})'
        return self

    def do_nothing(self) -> PostgreSQLWrapper:
        self._query += ' DO NOTHING'
        return self

    def do_update(self, column: str, value: object) -> PostgreSQLWrapper:
        self._query += f' DO UPDATE SET {column} = {format_single_value(value)}'
        return self

    def select(self, columns: list) -> PostgreSQLWrapper:
        if self._query is not None:
            self._query += f' SELECT {format_columns(columns)}'
        else:
            self._query = f'SELECT {format_columns(columns)}'
        return self

    def select_distinct(self, columns: list) -> PostgreSQLWrapper:
        if self._query is not None:
            self._query += f' SELECT DISTINCT {format_columns(columns)}'
        else:
            self._query = f'SELECT DISTINCT {format_columns(columns)}'
        return self

    def from_(self, source: str) -> PostgreSQLWrapper:
        self._query += f' FROM ({source})'
        return self

    def as_(self, label: str) -> PostgreSQLWrapper:
        self._query += f' AS {label}'
        return self

    def delete_from(self, table: str) -> PostgreSQLWrapper:
        self._query = f'DELETE FROM {table}'
        return self

    def join(self, table: str) -> PostgreSQLWrapper:
        self._query += f' JOIN ({table})'
        return self

    def inner_join(self, table: str) -> PostgreSQLWrapper:
        self._query += f' INNER JOIN ({table})'
        return self

    def left_join(self, table: str, label: str = None) -> PostgreSQLWrapper:
        self._query += f' LEFT JOIN ({table})'
        if label:
            self._query += f' {label}'
        return self

    def right_join(self, table: str) -> PostgreSQLWrapper:
        self._query += f' RIGHT JOIN ({table})'
        return self

    def full_join(self, table: str) -> PostgreSQLWrapper:
        self._query += f' FULL JOIN ({table})'
        return self

    def full_outer_join(self, table: str) -> PostgreSQLWrapper:
        self._query += f' FULL OUTER JOIN ({table})'
        return self

    def lateral_join(self, source: str) -> PostgreSQLWrapper:
        self._query += f', LATERAL {source}'
        return self

    def union(self, table: str) -> PostgreSQLWrapper:
        self._query += f' UNION ({table})'
        return self

    def union_all(self, table: str) -> PostgreSQLWrapper:
        self._query += f' UNION ALL ({table})'
        return self

    def on(self, expression: str) -> PostgreSQLWrapper:
        self._query += f' ON ({expression})'
        return self

    def eq(self, column: str) -> PostgreSQLWrapper:
        self._query += f' = {column}'
        return self

    def using(self, columns: list) -> PostgreSQLWrapper:
        self._query += f' USING ({", ".join(columns)})'
        return self

    def where(self, conditions: list) -> PostgreSQLWrapper:
        if len(conditions) == 0:
            return self

        self._query += f' WHERE {format_conditions(conditions, " AND ")}'
        return self

    def order_by(self, column: str) -> PostgreSQLWrapper:
        self._query += f' ORDER BY {column}'
        return self

    def asc(self) -> PostgreSQLWrapper:
        self._query += ' ASC'
        return self

    def desc(self) -> PostgreSQLWrapper:
        self._query += ' DESC'
        return self

    def limit(self, limit: int) -> PostgreSQLWrapper:
        self._query += f' LIMIT {str(limit)}'
        return self

    def truncate(self, table: str) -> PostgreSQLWrapper:
        self._query = f'TRUNCATE {table}'
        return self

    def cascade(self) -> PostgreSQLWrapper:
        self._query += ' CASCADE'
        return self

    def with_(self, name: str, subquery: PostgreSQLWrapper) -> PostgreSQLWrapper:
        self._query = f'WITH {name} AS ({subquery.build()})'
        return self

    def group_by(self, columns: list) -> PostgreSQLWrapper:
        self._query += f'GROUP BY {format_columns(columns)}'
        return self

    def build(self) -> str:
        return self._query

    @staticmethod
    def equals(column: str, value: object) -> str:
        return f'{column} = {format_single_value(value)}'

    @staticmethod
    def equals_expression(column: str, value: object) -> str:
        return f'{column} = {value}'

    @staticmethod
    def not_equals(column: str, value: object) -> str:
        return f'{column} <> {format_single_value(value)}'

    @staticmethod
    def greater_than(column: str, value: object) -> str:
        return f'{column} > {format_single_value(value)}'

    @staticmethod
    def greater_or_equal(column: str, value: object) -> str:
        return f'{column} >= {format_single_value(value)}'

    @staticmethod
    def less_than(column: str, value: object) -> str:
        return f'{column} < {format_single_value(value)}'

    @staticmethod
    def less_or_equal(column: str, value: object) -> str:
        return f'{column} <= {format_single_value(value)}'

    @staticmethod
    def count(table: str, column: str) -> str:
        return f'count({table}.{column})'

    @staticmethod
    def _in(column: str, values: list) -> str:
        return f'{column} IN ({format_values(values)})'

    @staticmethod
    def as__(column: str, label: str) -> str:
        return f'{column} AS {label}'

    @staticmethod
    def is_null(column: str) -> str:
        return f'{column} IS NULL'

    @staticmethod
    def is_not_null(column: str) -> str:
        return f'{column} IS NOT NULL'


def format_conditions(conditions: list, separator: str) -> str:
    return separator.join(str(condition) for condition in conditions)


def format_columns(columns: list) -> str:
    separator = ', '
    return separator.join(str(column) for column in columns)


def format_values(values: list) -> str:
    separator = ', '
    return separator.join(format_single_value(value) for value in values)


def format_set_values(columns: list, values: list) -> str:
    assert len(columns) == len(values)
    separator = ', '

    operations = list()
    for (column, value) in zip(columns, values):
        operations.append(f'{column} = {format_single_value(value)}')

    return separator.join(operations)


def format_single_value(value: object) -> str:
    if isinstance(value, str):
        return f'\'{value}\''
    elif isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
        return f'\'{str(value)}\''
    elif isinstance(value, bool):
        return f'\'{str(value).lower()}\''
    elif isinstance(value, list):
        if len(value):
            return f'ARRAY {value}'
        else:
            return 'null'
    elif value is None:
        return 'null'
    return str(value)
