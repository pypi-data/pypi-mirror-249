from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .betrag import Betrag
from .kostenposition import Kostenposition


class Kostenblock(BaseModel):
    """
    Mit dieser Komponente werden mehrere Kostenpositionen zusammengefasst.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Kostenblock.svg" type="image/svg+xml"></object>

    .. HINT::
        `Kostenblock JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Kostenblock.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    kostenblockbezeichnung: Annotated[str | None, Field(None, title="Kostenblockbezeichnung")]
    kostenpositionen: Annotated[list[Kostenposition] | None, Field(None, title="Kostenpositionen")]
    summe_kostenblock: Annotated[Betrag | None, Field(None, alias="summeKostenblock")]
