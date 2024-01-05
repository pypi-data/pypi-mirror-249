# Copyright UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import pyarrow

from ...schema.models.tasks import classification
from ..outputs import FieldFormatError, OutputSpecification


class Classification(OutputSpecification):
    def __init__(self, task: classification.Classification):
        if not isinstance(task, classification.Classification):
            raise TypeError(
                f"'task' must be of type classification.Classification; got {type(task)}"
            )
        super().__init__(task)

    def _fields(self):
        return [pyarrow.field("label", pyarrow.string())]


class Ranking(OutputSpecification):
    def __init__(self, task: classification.Classification):
        if not isinstance(task, classification.Classification):
            raise TypeError(
                f"'task' must be of type classification.Classification; got {type(task)}"
            )
        super().__init__(task)

    def _fields(self):
        return [pyarrow.field("label", pyarrow.list_(pyarrow.string()))]

    def verify_output(self, item):
        super().verify_output(item)
        try:
            if len(item["label"]) != self.task.numLabels:
                raise FieldFormatError(
                    f"field 'label' should have len() == task.numLabels ({self.task.numLabels})"
                )
        except TypeError:
            raise FieldFormatError(
                f"field 'label' should have len() == task.numLabels ({self.task.numLabels})"
            )


class Scores(OutputSpecification):
    def __init__(self, task: classification.Classification):
        if not isinstance(task, classification.Classification):
            raise TypeError(
                f"'task' must be of type classification.Classification; got {type(task)}"
            )
        super().__init__(task)

    def _fields(self):
        return [
            pyarrow.field("label", pyarrow.list_(pyarrow.string())),
            pyarrow.field("score", pyarrow.list_(pyarrow.float32())),
        ]

    def verify_output(self, item):
        super().verify_output(item)
        try:
            if len(item["label"]) != self.task.numLabels:
                raise FieldFormatError(
                    f"field 'label' should have len() == task.numLabels ({self.task.numLabels})"
                )
        except TypeError:
            raise FieldFormatError(
                f"field 'label' should have len() == task.numLabels ({self.task.numLabels})"
            )
        try:
            if len(item["score"]) != self.task.numLabels:
                raise FieldFormatError(
                    f"field 'score' should have len() == task.numLabels ({self.task.numLabels})"
                )
        except TypeError:
            raise FieldFormatError(
                f"field 'score' should have len() == task.numLabels ({self.task.numLabels})"
            )
