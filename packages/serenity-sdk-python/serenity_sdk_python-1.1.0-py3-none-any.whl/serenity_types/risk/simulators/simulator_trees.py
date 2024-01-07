"""
Entity tree nodes specify nodes for entity trees.
"""

from typing import List, Optional

from pydantic import Field
from serenity_types.risk.simulators.entities import EntityId
from serenity_types.utils.serialization import CamelModel


class EntityTreeNode(CamelModel):
    """
    Trees are composed of nodes that are either leaves or have children.
    Each node has a mandatory entity_id field that reference an existing entity object.
    The entity_id should be unique within a tree, however, it could belong to multiple trees.
    Most commonly used with simulator contributors.
    """

    entity_id: EntityId = Field(..., allow_mutation=False)
    """
    The id of the entity that is related to this node.
    This is usually a the id of a simulator contributor.
    """

    children: List["EntityTreeNode"] = Field(allow_mutation=False, default_factory=list)
    """
    The list of node children.
    If there is at least one child, then the node is either a branch or the root node.
    If this list is empty, then the node is a leaf.
    """

    label: Optional[str]
    """
    An optional user-readble label that can help the user to identify the node.
    In the case of simulator contributors, this is usually the string associated with the contributor type.
    """

    class Config:
        """
        Pydantic configuration: we vaildate the assignments so that the fields cannot be changed after creation.
        """

        validate_assignment = True


# Used to resolve the forward reference in the children field.
# (Needed in older versions of Python. Not needed in Python 3.11+.)
EntityTreeNode.update_forward_refs()
