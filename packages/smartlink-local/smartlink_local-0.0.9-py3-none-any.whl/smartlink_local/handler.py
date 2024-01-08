import traceback
from http import HTTPStatus

from lambda_decorators import cors_headers
from sdk.src.utilities import create_http_body

from .smartlink import SmartLinkLocal

smartlink_local = SmartLinkLocal()


@cors_headers
# I'm not sure if we are going to use this handler, let's keep it for the future
def execute_smartlink_handler(event, context):
    # TODO Add optional parameter to logger.start()
    #  which called api_call, so logger.start will call api_management
    #  to insert into api_call_table all fields including session_id.

    # get parameters from event
    smartlink_identifier = event['pathParameters'].get("identifier")

    # TODO Please make sure that inside execute() we SELECT smartlink_view,
    #  if !UserContext.isLogin() UserContext.set_effective_profile_id(profile_id)
    try:
        smartlink_local.execute(smartlink_identifier=smartlink_identifier)

        body = {
            "message": "Executed SmartLink successfully with smartlink_identifier=" + smartlink_identifier,
            "input": event
        }

        response = {
            "statusCode": HTTPStatus.OK,
            "body": create_http_body(body)
        }

    except Exception as e:
        body = {
            "message": "Failed to execute SmartLink with smartlink_identifier=" + smartlink_identifier,
            "input": event,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

        response = {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": create_http_body(body)
        }
        traceback.print_exc()

    return response


@cors_headers
# Get SmartLink Data by Identifier
def get_smartlink_details_handler(event, context):
    # get parameters from the event
    smartlink_identifier = event['pathParameters'].get("identifier")

    try:
        smartlink_details = smartlink_local.get_smartlink_details(smartlink_identifier=smartlink_identifier)
        body = {
            "message": "Retrieved SmartLink successfully with smartlink_identifier=" + smartlink_identifier,
            "input": event,
            "smartlink_details": {k: str(v) for k, v in smartlink_details.items()}
        }

        response = {
            "statusCode": HTTPStatus.OK,
            "body": create_http_body(body)
        }

    except Exception as e:
        body = {
            "message": "Failed to retrieve SmartLink with smartlink_identifier=" + smartlink_identifier,
            "input": event,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

        response = {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": create_http_body(body)
        }
        traceback.print_exc()

    return response


# @cors_headers
# Not used currently
# def create_smartlink_handler(event, context):
#     from_recipient = json.loads(event.get("from_recipient"))
#     to_recipient = json.loads(event.get("to_recipient"))
#     campaign_id = event.get("campaign_id")
#     action_id = event.get("action_id")
#
#     # create a SmartLink
#     smartlink_id = smartlink_local.insert(from_recipient=from_recipient, to_recipient=to_recipient,
#                                           campaign_id=campaign_id, action_id=action_id)
#
#     body = {
#         "message": "Created smartlink successfully with smartlink_identifier" + str(smartlink_id),
#         "input": event,
#         "smartlink_id": smartlink_id
#     }
#     response = {
#         "statusCode": HTTPStatus.OK,
#         "body": create_http_body(body)
#     }
#
#     return response
