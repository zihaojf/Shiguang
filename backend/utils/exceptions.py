# utils/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        customized_response = {
            "success": False,
            "code": response.status_code,
            "message": "请求失败"
        }

        # 处理字段级错误
        if response.status_code == 400:
            customized_response['errors'] = response.data
        else:
            customized_response['error_detail'] = response.data

        return Response(customized_response, status=response.status_code)
    return response