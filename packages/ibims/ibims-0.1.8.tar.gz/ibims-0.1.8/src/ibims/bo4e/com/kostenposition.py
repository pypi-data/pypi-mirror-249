from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .betrag import Betrag
from .menge import Menge
from .preis import Preis


class Kostenposition(BaseModel):
    """
    Diese Komponente wird zur Übertagung der Details zu einer Kostenposition verwendet.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Kostenposition.svg" type="image/svg+xml"></object>

    .. HINT::
        `Kostenposition JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Kostenposition.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    artikelbezeichnung: Annotated[str | None, Field(None, title="Artikelbezeichnung")]
    artikeldetail: Annotated[str | None, Field(None, title="Artikeldetail")]
    betrag_kostenposition: Annotated[Betrag | None, Field(None, alias="betragKostenposition")]
    bis: Annotated[AwareDatetime | None, Field(None, title="Bis")]
    einzelpreis: Preis | None = None
    menge: Menge | None = None
    positionstitel: Annotated[str | None, Field(None, title="Positionstitel")]
    von: Annotated[AwareDatetime | None, Field(None, title="Von")]
    zeitmenge: Menge | None = None
