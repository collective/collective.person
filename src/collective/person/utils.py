from collective.person import logger
from collective.person.behaviors.person import IPersonDataMarker
from plone import api


def reindex_all_person_content(idxs: list[str]):
    """Recatalog Person content items."""
    brains = api.content.find(object_provides=IPersonDataMarker)
    total = len(brains)
    logger.info(f"Will reindex {', '.join(idxs)} for {total} Person objects.")
    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=idxs)
    logger.info(f"Reindexed {total} Person objects.")
