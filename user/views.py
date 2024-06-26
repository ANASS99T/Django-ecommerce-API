from django.db import DatabaseError
from rest_framework import viewsets, status
from rest_framework.response import Response
from global_vars.models import Global_Vars
from user.models import Client
from user.serializer import ClientSerializer
from helpers.permission_helpers import check_permissions, unauthorized, check_auth
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.decorators import action


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(deleted_at__isnull=True)
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_create_client'):
            return unauthorized()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_update_client'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def self_update(self, request, *args, **kwargs):
        if not check_permissions(request, ['can_update_client_self']):
            return unauthorized()
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def destroy_list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_client_all'):
            return unauthorized()
        ids_to_delete = request.data.get('ids', [])  # Get the list of IDs from the request data
        for id in ids_to_delete:
            instance = self.queryset.get(id=id)  # Get the instance with the given ID
            self.perform_destroy(instance)  # Delete the instance
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_client'):
            return unauthorized()
        client = self.get_object()
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def self_destroy(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_delete_client_self'):
            return unauthorized()
        instance = request.user
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_client_all'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_view_client'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        if not check_permissions(request, 'can_reset_password'):
            return unauthorized()
        instance = self.get_object()
        try:
            global_var = Global_Vars.objects.get(key='default_password')
        except Global_Vars.DoesNotExist:
            return Response({"error": "Default password not set in global variables"},
                            status=status.HTTP_400_BAD_REQUEST)
        new_password = global_var.value
        instance.password = make_password(new_password)
        instance.save()
        return Response(status=status.HTTP_200_OK, data={"message": "Password reset successfully"})

    @action(detail=False, methods=['post'])
    def self_reset_password(self, request, *args, **kwargs):
        if not check_permissions(request, ['can_reset_password', 'can_reset_password_self'], option='OR'):
            return unauthorized()
        instance = request.user
        try:
            global_var = Global_Vars.objects.get(key='default_password')
        except Global_Vars.DoesNotExist:
            return Response({"error": "Default password not set in global variables"},
                            status=status.HTTP_400_BAD_REQUEST)
        new_password = global_var.value
        instance.password = make_password(new_password)
        return Response(status=status.HTTP_200_OK, data={"message": "Password reset successfully"})

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        client = None

        if not password or not (email or phone_number):
            return Response({"error": "Email or phone number and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = get_user_model()
        try:
            if email:
                client = user.objects.get(email=email)
            else:
                client = user.objects.get(phone_number=phone_number)
        except client.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not client.is_active:
            return Response({"error": "User is not active"}, status=status.HTTP_403_FORBIDDEN)

        token, created = Token.objects.get_or_create(user=client)
        if not created:
            return Response({"error": "Failed to create token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "User logged in successfully", "token": token.key}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        username = request.data.get('username')

        if not username:
            username = email

        client = None

        if not email and not phone_number:
            return Response({"error": "Email or phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not password or not confirm_password:
            return Response({"error": "Password and confirm password are required"}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_model()

        if email:
            try:
                client = user.objects.get(email=email)
            except user.DoesNotExist:
                pass
        elif phone_number:
            try:
                client = user.objects.get(phone_number=phone_number)
            except user.DoesNotExist:
                pass
        else:
            return Response({"error": "Email or Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        if client:
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Client.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
        except DatabaseError as e:
            return Response({"error": "Database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not user:
            return Response({"error": "Failed to create user"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User registered successfully", "username":user.username}, status=status.HTTP_201_CREATED)
