from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        name = args[0].request.data.get("name", "")
        phone_number = args[0].request.data.get("phone_number", "")
        if not title and not artist:
            return Response(
                data={
                    "message": "Both name and number are required to add a contact"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated