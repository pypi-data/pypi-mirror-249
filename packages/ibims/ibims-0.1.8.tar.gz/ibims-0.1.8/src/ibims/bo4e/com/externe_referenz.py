from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class ExterneReferenz(BaseModel):
    """
    Viele Datenobjekte weisen in unterschiedlichen Systemen eine eindeutige ID (Kundennummer, GP-Nummer etc.) auf.
    Beim Austausch von Datenobjekten zwischen verschiedenen Systemen ist es daher hilfreich,
    sich die eindeutigen IDs der anzubindenden Systeme zu merken.

    .. raw:: html

        <object data="../_static/images/bo4e/com/ExterneReferenz.svg" type="image/svg+xml"></object>

    .. HINT::
        `ExterneReferenz JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/ExterneReferenz.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    ex_ref_name: Annotated[str | None, Field(None, alias="exRefName", title="Exrefname")]
    ex_ref_wert: Annotated[str | None, Field(None, alias="exRefWert", title="Exrefwert")]
