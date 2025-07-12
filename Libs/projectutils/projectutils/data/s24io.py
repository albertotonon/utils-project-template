import logging
import re
import sys
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame, Series, read_csv
from pandas.core.dtypes.common import is_bool_dtype, is_numeric_dtype, is_string_dtype
from pandas.errors import OutOfBoundsDatetime
from pandas.io.formats.style import Styler

from projectutils.data.columntypes import (BOOL_COLUMNS, DATETIME_COLUMNS, DATE_COLUMNS, FLOAT_COLUMNS, INTEGER_COLUMNS,
                                           STRING_COLUMNS, )


class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


skipped_line_re = re.compile(r'Skipping line +(\d+)')


def read_csv_list_errors(fname: Path, sep=',') -> Tuple[List[int], DataFrame]:
    """Reads a CSV file and returns the indexes of lines with parse errors."""
    newstderr = StringIO()
    with RedirectStdStreams(stderr=newstderr):
        result_dataframe = read_csv(fname, sep=sep,
                                    compression='infer',
                                    error_bad_lines=False, warn_bad_lines=True)
    error_line_numbers = [int(match.group(1)) for match in skipped_line_re.finditer(newstderr.getvalue())]
    return error_line_numbers, result_dataframe


def read_csv_cast_types(filename: Path, sep=',') -> DataFrame:
    """Reads an AutoScout dataset from a CSV file and outputs a dataframe with the right type for each column."""
    logging.info(f'Loading data from CSV file "{filename}"...')
    err_lines, raw_data = read_csv_list_errors(filename, sep=sep)
    if err_lines:
        logging.warning(f'Found {len(err_lines)} lines with errors.')
    cast_types(raw_data)
    return raw_data


def cast_types(raw_data: DataFrame):
    """
    Modifies the input dataframe to adhere to the AS24 data definition.
    :param raw_data:
    :return: nothing, the dataframe is modified in-place.
    """
    logging.info('Converting column types...')
    for column in raw_data.columns:
        logging.debug(f'Processing "{column}"')
        if column in INTEGER_COLUMNS:
            # ordinary int (lowercase i) cannot handle NaNs
            to_float = pd.to_numeric(raw_data[column], errors='coerce')
            right_int_type = _get_equivalent_int_type(to_float.dtype)
            # to avoid "TypeError: cannot safely cast non-equivalent float64 to int64"
            raw_data[column] = np.floor(to_float).astype(right_int_type)
        elif column in FLOAT_COLUMNS:
            raw_data[column] = pd.to_numeric(raw_data[column], errors='coerce', downcast='float')
        elif column in BOOL_COLUMNS:
            raw_data[column] = _convert_to_bool(raw_data[column])
        elif column in DATE_COLUMNS:
            raw_data[column] = _convert_to_datetime(raw_data[column], input_with_time=False)
        elif column in DATETIME_COLUMNS:
            raw_data[column] = _convert_to_datetime(raw_data[column], input_with_time=True)
        elif column in STRING_COLUMNS:
            raw_data[column] = _convert_to_str_keep_nan(raw_data, column)
        else:
            logging.warning(f'Unknown type for column "{column}"')


def _get_equivalent_int_type(float_dtype: np.dtype) -> str:
    """
    Returns an Int dtype (capital "I" for allowing NaNs) with the same bit size as the input float dtype.
    :param float_dtype:
    :return: an Int dtype (capital "I" for allowing NaNs) with the same bit size as the input float dtype.
    """
    num_bits_str = re.findall(r'\d+$', float_dtype.name)
    assert len(num_bits_str) == 1
    return f'Int{num_bits_str[0]}'


def _convert_to_bool(series_raw: Series) -> Series:
    if is_bool_dtype(series_raw):
        return series_raw
    if is_numeric_dtype(series_raw):
        return series_raw > 0
    if is_string_dtype(series_raw):
        return series_raw.isin(['true', 'True', 'TRUE'])
    raise ValueError("Don't know how to convert column to boolean.")


def _convert_to_datetime(series_str: Series, input_with_time: bool):
    format_str = '%Y-%m-%d %H:%M:%S' if input_with_time else '%Y-%m-%d'
    try:
        return pd.to_datetime(series_str, format=format_str, errors='coerce')
    except OutOfBoundsDatetime:
        timestamp_max_year = str(pd.Timestamp.max.year)
        modified_series = series_str.copy()
        modified_series[modified_series.str[0:4] > timestamp_max_year] = pd.Timestamp.max.strftime(format_str)
        return _convert_to_datetime(modified_series, input_with_time)


def _convert_to_str_keep_nan(df: DataFrame, col_name: str):
    # all this mess because pandas' `astype('str')` replaces NaNs with 'nan'
    return np.where(pd.isnull(df[col_name]), df[col_name], df[col_name].astype(str))


def to_unix_timestamp(dt: Series):
    return (dt - pd.Timestamp(ts_input='1970-01-01', tz=dt.dt.tz)) // pd.Timedelta('1s')


def prettify(data_frame: DataFrame) -> Styler:
    """
    Use this to nicely format a dataframe in a Jupyter notebook.
    Floating point numbers will be formatted by keeping 2 decimal digits and adding thousand separators.
    """
    format_dict = {m: '{:,.2f}'
                   for m in data_frame.select_dtypes(include=['float']).columns}
    format_dict.update({m: '{:,.0f}'
                        for m in data_frame.select_dtypes(include=['int']).columns})
    return data_frame.style.format(format_dict)


def load_ini_config(config: Path) -> ConfigParser:
    parser = ConfigParser(allow_no_value=True)
    parser.read(str(config))
    return parser
