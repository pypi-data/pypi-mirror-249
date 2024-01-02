import http
import json

import requests
from logger_local.Logger import Logger
from star_local.star_local import StarsLocal

from .api_call import APICallsLocal
from .api_limit_status import APILimitStatus
from .api_management_local import APIManagementsLocal
from .api_type import ApiTypesLocal
from .constants import api_management_local_python_code
from .Exception_API import PassedTheHardLimitException
from .external_user_id import get_extenal_user_id_by_api_type_id

logger = Logger.create_logger(object=api_management_local_python_code)


class Direct:
    @staticmethod
    def try_to_call_api(external_user_id: int, api_type_id: int, url: str, outgoing_data: dict,
                        outgoing_header: dict) -> dict:
        logger.start(
            object={'external_user_id': str(external_user_id), 'api_type_id': str(api_type_id),
                    'endpoint': str(url), 'outgoing_body': str(outgoing_data), 'outgoing_header': str(outgoing_header)})
        action_id = ApiTypesLocal.get_action_id_by_api_type_id(api_type_id)
        StarsLocal.profile_star_before_action(action_id)
        api_management = APIManagementsLocal()
        api_management.sleep_per_interval(api_type_id)

        if external_user_id is None:
            external_user_id = get_extenal_user_id_by_api_type_id(api_type_id)
        # connection = Connector.connect("api_call")
        # cursor = connection.cursor()

        try:
            arr, outgoing_data_significant_fields_hash = api_management.check_cache(
                api_type_id, outgoing_data)
            if arr is None:
                check = api_management.check_limit(
                    external_user_id=external_user_id, api_type_id=api_type_id)
                logger.info("check= " + str(check))
                if check == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                    logger.warn("You excced the soft limit")
                if check != APILimitStatus.GREATER_THAN_HARD_LIMIT:
                    output = requests.post(url=url, data=outgoing_data, headers=outgoing_header)
                    status_code = output.status_code
                    text = output.text
                    incoming_message = output.content.decode('utf-8')
                    response_body = output.json()
                    response_body_str = json.dumps(response_body)
                    if http.HTTPStatus.OK == status_code:
                        StarsLocal.api_executed(api_type_id=api_type_id)
                    is_network = 1
                    api_call_data_dict = {
                        'api_type_id': api_type_id, 'external_user_id': external_user_id,
                        'endpoint': url, 'outgoing_header': str(outgoing_header),
                        'outgoing_body': str(outgoing_data),
                        'outgoing_body_significant_fields_hash': outgoing_data_significant_fields_hash,
                        'incoming_message': incoming_message, 'http_status_code': status_code,
                        'response_body': response_body_str,
                        'is_network': is_network
                    }
                    api_call_id = APICallsLocal.insert_api_call_dict(api_call_data_dict)
                    logger.end("check= " + str(check),
                               object={'status_code': status_code, 'text': text, 'api_call_id': api_call_id})
                    # return request("post", url=url, data=outgoing_data, json=json, **kwargs)
                    return {'status_code': status_code, 'text': text, 'api_call_id': api_call_id}

                else:
                    logger.error("you passed the hard limit")
                    raise PassedTheHardLimitException
            else:
                status_code = arr[0]
                text = arr[1]
                is_network = 0
                incoming_message = ""
                response_body = ""
                api_call_data_dict = {'api_type_id': api_type_id, 'external_user_id': external_user_id,
                                      'endpoint': url, 'outgoing_header': str(outgoing_header),
                                      'outgoing_body': str(outgoing_data),
                                      'outgoing_body_significant_fields_hash': outgoing_data_significant_fields_hash,
                                      'incoming_message': incoming_message, 'http_status_code': status_code,
                                      'response_body': response_body,
                                      'is_network': is_network
                                      }
                StarsLocal.api_executed(api_type_id=api_type_id)
                api_call_id = APICallsLocal.insert_api_call_dict(api_call_data_dict)
                logger.info("bringing result from cache in database", object={
                    'status_code': status_code, 'text': text, 'api_call_id': api_call_id})
                return {'status_code': status_code, 'text': text, 'api_call_id': api_call_id}
        except Exception as exception:
            logger.exception("exception=" + str(exception), object=exception)
            logger.end()
            raise exception
