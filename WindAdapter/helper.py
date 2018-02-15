# -*- coding: utf-8 -*-

import datetime
import os

import numpy as np
import pandas as pd
from decouple import config

from WindAdapter.enums import Header
from WindAdapter.enums import OutputFormat

DATA_DICT_PATH = config('DATA_DICT_PATH', default='data_dict.csv')
DATA_DICT_PATH_TYPE_ABS = config('DATA_DICT_PATH_TYPE_ABS', default=False, cast=bool)

INDEX_NAME = config('MULTI_INDEX_NAMES', default='date,secID')
COL_NAME = config('DF_COL_NAME', default='factor')


class WindQueryHelper:
    def __init__(self, data_dict_path=DATA_DICT_PATH, path_type_abs=DATA_DICT_PATH_TYPE_ABS):
        try:
            if not path_type_abs:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(current_dir, data_dict_path)
                self.data_dict_path = path
            else:
                self.data_dict_path = data_dict_path
            self._data_dict = pd.read_csv(self.data_dict_path, index_col=0, encoding='gbk')
        except ValueError:
            raise ValueError('data_dict fails to load')

    @property
    def data_dict(self):
        return self._data_dict

    @staticmethod
    def _split_params(params):
        main_params = params[[Header.API, Header.EXPLANATION, Header.INDICATOR]]
        extra_params = params.drop([Header.API, Header.EXPLANATION, Header.INDICATOR, Header.TYPE])
        extra_params[Header.TENOR.value] = np.nan
        extra_params[Header.FREQ.value] = 'M'
        return main_params, extra_params

    def get_query_params(self, factor_name=None):
        try:
            self.data_dict.index = self.data_dict.index.str.lower()
            factor_params = self.data_dict.loc[factor_name.lower()]
        except:
            raise ValueError(
                'WindQueryHelper.get_query_params: failed to find params for factor {0}, check factor name spelling'.format(
                    factor_name))
        main_params, extra_params = WindQueryHelper._split_params(factor_params)
        main_params[Header.API] = 'w.' + main_params[Header.API]

        return main_params, extra_params

    @staticmethod
    def convert_2_multi_index(df):
        df = df.copy()
        df = df.stack()
        df = pd.DataFrame(df)
        df.index.names = INDEX_NAME.split(',')
        df.columns = [COL_NAME]
        return df

    @staticmethod
    def reformat_wind_data(raw_data, date, output_data_format=OutputFormat.PIVOT_TABLE_DF, multi_factors=False):
        if not multi_factors:
            ret = pd.DataFrame(data=raw_data.Data,
                               columns=raw_data.Codes,
                               index=[date.strftime('%Y-%m-%d')])
            if output_data_format == OutputFormat.MULTI_INDEX_DF:
                ret = WindQueryHelper.convert_2_multi_index(ret)
        elif 'windcode' not in raw_data.Fields:
            ret = pd.DataFrame(data=np.array(raw_data.Data).T,
                               index=pd.MultiIndex.from_product([raw_data.Codes, [date.strftime('%Y-%m-%d')]],
                                                                names=['secID', 'date']),
                               columns=[raw_data.Fields])
        else:
            # ret = pd.DataFrame(data=np.array(raw_data.Data).T,
            #                    index=pd.MultiIndex.from_arrays([raw_data.Times, raw_data.Codes*len(raw_data.Times)],
            #                                                    names=['date', 'secID']),
            #                    columns=raw_data.Fields)
            ret = pd.DataFrame(data=np.array(raw_data.Data[2:]).T,
                               index=pd.MultiIndex.from_arrays([raw_data.Data[raw_data.Fields.index('windcode')],
                                                                raw_data.Times],
                                                               names=['secID', 'date']),
                               columns=[field for field in raw_data.Fields if field != 'time' and field != 'windcode'])
        return ret

    @staticmethod
    def latest_report_date(date):
        month = date.month
        if month <= 4:
            date = datetime.datetime(date.year - 1, 9, 30)
        elif month <= 8:
            date = datetime.datetime(date.year, 3, 31)
        elif month <= 11:
            date = datetime.datetime(date.year, 6, 30)
        else:
            date = datetime.datetime(date.year, 9, 30)
        return date
