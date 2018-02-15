# -*- coding: utf-8 -*-


from enum import Enum
from enum import IntEnum


class StrEnum(str, Enum):
    pass


class FreqType(StrEnum):
    MIN1 = 'min1'
    MIN5 = 'min5'
    MIN10 = 'min10'
    EOD = 'D'
    EOW = 'W'
    EOM = 'M'
    EOSY = 'S'
    EOY = 'Y'


class OutputFormat(IntEnum):
    MULTI_INDEX_DF = 0
    PIVOT_TABLE_DF = 1


class Header(StrEnum):
    NAME = 'name'
    TENOR = 'tenor'
    API = 'api'
    INDICATOR = 'indicator'
    FREQ = 'period'
    PRICEADJ = 'priceadj'
    UNIT = 'unit'
    TRADEDATE = 'tradeDate'
    CYCLE = 'cycle'
    EXPLANATION = 'explanation'
    TYPE = 'type'
    REPORTADJ = 'reportadj'
    MULTIFACTORS = 'multifactors'


class WindDataType(IntEnum):
    WSS_TYPE = 0
    WSD_TYPE = 1


class LogLevel(StrEnum):
    INFO = 'info'
    WARNING = 'warining'
    CRITICAL = 'critical'
    NOTSET = 'notset'