from rest_framework import generics
from .models import ContactDetails
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from .decorators import validate_request_data
from rest_framework.response import Response
from .serializers import ContactDetailsSerializer, TokenSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
           
            login(request, user)
            serializer = TokenSerializer(data={
               
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterUsers(generics.CreateAPIView):
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(status=status.HTTP_201_CREATED)

# Get all Contact Details

# class ListContactView(generics.ListAPIView):
    
#     queryset = ContactDetails.objects.all()
#     serializer_class = ContactDetailsSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#Create New Contact
class CreateContactView(generics.ListCreateAPIView):
    
    queryset = ContactDetails.objects.all()
    serializer_class = ContactDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        contact = ContactDetails.objects.create(
            title=request.data["name"],
            artist=request.data["phone_number"]
        )
        return Response(
            data=ContactDetailsSerializer(contact).data,
            status=status.HTTP_201_CREATED
        )

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = ContactDetails.objects.all()
    serializer_class = ContactDetailsSerializer

    def get(self, request, *args, **kwargs):
        try:
            contact = self.queryset.get(pk=kwargs["name"])
            return Response(SongsSerializer(contact).data)
        except ContactDetails.DoesNotExist:
            return Response(
                data={
                    "message": "Given name  {} does not exist".format(kwargs["name"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            contact = self.queryset.get(pk=kwargs["name"])
            serializer = ContactDetailsSerializer()
            updated_contact = serializer.update(contact, request.data)
            return Response(ContactDetailsSerializer(updated_contact).data)
        except ContactDetails.DoesNotExist:
            return Response(
                data={
                    "message": "Given name: {} does not exist".format(kwargs["name"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            contact = self.queryset.get(pk=kwargs["name"])
            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ContactDetails.DoesNotExist:
            return Response(
                data={
                    "message": "Given name: {} does not exist".format(kwargs["name"])
                },
                status=status.HTTP_404_NOT_FOUND
            ) 