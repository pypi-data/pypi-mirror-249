from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger

from .constants import api_management_local_python_code

logger = Logger.create_logger(object=api_management_local_python_code)


class APICallsLocal(GenericCRUD):
    def __init__(self) -> None:
        # TODO What about default id column = "api_call_id"
        super().__init__(default_schema_name="api_call", default_table_name="api_call_table")

    @staticmethod
    # TODO Should be public and also used by logger.start() when sending api_call_dict (in incoming API handers)
    # TOOD api_call_data_dict -> api_call_dict
    def insert_api_call_dict(api_call_data_dict: dict) -> int:
        if api_call_data_dict['is_network'] is None:
            api_call_data_dict['is_network'] = "null"
        logger.start(object={"api_call_data_dict ": api_call_data_dict})
        try:
            api_local = APICallsLocal()
            api_call_id = api_local.insert(data_json=api_call_data_dict)
            logger.end()
            return api_call_id
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise exception
