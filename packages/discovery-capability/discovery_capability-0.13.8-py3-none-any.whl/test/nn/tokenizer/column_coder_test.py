import unittest
import os
from pathlib import Path
import shutil
import ast
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from ds_capability.nn.tokenizers.column_coder import ColumnCodes
from ds_core.properties.property_manager import PropertyManager
from ds_capability import *
from ds_capability.components.commons import Commons

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class TemplateTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # clean out any old environments
        for key in os.environ.keys():
            if key.startswith('HADRON'):
                del os.environ[key]
        # Local Domain Contract
        os.environ['HADRON_PM_PATH'] = os.path.join('working', 'contracts')
        os.environ['HADRON_PM_TYPE'] = 'parquet'
        # Local Connectivity
        os.environ['HADRON_DEFAULT_PATH'] = Path('working/data').as_posix()
        # Specialist Component
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
        except OSError:
            pass
        try:
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except OSError:
            pass
        try:
            shutil.copytree('../_test_data', os.path.join(os.environ['PWD'], 'working/source'))
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_for_smoke(self):
        fe = FeatureEngineer.from_memory()
        tbl = fe.tools.get_synthetic_data_types(10)
        self.assertEqual((10, 6), tbl.shape)

    def test_column_coder(self):
        raw = [[0,134.09,'3527213246127876953','La Verne','CA',91750], [0,38.43,'-727612092139916043','Monterey Park','CA',91754]]
        all_columns = ['User', 'Amount', 'Merchant Name', 'Merchant City', 'Merchant State', 'Zip']
        df = pd.DataFrame(raw,columns=all_columns)

        # these are the columns used to train the model
        columns = ['Amount', 'Merchant Name', 'Merchant City', 'Merchant State', 'Zip']
        float_columns = ['Amount']
        category_columns = ['Merchant Name', 'Merchant City', 'Merchant State']
        integer_columns = ['Zip']

        tab_structure = []
        for c in columns:
            if c in float_columns:
                item = {
                    "name": c,
                    "code_type": "float",
                    "args": {
                        "code_len": 3,  # number of tokens used to code the column
                        "base": 32,  # the positional base number. ie. it uses 32 tokens for one digit
                        "fillall": True,  # whether to use full base number for each token or derive it from the data.
                        "hasnan": False,  # can it handles nan or not
                        "transform": "yeo-johnson"
                        # can be ['yeo-johnson', 'quantile', 'robust'], check https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing
                    }
                }
            elif c in integer_columns:
                item = {
                    "name": c,
                    "code_type": "int",
                    "args": {
                        "code_len": 3,  # number of tokens used to code the column
                        "base": 47,  # the positional base number. ie. it uses 32 tokens for one digit
                        "fillall": True,  # whether to use full base number for each token or derive it from the data.
                        "hasnan": True,  # can it handles nan or not
                    }
                }
            else:
                item = {
                    "name": c,
                    "code_type": "category",
                }
            tab_structure.append(item)
        # print(OmegaConf.to_yaml(tab_structure))
        # print(columns)

        example_arrays = {}
        for col in tab_structure:
            col_name = col['name']
            if col_name in category_columns:
                example_arrays[col_name] = [i.strip() for i in df[col_name].astype(str).unique()]
            else:
                example_arrays[col_name] = df[col_name].dropna().unique()
        cc = ColumnCodes.get_column_codes(tab_structure, example_arrays)
        print(cc)

    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")


def tprint(t: pa.table, headers: [str, list] = None, d_type: [str, list] = None, regex: [str, list] = None):
    _ = Commons.filter_columns(t.slice(0, 10), headers=headers, d_types=d_type, regex=regex)
    print(Commons.table_report(_).to_string())


if __name__ == '__main__':
    unittest.main()
