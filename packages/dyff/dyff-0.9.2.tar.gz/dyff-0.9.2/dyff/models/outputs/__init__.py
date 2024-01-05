# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import List

import pyarrow

__all__ = [
    "TaskOutputError",
    "MissingFieldsError",
    "FieldFormatError",
    "OutputSpecification",
]


class TaskOutputError(Exception):
    pass


class MissingFieldsError(TaskOutputError):
    pass


class FieldFormatError(TaskOutputError):
    pass


class OutputSpecification:
    """Note: Implementations need to be thread-safe"""

    def __init__(self, task):
        self.__task = task
        fields = [pyarrow.field("_index_", pyarrow.int64())]
        fields.extend(self._fields())
        unique_names = set()
        duplicates = set()
        for f in fields:
            if f.name in unique_names:
                duplicates.add(f.name)
            else:
                unique_names.add(f.name)
        if len(duplicates) > 0:
            raise ValueError(f"duplicate field names: {duplicates}")
        self.__schema = pyarrow.schema(fields)
        self.__required_fields = frozenset(self.__schema.names)

    @abc.abstractmethod
    def _fields(self) -> List[pyarrow.Field]:
        raise NotImplementedError()

    @property
    def schema(self) -> pyarrow.Schema:
        return self.__schema

    @property
    def task(self):
        return self.__task

    def verify_output(self, item) -> None:
        missing = self.__required_fields.difference(item.keys())
        if len(missing) > 0:
            raise MissingFieldsError(missing)
