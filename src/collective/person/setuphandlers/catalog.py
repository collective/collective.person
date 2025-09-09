from collective.person.utils import reindex_all_person_content
from Products.GenericSetup.tool import SetupTool


def reindex_persons(context: SetupTool):
    """Recatalog all person content to add metadata columns."""
    idxs = ["contact_email", "contact_phone", "contact_website"]
    reindex_all_person_content(idxs)
