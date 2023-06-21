from collective.person import _
from collective.person.controlpanel.interfaces import IPersonSettings
from collective.person.interfaces import IPersonLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


class SettingsEditForm(RegistryEditForm):
    schema = IPersonSettings
    schema_prefix = "person"
    label = "Person Settings"


class SettingsControlPanelFormWrapper(ControlPanelFormWrapper):
    form = SettingsEditForm


@adapter(Interface, IPersonLayer)
class SettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IPersonSettings
    configlet_id = "person"
    configlet_category_id = "Products"
    title = _("Person Settings")
    group = "Products"
    schema_prefix = "person"
