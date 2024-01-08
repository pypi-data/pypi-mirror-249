from redturtle.auditlog import logger


def new_user(principal, event):
    logger.info(
        "[USER CREATED] id=%s username=%s path=%s email=%s fullname=%s roles=%s",
        principal.getId(),
        principal.getUserName(),
        "/".join(principal.getPhysicalPath()),
        principal.getProperty("email"),
        principal.getProperty("fullname"),
        principal.getRoles(),
    )


def del_user(userid, event):
    logger.info("[USER DELETED] id=%s", userid)


def new_group(groupname, event):
    logger.info("[GROUP CREATED] id=%s", groupname)


def del_group(groupname, event):
    logger.info("[GROUP DELETED] id=%s", groupname)


def add_principal_to_group(principal, event):
    logger.info("[USER ADDED TO GROUP] id=%s group=%s", principal, event.group_id)


def remove_principal_from_group(principal, event):
    logger.info("[USER REMOVED FROM GROUP] id=%s group=%s", principal, event.group_id)
