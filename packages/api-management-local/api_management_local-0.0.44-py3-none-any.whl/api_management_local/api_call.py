import ast
import json
from typing import Dict

from circles_local_database_python.generic_crud import GenericCRUD
from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

from .api_limit import (API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
                        DEVELOPER_EMAIL)

api_management_local_python_code = {
    "component_id": API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    "component_name": API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    "component_category": LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": DEVELOPER_EMAIL,
}
load_dotenv()

logger = Logger.create_logger(object=api_management_local_python_code)


class APICallsLocal(GenericCRUD):
    def __init__(self) -> None:
        # TODO What about default id column = "api_call_id"
        super().__init__(default_schema_name="api_call", default_table_name="api_call_table")

    @staticmethod
    # TODO Should be public and also used by logger.start() when sending api_call_dict (in incoming API handers)
    # TOOD api_call_data_dict -> api_call_dict
    def _insert_api_call_dict(api_call_data_dict: dict) -> int:
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
