# -*- coding: utf-8 -*-
"""Init and utils."""
from .monkeys import patches
from zope.i18nmessageid import MessageFactory

import logging


_ = MessageFactory("redturtle.auditlog")
logger = logging.getLogger(__name__)

patches()
