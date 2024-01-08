from AccessControl.rolemanager import RoleManager
from Products.PlonePAS.plugins.role import GroupAwareRoleManager


def logafter(fun, action):
    def wrapper(*args, **kwargs):
        result = fun(*args, **kwargs)
        from redturtle.auditlog import logger

        logger.info("[%s] %s %s", action, args, kwargs),
        return result

    return wrapper


def patches():
    GroupAwareRoleManager.assignRolesToPrincipal = logafter(
        GroupAwareRoleManager.assignRolesToPrincipal, "USER ROLE ASSIGNED"
    )
    RoleManager.manage_setLocalRoles = logafter(
        RoleManager.manage_setLocalRoles, "USER LOCALROLE ASSIGNED"
    )
    RoleManager.manage_addLocalRoles = logafter(
        RoleManager.manage_addLocalRoles, "USER LOCALROLE ASSIGNED"
    )
    RoleManager.manage_delLocalRoles = logafter(
        RoleManager.manage_delLocalRoles, "USER LOCALROLE DELETED"
    )
