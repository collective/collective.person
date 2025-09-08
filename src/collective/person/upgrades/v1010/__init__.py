from collective.person import logger
from collective.person.behaviors.person import IPersonData
from plone import api
from Products.GenericSetup.tool import SetupTool


def reindex_persons(context: SetupTool):
    """Reindex all Person objects to update the  index."""
    idxs = ["sortable_title", "Title", "SearchableText", "object_provides"]
    brains = api.content.find(object_provides=IPersonData)
    total = len(brains)
    logger.info(f"Will reindex {', '.join(idxs)} for {total} Person objects.")
    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=idxs)
    logger.info(f"Reindexed {total} Person objects.")
