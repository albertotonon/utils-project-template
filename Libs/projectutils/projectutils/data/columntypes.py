# hint: don't use categorical columns at this point since the pandas type "category" is not very
# usable yet (I had some issues in the past). You could use information on which columns
# should be treated as categorical values when you create your model, for example as an
# hyper-parameter.
ID_COLUMN = ''
TARGET_COLUMN = ''

INTEGER_COLUMNS = set()

FLOAT_COLUMNS = set()

BOOL_COLUMNS = set()

DATETIME_COLUMNS = set()

DATE_COLUMNS = set()

STRING_COLUMNS = set()


def union_all_columns() -> set[str]:
    all_cols = INTEGER_COLUMNS.copy()
    all_cols.update(FLOAT_COLUMNS, BOOL_COLUMNS, DATE_COLUMNS, DATETIME_COLUMNS, STRING_COLUMNS)
    return all_cols


ALL_KNOWN_COLUMNS = union_all_columns()
