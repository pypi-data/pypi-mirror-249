import os

from circles_local_database_python.connector import Connector
from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from url_local import action_name_enum, component_name_enum, entity_name_enum
from url_local.url_circlez import OurUrl

from .api_limit import (API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
                        DEVELOPER_EMAIL)
from .api_management_local import APIManagementsLocal

load_dotenv()
BRAND_NAME = os.getenv('BRAND_NAME')
AUTHENTICATION_API_VERSION = 1
authentication_login_validate_user_jwt_url = OurUrl.endpoint_url(
    brand_name=BRAND_NAME,
    environment_name=os.getenv('ENVIRONMENT_NAME'),
    component_name=component_name_enum.ComponentName.AUTHENTICATION.value,
    entity_name=entity_name_enum.EntityName.AUTH_LOGIN.value,
    version=AUTHENTICATION_API_VERSION,
    action_name=action_name_enum.ActionName.VALIDATE_USER_JWT.value
)
api_management_local_python_code = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
# Can we create a logger with api_type_id
logger = Logger.create_logger(object=api_management_local_python_code)


class APIMangementManager():
    def __init__(self) -> None:
        pass

    @staticmethod
    def seconds_to_sleep_after_passing_the_hard_limit(api_type_id: int):
        # TODO Can we update the logger internal object and add api_type_id to all logger records?
        try:
            hard_limit_value, hard_limit_unit = APIManagementsLocal._get_hard_limit_by_api_type_id(
                api_type_id=api_type_id)
            connection = Connector.connect("api_call")
            cursor = connection.cursor()

            # TODO SELECT from _view and not _table
            query = f"""SELECT TIMESTAMPDIFF(SECOND, NOW(), 
                        (SELECT TIMESTAMPADD({hard_limit_unit}, 1, MIN(start_timestamp)) 
                        FROM (SELECT start_timestamp 
                            FROM api_call.api_call_table 
                            WHERE api_type_id = %s AND is_network=TRUE 
                            ORDER BY api_call_id DESC LIMIT %s) AS a))"""

            cursor.execute(query, (api_type_id, hard_limit_value))
            seconds_to_sleep_after_passing_the_hard_limit = cursor.fetchone()[0]

            logger.end(
                "seconds_to_sleep_after_passing_the_hard_limit = " + str(seconds_to_sleep_after_passing_the_hard_limit))
            return seconds_to_sleep_after_passing_the_hard_limit

        except Exception as exception:
            logger.exception("exception=" + str(exception), object=exception)
            logger.end()
            raise  # Raise the exception for higher-level handling
