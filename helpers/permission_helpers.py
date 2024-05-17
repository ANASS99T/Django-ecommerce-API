
from roles.models import Permission


def check_auth(request):
    return request.user.is_authenticated


def check_permissions(request, permission):
    user_permissions = Permission.objects.filter(
        role__user=request.user, name=permission)
    return user_permissions.exists()
