from rest_framework.response import Response
from rest_framework import status
from roles.models import Role, Permission


def check_auth(request) -> bool:
    return request.user.is_authenticated


def check_permissions(request, permissions, option='AND') -> bool:
    # check if the user exists have the role:
    if not check_auth(request):
        return False
    roles = request.user.roles.all()

    roles_list = list(roles)

    if not roles_list:
        return False

    if not isinstance(permissions, list):
        permissions = [permissions]
    if option == 'AND':
        for permission in permissions:
            # check if any of the roles have the permission:
            for role in roles:
                if not role.permissions.filter(name=permission).exists():
                    return False
            return True
    elif option == 'OR':
        for permission in permissions:
            # check if any of the roles have the permission:
            for role in roles:
                if role.permissions.filter(name=permission).exists():
                    return True
        return False


def unauthorized() -> Response:
    return Response({'message': 'Unauthorized to do this action'}, status=status.HTTP_401_UNAUTHORIZED)