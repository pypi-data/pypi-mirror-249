# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.auditlog import logger
from redturtle.auditlog.testing import (  # noqa: E501
    REDTURTLE_AUDITLOG_INTEGRATION_TESTING,
)

import unittest


class TestUser(unittest.TestCase):
    layer = REDTURTLE_AUDITLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_create_user(self):
        with self.assertLogs(logger, level="INFO") as cm:
            api.user.create(
                username="foo", email="foo@example.org", password="secret!!"
            )
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER CREATED] id=foo username=foo "
                    "path=/plone/acl_users email= fullname= roles=['Authenticated']"
                ],
            )

    def test_delete_user(self):
        api.user.create(username="foo", email="foo@example.org", password="secret!!")
        with self.assertLogs(logger, level="INFO") as cm:
            api.user.delete(username="foo")
            self.assertEqual(
                cm.output, ["INFO:redturtle.auditlog:[USER DELETED] id=foo"]
            )


class TestRoles(unittest.TestCase):
    layer = REDTURTLE_AUDITLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_assign_global_role_to_user(self):
        user = api.user.create(
            username="foo", email="foo@example.org", password="secret!!"
        )
        self.assertEqual(user.getRoles(), ["Member", "Authenticated"])
        with self.assertLogs(logger, level="INFO") as cm:
            api.user.grant_roles(username="foo", roles=["Manager"])
            self.assertEqual(len(cm.output), 1)
            self.assertTrue(
                cm.output[0].startswith(
                    "INFO:redturtle.auditlog:[USER ROLE ASSIGNED] "
                    "(<GroupAwareRoleManager at /plone/acl_users/portal_role_manager>, "
                )
                # "['Authenticated', 'Manager', 'Member'], 'foo') {}"
            )
            # XXX: roles are not sorted in the log
            self.assertIn("'Manager'", cm.output[0])
            self.assertTrue(cm.output[0].endswith("], 'foo') {}"))

        # revoke global roles became set new roles
        with self.assertLogs(logger, level="INFO") as cm:
            api.user.revoke_roles(username="foo", roles=["Manager"])
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER ROLE ASSIGNED] "
                    "(<GroupAwareRoleManager at /plone/acl_users/portal_role_manager>, "
                    "['Member'], 'foo') {}"
                ],
            )

    def test_assign_local_role_to_user(self):
        user = api.user.create(
            username="foo", email="foo@example.org", password="secret!!"
        )
        self.assertEqual(user.getRoles(), ["Member", "Authenticated"])
        folder = api.content.create(
            type="Folder",
            title="Folder",
            container=self.portal,
        )
        with self.assertLogs(logger, level="INFO") as cm:
            api.user.grant_roles(username="foo", roles=["Manager"], obj=folder)
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER LOCALROLE ASSIGNED] (<Folder at /plone/folder>, "
                    "'foo', ['Manager']) {}"
                ],
            )

        with self.assertLogs(logger, level="INFO") as cm:
            api.user.revoke_roles(username="foo", roles=["Manager"], obj=folder)
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER LOCALROLE DELETED] (<Folder at /plone/folder>, "
                    "['foo']) {}"
                ],
            )


class TestGroups(unittest.TestCase):
    layer = REDTURTLE_AUDITLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.foo = api.user.create(
            username="foo", email="foo@example.org", password="secret!!"
        )

    def test_create_group(self):
        with self.assertLogs(logger, level="INFO") as cm:
            api.group.create(
                groupname="group",
                title="Group",
                description="Group Description",
                roles=["Manager"],
            )
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[GROUP CREATED] id=group",
                    "INFO:redturtle.auditlog:[USER ROLE ASSIGNED] "
                    "(<GroupAwareRoleManager at /plone/acl_users/portal_role_manager>, ['Manager'], 'group') {}",
                ],
            )

    def test_delete_group(self):
        api.group.create(groupname="group")
        with self.assertLogs(logger, level="INFO") as cm:
            api.group.delete(groupname="group")
            self.assertEqual(
                cm.output, ["INFO:redturtle.auditlog:[GROUP DELETED] id=group"]
            )

    def test_assign_user_to_group(self):
        group = api.group.create(groupname="group")
        self.assertEqual(group.getGroupMembers(), [])
        with self.assertLogs(logger, level="INFO") as cm:
            api.group.add_user(groupname="group", username="foo")
            self.assertEqual(
                cm.output,
                ["INFO:redturtle.auditlog:[USER ADDED TO GROUP] id=foo group=group"],
            )

        with self.assertLogs(logger, level="INFO") as cm:
            api.group.remove_user(groupname="group", username="foo")
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER REMOVED FROM GROUP] id=foo group=group"
                ],
            )

    def test_assign_global_role_to_group(self):
        group = api.group.create(groupname="group")
        self.assertEqual(group.getRoles(), ["Authenticated"])
        with self.assertLogs(logger, level="INFO") as cm:
            api.group.grant_roles(groupname="group", roles=["Manager"])
            self.assertEqual(len(cm.output), 1)
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER ROLE ASSIGNED] "
                    "(<GroupAwareRoleManager at /plone/acl_users/portal_role_manager>, ['Manager'], 'group') {}"
                ],
            )

        # revoke global roles became set new roles
        with self.assertLogs(logger, level="INFO") as cm:
            api.group.revoke_roles(groupname="group", roles=["Manager"])
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER ROLE ASSIGNED] "
                    "(<GroupAwareRoleManager at /plone/acl_users/portal_role_manager>, "
                    "[], 'group') {}"
                ],
            )

    def test_assign_local_role_to_group(self):
        group = api.group.create(groupname="group")
        self.assertEqual(group.getRoles(), ["Authenticated"])
        folder = api.content.create(
            type="Folder",
            title="Folder",
            container=self.portal,
        )
        with self.assertLogs(logger, level="INFO") as cm:
            api.group.grant_roles(groupname="group", roles=["Manager"], obj=folder)
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER LOCALROLE ASSIGNED] (<Folder at /plone/folder>, "
                    "'group', ['Manager']) {}"
                ],
            )

        with self.assertLogs(logger, level="INFO") as cm:
            api.group.revoke_roles(groupname="group", roles=["Manager"], obj=folder)
            self.assertEqual(
                cm.output,
                [
                    "INFO:redturtle.auditlog:[USER LOCALROLE DELETED] (<Folder at /plone/folder>, "
                    "['group']) {}"
                ],
            )
