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

from AccessControl import ClassSecurityInfo
from bika.lims import api
from plone.autoform import directives
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.abx import messageFactory as _
from senaite.abx.interfaces import IAntibiotic
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.content.base import Container
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidget
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant


def validly(data, field_name):
    """Returns whether the value from data for the field_name passed in can
    be validated or not
    """
    value = getattr(data, field_name, None)
    if not value:
        return False

    # https://community.plone.org/t/dexterity-unique-field-validation
    context = getattr(data, "__context__", None)
    if context is not None:
        old_value = getattr(context, field_name, None)
        if value == old_value:
            # nothing changed
            return False

    return True


class IAntibioticSchema(model.Schema):
    """Schema interface
    """
    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )

    abbreviation = schema.TextLine(
        title=_(u"Abbreviation"),
        required=True,
    )

    antibiotic_class = UIDReferenceField(
        title=_(u"Antibiotic class"),
        allowed_types=("AntibioticClass", ),
        multi_valued=False,
        required=False,
    )

    directives.widget(
        "antibiotic_class",
        UIDReferenceWidget,
        query={
            "portal_type": "AntibioticClass",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        },
        display_template="<a href='${url}'>${title}</a>",
        columns=[
            {
                "name": "title",
                "label": _(u"column_label_title", default=u"Title"),
            }
        ],
        catalog=SETUP_CATALOG
    )

    @invariant
    def validate_title(data):
        """Checks if the title is unique
        """
        if not validly(data, "title"):
            return

        cat = api.get_tool(SETUP_CATALOG)
        if cat(portal_type="Antibiotic", title=data.title):
            raise Invalid(_("Title must be unique"))

    @invariant
    def validate_abbreviation(data):
        """Checks if the abbreviation is unique
        """
        if not validly(data, "abbreviation"):
            return

        cat = api.get_tool(SETUP_CATALOG)
        for brain in cat(portal_type="Antibiotic"):
            antibiotic = api.get_object(brain)
            if antibiotic.abbreviation == data.abbreviation:
                raise Invalid(_("Abbreviation must be unique"))


@implementer(IAntibiotic, IAntibioticSchema)
class Antibiotic(Container):
    """Antibiotic content
    """
    # Catalogs where this type will be catalogued
    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()
    exclude_from_nav = True

    @security.protected(permissions.View)
    def getAbbreviation(self):
        """Returns the abbreviation of this antibiotic
        """
        accessor = self.accessor("abbreviation")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setAbbreviation(self, value):
        """Sets the abbreviation for this antibiotic
        """
        mutator = self.mutator("abbreviation")
        mutator(self, value)

    @security.protected(permissions.View)
    def getAntibioticClass(self):
        """Returns the Antibiotic class this antibiotic is assigned to
        """
        accessor = self.accessor("antibiotic_class")
        return accessor(self)

    @security.protected(permissions.View)
    def getRawAntibioticClass(self):
        """Returns the UID of the antibiotic class
        """
        accessor = self.accessor("antibiotic_class", raw=True)
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setAntibioticClass(self, value):
        """Sets the antibiotic class for this antibiotic
        """
        mutator = self.mutator("antibiotic_class")
        mutator(self, value)
