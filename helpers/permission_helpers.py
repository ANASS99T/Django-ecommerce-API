

def check_auth(request):
    return request.user.is_authenticated


def check_permissions(request, permission):
    # check if the user exists have the role:
    if not check_auth(request):
        return False
    roles = request.user.roles.all()
    if not roles:
        return False

    # check if any of the roles have the permission:
    for role in roles:
        if role.permissions.filter(name=permission).exists():
            return True
    return False
