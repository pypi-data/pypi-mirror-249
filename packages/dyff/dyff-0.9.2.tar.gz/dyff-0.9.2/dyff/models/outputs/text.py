# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import pyarrow

from ...schema.models.tasks import classification
from ..outputs import FieldFormatError, OutputSpecification


class TaggedSpans(OutputSpecification):
    def __init__(self, task: classification.Classification):
        if not isinstance(task, classification.Classification):
            raise TypeError(
                f"'task' must be of type classification.Classification; got {type(task)}"
            )
        super().__init__(task)
        self._label_set = set(self.task.labels)

    def _fields(self):
        return [
            pyarrow.field(
                "spans",
                pyarrow.list_(
                    pyarrow.struct(
                        [
                            pyarrow.field("start", pyarrow.int64()),
                            pyarrow.field("end", pyarrow.int64()),
                            pyarrow.field("tag", pyarrow.string()),
                        ]
                    )
                ),
            )
        ]

    def verify_output(self, item):
        super().verify_output(item)
        try:
            for span in item["spans"]:
                if span["tag"] not in self._label_set:
                    raise FieldFormatError(
                        f"field 'tag' has invalid value {span['tag']}"
                    )
                start = int(span["start"])
                end = int(span["end"])
                if not (0 <= start < end):
                    raise FieldFormatError(
                        f"[start, end) [{start}, {end}) is not a valid interval"
                    )
        except ValueError as ex:
            raise FieldFormatError(
                "[start, end) interval not convertible to int()"
            ) from ex
