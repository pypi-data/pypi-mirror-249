import io
import os
import unittest
from json import load
from pathlib import Path

import pandas as pd

from lumipy.provider import PandasProvider


class TestPandasProviders(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        file_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = Path(file_dir + '/../../data/context_examples')
        cls.data_dir = data_dir

        cls.iris = PandasProvider('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv', 'iris')
        cls.titanic = PandasProvider('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv', 'titanic')

        prices_df = pd.read_csv(data_dir / '..' / 'prices.csv')
        prices_df['Date'] = pd.to_datetime(prices_df.Date).dt.tz_localize(tz='utc')
        cls.prices = PandasProvider(prices_df, 'prices')

    def get_req(self, name):
        ctx_path = self.data_dir / f'{name}.json'
        with open(ctx_path, 'r') as f:
            req = load(f)
            req['param_specs']['UsePandasFilter']['value'] = True
            return req

    def get_exp(self, name):
        csv_path = self.data_dir / f'{name}.csv'
        return pd.read_csv(csv_path)

    def assertDataMatchesExpected(self, prov, name, is_agg, is_ord, is_offset):
        exp_df = self.get_exp(name)
        if 'Date' in exp_df.columns:
            exp_df['Date'] = pd.to_datetime(exp_df.Date).dt.tz_localize(tz='utc')

        req = self.get_req(name)

        lines = list(prov._pipeline(req))

        cols = [c for c in prov.columns]
        exp_df = exp_df[cols]

        cols += ['LineType', 'Message']

        sig_csv = io.StringIO('\n'.join(lines[:3]))
        sig_df = pd.read_csv(sig_csv, names=cols, header=None).iloc[:, -2:].set_index('LineType')
        self.assertEqual(is_agg, sig_df.loc['is_agg'].Message)
        self.assertEqual(is_ord, sig_df.loc['is_ord'].Message)
        self.assertEqual(is_offset, sig_df.loc['is_offset'].Message)

        obs_csv = io.StringIO(lines[3])
        obs_df = pd.read_csv(obs_csv, names=cols, header=None).iloc[:, :-2]

        self.assertSequenceEqual(exp_df.shape, obs_df.shape)

        compare = exp_df.fillna('NA') == obs_df.fillna('NA')
        self.assertTrue(compare.all().all())

    def test_iris_no_filter(self):
        self.assertDataMatchesExpected(self.iris, 'test_iris_no_filter', False, False, False)

    def test_iris_no_filter_limit(self):
        self.assertDataMatchesExpected(self.iris, 'test_iris_no_filter_limit', False, False, False)

    def test_iris_no_filter_limit_offset(self):
        self.assertDataMatchesExpected(self.iris, 'test_iris_no_filter_limit_offset', False, False, True)

    def test_iris_join_filter(self):
        self.assertDataMatchesExpected(self.iris, 'test_iris_join_filter', False, False, False)

    def test_titanic_op_and(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_and', False, False, False)

    def test_titanic_op_or(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_or', False, False, False)

    def test_titanic_op_concat(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_concat', False, False, False)

    def test_titanic_op_eq(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_eq', False, False, False)

    def test_titanic_op_glob(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_glob', False, False, False)

    def test_titanic_op_gt(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_gt', False, False, False)

    def test_titanic_op_gte(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_gte', False, False, False)

    def test_titanic_op_in(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_in', False, False, False)

    def test_titanic_op_is_between(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_is_between', False, False, False)

    def test_titanic_op_is_not_between(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_is_not_between', False, False, False)

    def test_titanic_op_is_not_null(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_is_not_null', False, False, False)

    def test_titanic_op_is_null(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_is_null', False, False, False)

    def test_titanic_op_len(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_len', False, False, False)

    def test_titanic_op_like(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_like', False, False, False)

    def test_titanic_op_lower(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_lower', False, False, False)

    def test_titanic_op_lt(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_lt', False, False, False)

    def test_titanic_op_lte(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_lte', False, False, False)

    def test_titanic_op_neq(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_neq', False, False, False)

    def test_titanic_op_not(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_not', False, False, False)

    def test_titanic_op_not_glob(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_not_glob', False, False, False)

    def test_titanic_op_not_in(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_not_in', False, False, False)

    def test_titanic_op_not_like(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_not_like', False, False, False)

    def test_titanic_op_replace(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_replace', False, False, False)

    def test_titanic_op_substr(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_substr', False, False, False)

    def test_titanic_op_upper(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_op_upper', False, False, False)

    # Boolean column
    def test_titanic_single_bool_column(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_single_bool_column', False, False, False)

    # Numeric functions
    def test_titanic_numeric_abs(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_abs', False, False, False)

    def test_titanic_numeric_add(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_add', False, False, False)

    def test_titanic_numeric_ceil(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_ceil', False, False, False)

    def test_titanic_numeric_exp(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_exp', False, False, False)

    def test_titanic_numeric_floor(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_floor', False, False, False)

    def test_titanic_numeric_flooordiv(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_floordiv', False, False, False)

    def test_titanic_numeric_log(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_log', False, False, False)

    def test_titanic_numeric_log10(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_log10', False, False, False)

    def test_titanic_numeric_mod(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_mod', False, False, False)

    def test_titanic_numeric_multiply(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_multiply', False, False, False)

    def test_titanic_numeric_power(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_power', False, False, False)

    def test_titanic_numeric_round(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_round', False, False, False)

    def test_titanic_numeric_sign(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_sign', False, False, False)

    def test_titanic_numeric_sub(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_sub', False, False, False)

    def test_titanic_numeric_truediv(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_numeric_truediv', False, False, False)

    # Literal values
    def test_titanic_literal_bool(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_literal_bool', False, False, False)

    def test_titanic_literal_float(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_literal_float', False, False, False)

    def test_titanic_literal_int(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_literal_int', False, False, False)

    def test_titanic_literal_list(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_literal_list', False, False, False)

    def test_titanic_literal_str(self):
        self.assertDataMatchesExpected(self.titanic, 'test_titanic_literal_str', False, False, False)

    def test_prices_literal_date(self):
        self.assertDataMatchesExpected(self.prices, 'test_prices_literal_date', False, False, False)

    # Datetime fns
    def test_prices_dt_date_str(self):
        self.assertDataMatchesExpected(self.prices, 'test_prices_dt_date_str', False, False, False)

    def test_prices_dt_day_name(self):
        self.assertDataMatchesExpected(self.prices, 'test_prices_dt_day_name', False, False, False)

    def test_prices_dt_day_of_month(self):
        self.assertDataMatchesExpected(self.prices, 'test_prices_dt_day_of_month', False, False, False)

    def test_prices_dt_day_of_week(self):
        self.assertDataMatchesExpected(self.prices, 'test_prices_dt_day_of_week', False, False, False)

    def test_prices_dt_day_of_year(self):
        self.assertDataMatchesExpected(self.prices, 'test_prices_dt_day_of_year', False, False, False)

    def test_prices_dt_julian_day(self):
        self.assertDataMatchesExpected(self.prices, 'test_prices_dt_julian_day', False, False, False)
