import json

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from cosmic_pipeline.exceptions import CosmicPipelineValidationError


def custom_exception_handler(exc, context):
    if isinstance(exc, CosmicPipelineValidationError):
        return Response(
            json.loads(json.dumps(exc.message_dict)), status=status.HTTP_400_BAD_REQUEST
        )
    if isinstance(exc, IntegrityError):
        message = "Entry already exists, unique constraint violated."
        return Response(
            {"detail": message}, status=status.HTTP_400_BAD_REQUEST
        )
    response = exception_handler(exc, context)
    if response is not None:
        pass
    if response is not None:
        if isinstance(response.data, list):
            response.data = {"detail": response.data, "status_code": response.status_code}
        else:
            response.data["status_code"] = response.status_code
    return response
