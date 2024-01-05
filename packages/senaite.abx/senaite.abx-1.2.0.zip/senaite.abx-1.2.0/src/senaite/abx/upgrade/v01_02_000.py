# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.ABX.
#
# SENAITE.ABX is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2020-2024 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from senaite.abx import logger
from senaite.abx import PRODUCT_NAME
from senaite.abx.content.antibiotic import Antibiotic
from senaite.core.upgrade import upgradestep
from senaite.core.upgrade.utils import UpgradeUtils

version = "1200"
profile = "profile-{0}:default".format(PRODUCT_NAME)


@upgradestep(PRODUCT_NAME, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup  # noqa
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(PRODUCT_NAME)

    if ut.isOlderVersion(PRODUCT_NAME, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            PRODUCT_NAME, ver_from, version))
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(PRODUCT_NAME, ver_from,
                                                   version))

    # -------- ADD YOUR STUFF BELOW --------

    logger.info("{0} upgraded to version {1}".format(PRODUCT_NAME, version))
    return True


def remove_antibiotic_behavior(tool):
    """Removes IAntibioticBehavior and uses IAntibioticSchema instead
    """
    logger.info("Remove IAntibioticBehavior behavior ...")
    pt = api.get_tool("portal_types")
    fti = pt.get("Antibiotic")

    # set the new schema
    schema = "senaite.abx.content.antibiotic.IAntibioticSchema"
    fti.schema = schema

    # remove behaviors
    behaviors = fti.behaviors
    to_remove = [
        "plone.app.dexterity.behaviors.metadata.IBasic",
        "senaite.abx.behaviors.antibiotic.IAntibioticBehavior",
    ]
    behaviors = filter(lambda b: b not in to_remove, behaviors)

    # Re-assign behaviors
    fti.behaviors = tuple(behaviors)

    # Antibiotic content type is now folderish
    setup = api.get_setup()
    antibiotics = setup.antibiotics
    for antibiotic in antibiotics.objectValues():
        id = antibiotic.getId()
        antibiotics._delOb(id)
        antibiotic.__class__ = Antibiotic
        antibiotics._setOb(id, antibiotic)
        BTreeFolder2Base._initBTrees(antibiotics[id])
        antibiotics[id].reindexObject()

    logger.info("Remove IAntibioticBehavior behavior [DONE]")
