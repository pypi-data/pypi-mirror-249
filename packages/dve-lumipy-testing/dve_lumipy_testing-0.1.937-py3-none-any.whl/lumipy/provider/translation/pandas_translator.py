import warnings
from typing import Union

from pandas import DataFrame, Series, merge

from lumipy.common import table_spec_to_df
from lumipy.provider.context import Expression
from lumipy.provider.translation.pandas_map import pandas_map


class PandasTranslator:

    @staticmethod
    def _restriction_table(df, meta, content):
        # Parse restriction table into a dataframe and then build a filter for which columns pass
        res_df = table_spec_to_df(meta, content)
        on_cols = res_df.columns.tolist()
        merge_df = merge(df, res_df, how='left', on=on_cols, indicator=True)
        return merge_df['_merge'] == 'both'

    @staticmethod
    def _col_value(df, x):
        # If column isn't present, return None for partial filter application
        return df[x] if x in df.columns else None

    def __init__(self, context):
        self._context = context
        self.full_where = None
        self.agg_applied = False
        self.full_order = None

    def translate_expression(self, df):

        self.full_where = True

        def translate(ex: Expression) -> Union[Series, None, float, str, bool]:

            if ex.op == 'ColValue':
                fn = lambda x: self._col_value(df, x)
            elif ex.op == 'RestrictionTable':
                fn = lambda x: self._restriction_table(df, *x)
            elif ex.op in pandas_map:
                fn = pandas_map[ex.op]
            else:
                # Otherwise, can't be translated. Set value to None so the associated bit of the filter isn't applied.
                warnings.warn(f'No mapping for op={ex.op}')
                return None

            inputs = [a if ex.is_leaf() else translate(a) for a in ex.args]

            # Handle partial application here...
            is_partial = any(i is None for i in inputs)
            if not is_partial:
                return fn(*inputs)

            # flip the flag if filter is partially applied
            self.full_where = False

            if ex.is_logic_op():
                # if it's a logic function return all True
                return Series([True] * df.shape[0])
            else:
                # if it's any other return None
                return None

        if self._context.where_clause is not None:
            return translate(self._context.where_clause).fillna(False)

        return None

    def apply_where(self, df):
        where_filter = self.translate_expression(df)
        if where_filter is None:
            return df
        return df[where_filter]

    def apply_limit(self, df):

        lim = self._context.limit_clause

        lower = lim.offset if lim.offset else 0
        upper = lim.limit + lower if lim.limit else None

        if not lim.has_requirements():
            self._context.is_offset = lower > 0
            return df.iloc[lower:upper]
        elif lim.requires_filter_only() and self.full_where:
            self._context.is_offset = lower > 0
            return df.iloc[lower:upper]
        elif lim.requires_filter_and_order() and self.full_where and self.full_order:
            self._context.is_offset = lower > 0
            return df.iloc[lower:upper]

        return df

    def apply_aggregation(self, df):
        # todo: implement
        return df

    def apply_ordering(self, df):
        # todo: implement
        return df

    def apply(self, df, yield_mode=False) -> DataFrame:

        df = self.apply_where(df)

        if not yield_mode:
            df = self.apply_aggregation(df)
            df = self.apply_ordering(df)
            df = self.apply_limit(df)

        return df
