from __future__ import annotations

from distutils.util import strtobool
from typing import Dict, Any, Union, Literal, List

from pandas import to_datetime
from pydantic import BaseModel, StrictStr, StrictBool

from lumipy.common import table_spec_to_df
from lumipy.provider.common import expression_to_table_spec


class Expression(BaseModel):

    op: StrictStr
    args: List[Union[Expression, str, int, bool, float]]

    def is_leaf(self):
        return self.op in ['ColValue', 'DateValue', 'BoolValue', 'StrValue', 'NumValue', 'TableSpec']

    def is_logic_op(self):
        return self.op in [
            'And', 'Or',
            'Gt', 'Lt', 'Gte', 'Lte',
            'Eq', 'Neq',
            'In', 'NotIn',
            'Between', 'NotBetween',
            'Like', 'NotLike', 'Glob', 'NotGlob',
            'Regexp', 'NotRegexp',
        ]

    def __str__(self):
        return self.json(indent=2)

    def __repr__(self):
        return str(self)


class ParamVal(BaseModel):

    name: StrictStr
    data_type: StrictStr
    value: Union[Expression, str]

    def get(self):

        if self.data_type == 'Table':
            args = expression_to_table_spec(*self.value.args)
            return table_spec_to_df(*args)

        from lumipy.provider import DType

        t = DType[self.data_type]

        if t == DType.Int:
            return int(self.value)
        if t == DType.Double:
            return float(self.value)
        if t == DType.Text:
            return str(self.value)
        if t == DType.Boolean:
            return bool(strtobool(str(self.value)))
        if t == DType.DateTime or t == DType.Date:
            return to_datetime(self.value, errors='coerce')

        return self.value

    def __str__(self):
        return self.json(indent=2)

    def __repr__(self):
        return str(self)


class Limit(BaseModel):

    limit: Union[int, None] = None
    offset: Union[int, None] = None
    limitType: Literal['NoFilteringRequired', 'FilteringRequired', 'FilteringAndOrderingRequired'] = 'NoFilteringRequired'

    def requires_filter_only(self):
        return self.limitType == 'FilteringRequired'

    def requires_filter_and_order(self):
        return self.limitType == 'FilteringAndOrderingRequired'

    def has_requirements(self):
        return self.requires_filter_only() or self.requires_filter_and_order()

    def __str__(self):
        return self.json(indent=2)

    def __repr__(self):
        return str(self)


class Context(BaseModel):

    where_clause: Union[Expression, None]
    param_specs: Dict[StrictStr, ParamVal] = {}
    limit_clause: Limit = Limit()

    is_agg: StrictBool = False
    is_ordered: StrictBool = False
    is_offset: StrictBool = False

    def get(self, name) -> Any:
        if name in self.param_specs:
            return self.param_specs[name].get()
        return None

    @property
    def pandas(self):
        from lumipy.provider.translation.pandas_translator import PandasTranslator
        return PandasTranslator(self)

    def limit(self):
        return self.limit_clause.limit

    def offset(self):
        return self.limit_clause.offset

    def __str__(self):
        return self.json(indent=2)

    def __repr__(self):
        return str(self)
