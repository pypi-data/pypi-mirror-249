#     Copyright 2023, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Nodes for match statement for Python3.10+ """

from .ChildrenHavingMixins import ChildHavingExpressionMixin
from .ExpressionBases import ExpressionBase
from .ExpressionShapeMixins import ExpressionTupleShapeExactMixin


class ExpressionMatchArgs(
    ExpressionTupleShapeExactMixin, ChildHavingExpressionMixin, ExpressionBase
):
    kind = "EXPRESSION_MATCH_ARGS"

    named_children = ("expression",)

    __slots__ = ("max_allowed",)

    def __init__(self, expression, max_allowed, source_ref):
        ChildHavingExpressionMixin.__init__(self, expression=expression)

        ExpressionBase.__init__(self, source_ref)

        self.max_allowed = max_allowed

    def computeExpression(self, trace_collection):
        # TODO: May know that match args doesn't raise from the shape of
        # the matches expression, most don't.

        trace_collection.onExceptionRaiseExit(BaseException)

        return self, None, None
