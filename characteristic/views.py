from rest_framework import viewsets, status
from rest_framework.response import Response

from helpers.permission_helpers import unauthorized, check_permissions, check_auth
from characteristic.models import Characteristic
from characteristic.serializer import CharacteristicSerializer


class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.filter(deleted_at__isnull=True)
    serializer_class = CharacteristicSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new characteristic.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.

        Raises:
            Unauthorized: If the user does not have permission to create a characteristic.
            ValidationError: If the request data is invalid.
        """

        if not check_permissions(request, 'can_create_characteristic'):
            return unauthorized()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing characteristic.

        This method is used to update an existing characteristic object. It checks the user's permissions
        to ensure they have the necessary rights to update a characteristic. If the user does not have
        the required permissions, an unauthorized response is returned.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args (tuple): Additional positional arguments.
            **kwargs (dict): Additional keyword arguments.

        Returns:
            Response: The updated characteristic data in the response body with a status code of 200 (OK).

        Raises:
            PermissionDenied: If the user does not have the necessary permissions.
            ValidationError: If the serializer data is invalid.
        """
        if not check_permissions(request, 'can_update_characteristic'):
            return unauthorized()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a characteristic.

        This method deletes a characteristic object based on the provided request.
        It checks the permissions of the request and returns an unauthorized response
        if the user does not have the required permission. If the characteristic is found,
        it sets the `deleted_at` attribute to the deletion time, marking it as deleted.
        A response with status code 204 (No Content) is returned.
        If any exception occurs during the deletion process, a response with status code
        400 (Bad Request) and an error message is returned.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.

        Raises:
            None
        """
        if not check_permissions(request, 'can_delete_characteristic'):
            return unauthorized()
        try:
            characteristic = self.get_object()
            characteristic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        List all characteristics.

        This method checks if the user has the `can_view_characteristic_list` permission.
        If the user has the permission, it calls the parent class's list method to return a list of all characteristics.
        If the user does not have the permission, it returns an unauthorized response.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object. Contains a list of all characteristics if the user has the required permission.
        """
        if not check_permissions(request, 'can_view_characteristic_list'):
            return unauthorized()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific characteristic.

        This method checks if the user has the `can_view_characteristic` permission.
        If the user has the permission, it calls the parent class's retrieve method to return the specified characteristic.
        If the user does not have the permission, it returns an unauthorized response.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object. Contains the specified characteristic if the user has the required permission.
        """
        if not check_permissions(request, 'can_view_characteristic'):
            return unauthorized()
        return super().retrieve(request, *args, **kwargs)
