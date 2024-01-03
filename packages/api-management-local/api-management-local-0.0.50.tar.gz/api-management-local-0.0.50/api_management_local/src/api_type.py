from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger

from .constants import api_management_local_python_code
from .Exception_API import ApiTypeDisabledException, ApiTypeIsNotExistException

logger = Logger.create_logger(object=api_management_local_python_code)


class ApiTypesLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="api_type", default_table_name="api_type_table",
                         default_view_table_name="api_type_view", default_id_column_name="api_type_id")

    def get_action_id_by_api_type_id(self, api_type_id: int) -> int:
        select_clause = "action_id"
        where = "api_type_id = %s AND is_enabled = TRUE"
        action_id = self.select_one_dict_by_where(
            select_clause_value=select_clause, where=where, params=(api_type_id,))
        if action_id is None:
            action_id = self.select_one_tuple_by_id(select_clause_value="action_id",
                                                    id_column_value=api_type_id)
            if not action_id:
                raise ApiTypeIsNotExistException
            else:
                raise ApiTypeDisabledException

        return action_id["action_id"]
