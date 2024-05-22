from rest_framework.response import Response
from rest_framework import status

def check_auth(request):
    return request.user.is_authenticated


def check_permissions(request, permissions, option='AND'):
    # check if the user exists have the role:
    if not check_auth(request):
        return False
    roles = request.user.roles.all()
    if not roles:
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

def unauthorized():
    return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)