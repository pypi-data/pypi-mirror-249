from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .betrag import Betrag
from .fremdkostenposition import Fremdkostenposition


class Fremdkostenblock(BaseModel):
    """
    Komponente zur Abbildung eines Kostenblocks in den Fremdkosten

    .. raw:: html

        <object data="../_static/images/bo4e/com/Fremdkostenblock.svg" type="image/svg+xml"></object>

    .. HINT::
        `Fremdkostenblock JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Fremdkostenblock.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    kostenblockbezeichnung: Annotated[str | None, Field(None, title="Kostenblockbezeichnung")]
    kostenpositionen: Annotated[list[Fremdkostenposition] | None, Field(None, title="Kostenpositionen")]
    summe_kostenblock: Annotated[Betrag | None, Field(None, alias="summeKostenblock")]
