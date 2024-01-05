import re

from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from user_context_remote.user_context import UserContext

from .generic_crud import GenericCRUD
from .connector import Connector
from .utils import validate_none_select_table_name, validate_select_table_name, process_insert_data_json, process_update_data_json  # noqa501

# Constants
DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_ID = 206
DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_NAME = 'circles_local_database_python\\generic_crud_ml'  # noqa501
DEVELOPER_EMAIL = 'tal.g@circ.zone'
DEFAULT_LIMIT = 100

user_context = UserContext()
user = user_context.login_using_user_identification_and_password()

# Logger setup
logger = Logger.create_logger(object={
    'component_id': DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_ID,
    'component_name': DATABASE_MYSQL_GENERIC_CRUD_ML_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
})

TEST_TABLE_NAME = 'test_mysql_table'
TEST_ML_TABLE_NAME = 'test_mysql_ml_table'


class GenericCRUDML(GenericCRUD):
    """A class that provides generic CRUD functionality for tables with multi-language support."""  # noqa501

    def __init__(self, default_schema_name: str,
                 default_table_name: str = None,
                 default_ml_table_name: str = None,
                 default_view_table_name: str = None,
                 default_id_column_name: str = None,
                 connection: Connector = None) -> None:
        """Initializes the GenericCRUDML class. If connection is not provided,
        a new connection will be created."""
        logger.start(object={"default_schema_name": default_schema_name,
                             "default_table_name": default_table_name,
                             "id_column_name": default_id_column_name})
        super().__init__(default_schema_name=default_schema_name,
                         default_table_name=default_table_name,
                         default_view_table_name=default_view_table_name,
                         default_id_column_name=default_id_column_name,
                         connection=connection)
        if default_table_name is not None or default_ml_table_name is not None:
            self.default_ml_table_name = default_ml_table_name or re.sub(r'(_table)$', '_ml\\1', default_table_name)  # noqa501
        logger.end()

    def sql_in_list_by_entity_list_id(self, schema_name: str, entity_name: str,
                                      entity_list_id: int) -> str:
        """Example: select group_id from group.group_list_member_table WHERE group_list_id=1"""  # noqa501
        old_schema_name = self.schema_name
        self.set_schema(schema_name)
        ids = self.select_multi_dict_by_id(view_table_name=f"{entity_name}_list_member_view",  # noqa501
                                           select_clause_value=f"{entity_name}_id",  # noqa501
                                           id_column_name=f"{entity_name}_list_id",  # noqa501
                                           id_column_value=entity_list_id)
        ids = ids or [{f"{entity_name}_id": -1}]
        result = f" IN ({','.join([str(_id[f'{entity_name}_id']) for _id in ids])})"  # noqa501
        self.set_schema(old_schema_name)
        return result
