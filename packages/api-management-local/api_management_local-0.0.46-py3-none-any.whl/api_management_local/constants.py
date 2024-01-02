import os

# from circles_local_database_python.generic_crud import GenericCRUD
from dotenv import load_dotenv
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from sdk.src.validate import validate_enviroment_variables
from url_local import action_name_enum, component_name_enum, entity_name_enum
from url_local.url_circlez import OurUrl

load_dotenv()
# TODO Please use/create get_environment_name() and get_brand_name() functions one time in python-sdk-python-package
BRAND_NAME = os.getenv('BRAND_NAME')
validate_enviroment_variables()
# TODO Please use/create AUTHENTICATION_API_VERSION_DICT[environment_name] in url-remote-python-package
AUTHENTICATION_API_VERSION = 1
API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID = 212
API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME = "api-management-local-python-package"
DEVELOPER_EMAIL = "heba.a@circ.zone"

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
