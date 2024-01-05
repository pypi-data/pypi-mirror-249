"""Buy starting materials process."""

from typing import ClassVar

from gemd import (
    ProcessTemplate,
    ParameterTemplate,
    CategoricalBounds,
    NominalCategorical,
)

from openmsimodel.entity.gemd.process import Process
from openmsimodel.utilities.attributes import (
    AttrsDict,
    define_attribute,
    finalize_template,
)

__all__ = ["BuyStartingMaterials"]


class BuyStartingMaterials(Process):
    """Class representing the purchase of a starting material from a supplier."""

    TEMPLATE: ClassVar[ProcessTemplate] = ProcessTemplate(name=__name__)

    _ATTRS: ClassVar[AttrsDict] = {"conditions": {}, "parameters": {}}

    define_attribute(
        _ATTRS,
        template=ParameterTemplate(
            name="Supplier", bounds=CategoricalBounds(categories=[""])
        ),
        default_value=NominalCategorical(""),
    )

    finalize_template(_ATTRS, TEMPLATE)
