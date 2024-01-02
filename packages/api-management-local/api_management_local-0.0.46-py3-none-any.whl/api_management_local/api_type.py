from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger

from .constants import api_management_local_python_code
from .Exception_API import ApiTypeDisabledException, ApiTypeIsNotExistException

logger = Logger.create_logger(object=api_management_local_python_code)


class ApiTypesLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="api_type", default_table_name="api_type_view")

    @staticmethod
    def get_action_id_by_api_type_id(api_type_id: int) -> int:
        api_type = ApiTypesLocal()
        select_clause = "action_id"
        where = "api_type_id = {} AND is_enabled = TRUE".format(api_type_id)
        action_id = api_type.select_one_tuple_by_where(
            view_table_name="api_type_view", select_clause_value=select_clause, where=where)
        if action_id is None:
            select_clause = "action_id"
            where = "api_type_id = {}".format(api_type_id)
            api_type = ApiTypesLocal()
            # TODO Change it to use by_id
            action_id = api_type.select_one_tuple_by_where(select_clause_value=select_clause, where=where)
            if action_id is None:
                raise ApiTypeIsNotExistException
            else:
                raise ApiTypeDisabledException

        return action_id[0]
