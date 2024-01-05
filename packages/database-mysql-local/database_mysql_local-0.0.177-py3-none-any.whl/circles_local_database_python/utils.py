import os
from .to_sql_interface import ToSQLInterface


def validate_select_table_name(database_object_name: str) -> None:
    if os.getenv("environment_name") not in ("prod1", "dvlp1") and not database_object_name.endswith("_view"):  # noqa501
        raise Exception(
            f"View name must end with '_view' in this environment (got {database_object_name})")  # noqa501


def validate_none_select_table_name(database_object_name: str) -> None:
    if os.getenv("environment_name") not in ("prod1", "dvlp1") and not database_object_name.endswith("_table"):  # noqa501
        raise Exception(f"Table name must end with '_table' in this environment  (got {database_object_name})")  # noqa501


def process_insert_data_json(data_json):
    columns = []
    values = []

    # TODO What if data_json is None
    for key, value in data_json.items():
        if isinstance(value, ToSQLInterface):
            columns.append(key)
            values.append(value.to_sql())
        else:
            columns.append(key)
            values.append('%s')

    filtered_data_json = {key: value for key, value in data_json.items() if not isinstance(value, ToSQLInterface)}  # noqa501
    return ','.join(columns), ','.join(values), filtered_data_json


# Please add typing and example of input-output as docstring if possible.
def process_update_data_json(data_json):
    set_values = []

    for key, value in data_json.items():
        if isinstance(value, ToSQLInterface):
            set_values.append(f"{key}={value.to_sql()}")
        else:
            set_values.append(f"{key}=%s")

    filtered_data_json = {key: value for key, value in data_json.items() if not isinstance(value, ToSQLInterface)}  # noqa501
    return ', '.join(set_values) + ("," if data_json else ""), filtered_data_json  # noqa501
