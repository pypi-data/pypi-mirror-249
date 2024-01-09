from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.mengeneinheit import Mengeneinheit
from ..enum.preistyp import Preistyp
from ..enum.waehrungseinheit import Waehrungseinheit
from .preisstaffel import Preisstaffel


class Tarifpreisposition(BaseModel):
    """
    Mit dieser Komponente können Tarifpreise verschiedener Typen abgebildet werden.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Tarifpreisposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Tarifpreisposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Tarifpreisposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bezugseinheit: Mengeneinheit | None = None
    einheit: Waehrungseinheit | None = None
    mengeneinheitstaffel: Mengeneinheit | None = None
    preisstaffeln: Annotated[list[Preisstaffel] | None, Field(None, title="Preisstaffeln")]
    preistyp: Preistyp | None = None
