# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import redturtle.auditlog


class RedturtleAuditlogLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.auditlog)

    # def setUpPloneSite(self, portal):
    #     applyProfile(portal, 'redturtle.auditlog:default')


REDTURTLE_AUDITLOG_FIXTURE = RedturtleAuditlogLayer()


REDTURTLE_AUDITLOG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_AUDITLOG_FIXTURE,),
    name="RedturtleAuditlogLayer:IntegrationTesting",
)


REDTURTLE_AUDITLOG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_AUDITLOG_FIXTURE,),
    name="RedturtleAuditlogLayer:FunctionalTesting",
)
