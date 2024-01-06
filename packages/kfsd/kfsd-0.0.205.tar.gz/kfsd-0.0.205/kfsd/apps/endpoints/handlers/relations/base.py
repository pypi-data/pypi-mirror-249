import re
from django.http import Http404
from rest_framework.exceptions import ValidationError

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.constants import OPERATION_ADD
from kfsd.apps.endpoints.handlers.common.base import BaseHandler

from kfsd.apps.models.tables.relations.hierarchy import Hierarchy, HierarchyInit
from kfsd.apps.endpoints.handlers.relations.relation import (
    rm_all_relations,
    add_relation,
    remove_relation,
)
from kfsd.apps.endpoints.handlers.relations.hierarchy_init import (
    rm_all_hierarchies_init,
)


def handle_pre_del_process(instance):
    rm_all_relations(instance)
    rm_all_hierarchies_init(instance)


def handle_pre_save_process(model, instance):
    try:
        obj = model.objects.get(identifier=instance.identifier)
        instance._parent = None
        instance._created_by = None
        if hasattr(obj, "parent"):
            instance._parent = obj.parent

        if hasattr(obj, "created_by"):
            instance._created_by = obj.created_by

    except model.DoesNotExist:
        instance._parent = None
        instance._created_by = None


def handle_post_save_process(instance, created):
    handle_parent_hierarchy(instance, created)
    handle_owner_relation(instance, created)


def handle_owner_relation(instance, created):
    if created:
        if is_created_by_set(instance):
            add_relation(instance.created_by, instance, "role", "owner")
    else:
        if has_created_by_changed(instance):
            if was_created_by_set(instance):
                remove_relation(instance._created_by, instance, "role", "owner")
            if is_created_by_set(instance):
                add_relation(instance.created_by, instance, "role", "owner")


def handle_parent_hierarchy(instance, created):
    if created:
        if is_parent_set(instance):
            add_hierarchy_init(instance.parent, instance)
    else:
        if has_parent_changed(instance):
            if was_parent_set(instance):
                remove_hierarchy_init(instance._parent, instance)
            if is_parent_set(instance):
                add_hierarchy_init(instance.parent, instance)


def is_parent_new(instance):
    if not instance._parent and instance.parent:
        return True
    return False


def has_parent_changed(instance):
    if instance._parent != instance.parent:
        return True
    return False


def is_parent_set(instance):
    if instance.parent:
        return True
    return False


def was_parent_set(instance):
    if instance._parent:
        return True
    return False


def is_created_by_set(instance):
    if instance.created_by:
        return True
    return False


def has_created_by_changed(instance):
    if instance._created_by != instance.created_by:
        return True
    return False


def was_created_by_set(instance):
    if instance._created_by:
        return True
    return False


def add_hierarchy_init(parent, child):
    relationsQS = HierarchyInit.objects.filter(parent=parent, child=child)
    if not relationsQS:
        HierarchyInit.objects.create(
            parent=parent,
            child=child,
            parent_type=parent.type,
            child_type=child.type,
        )


def remove_hierarchy_init(parent, child):
    relationsQS = HierarchyInit.objects.filter(parent=parent, child=child)
    if relationsQS:
        for relation in relationsQS:
            relation.delete()


class BaseHRelHandler(BaseHandler):
    HIERARCHY_INIT = "hierarchy_init"
    CHILDREN = "children"
    PARENTS = "parents"
    CHILD = "child"
    PARENT = "parent"

    def __init__(self, **kwargs):
        BaseHandler.__init__(self, **kwargs)

    def getHierarchyInit(self):
        return DictUtils.get(self.getModelQSData(), self.HIERARCHY_INIT)

    def getChildren(self):
        return DictUtils.get(self.getModelQSData(), self.CHILDREN)

    def getParents(self):
        return DictUtils.get(self.getModelQSData(), self.PARENTS)

    def getRelationQS(self, relationTbl, parentQS, childQS):
        return relationTbl.objects.filter(parent=parentQS, child=childQS)

    def createRelation(self, relationTbl, **kwargs):
        relationTbl.objects.create(**kwargs)

    def removeRelation(self, relationQS):
        relationQS.delete()

    def clearRelations(self, relationTbl):
        entriesQS = relationTbl.objects.filter(parent=self.getModelQS())
        entriesQS.delete()

    def upsertRelation(self, relationTbl, targetQS, operation):
        fieldChanged = False
        relationQS = self.getRelationQS(relationTbl, self.getModelQS(), targetQS)
        if operation == OPERATION_ADD:
            if not relationQS:
                self.createRelation(
                    relationTbl,
                    parent=self.getModelQS(),
                    child=targetQS,
                    parent_type=self.getModelQS().type,
                    child_type=targetQS.type,
                )
                fieldChanged = True
        else:
            if not relationQS:
                raise Http404
            self.removeRelation(relationQS)
            fieldChanged = True
        return fieldChanged

    def getUniqIdentifierRegex(self):
        # extend later
        return None

    def applyUniqIdentifierRegex(self, identifier):
        regex = self.getUniqIdentifierRegex()
        if regex:
            return re.sub(regex, "", identifier)
        return identifier

    def getParentIdentifiers(self):
        parents = self.getParents()
        parentIds = []
        for parentData in parents:
            parentId = parentData[self.PARENT]
            parentIds.append(self.applyUniqIdentifierRegex(parentId))
        return parentIds

    def isValidHierarchyInitRelation(self, targetQS, operation):
        if self.applyUniqIdentifierRegex(
            self.getIdentifier()
        ) == self.applyUniqIdentifierRegex(targetQS.identifier):
            raise ValidationError(
                "Circular depedency error, cannot add hierarchy to the same object: {}".format(
                    self.getIdentifier()
                )
            )

        if (
            operation == OPERATION_ADD
            and self.applyUniqIdentifierRegex(targetQS.identifier)
            in self.getParentIdentifiers()
        ):
            raise ValidationError(
                "Circular dependency error, obj: {} uses obj: {}".format(
                    self.getIdentifier(), targetQS.identifier
                )
            )

    def upsertHierarchyInit(self, targetQS, operation):
        self.isValidHierarchyInitRelation(targetQS, operation)
        fieldChanged = self.upsertRelation(HierarchyInit, targetQS, operation)
        return {"detail": fieldChanged}

    def populateChildren(self, store):
        childIdentifiers = [child[self.CHILD] for child in store]
        childIdentifiersQS = self.getIdentifiersQS(childIdentifiers)
        for targetQS in childIdentifiersQS:
            self.upsertRelation(Hierarchy, targetQS, OPERATION_ADD)

    def generateChildren(self, store):
        from kfsd.apps.endpoints.handlers.relations.hrel import HRelHandler

        hierarchyInitData = self.getHierarchyInit()
        for hierarchy in hierarchyInitData:
            childDataHandler = HRelHandler(hierarchy[self.CHILD], True)
            store += childDataHandler.getChildren()
            store.append(hierarchy)

    def updateParentsChildren(self):
        from kfsd.apps.endpoints.handlers.relations.hrel import HRelHandler

        parents = self.getParentIdentifiers()
        for parentIdentifier in parents:
            if self.getIdentifier() != parentIdentifier:
                parentHandler = HRelHandler(parentIdentifier, True)
                parentHandler.refreshHierarchy()

    def refreshHierarchy(self):
        self.clearRelations(Hierarchy)
        self.refreshModelQSData()
        store = []
        self.generateChildren(store)
        self.populateChildren(store)
        self.refreshModelQSData()
        self.updateParentsChildren()
