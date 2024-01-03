from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger

from .constants import api_management_local_python_code

logger = Logger.create_logger(object=api_management_local_python_code)


class APICallsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="api_call", default_id_column_name="api_call_id",
                         default_table_name="api_call_table", default_view_table_name="api_call_view")

    def insert_api_call_dict(self, api_call_dict: dict) -> int:
        """Inserts a row into the api_call_table and returns the id of the inserted row"""
        logger.start(object={"api_call_data_dict ": api_call_dict})
        try:
            api_call_id = self.insert(data_json=api_call_dict)
            return api_call_id
        except Exception as exception:
            logger.exception(object=exception)
            raise exception
        finally:
            logger.end()
