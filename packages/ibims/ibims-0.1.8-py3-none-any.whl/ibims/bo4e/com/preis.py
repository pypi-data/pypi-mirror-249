from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.mengeneinheit import Mengeneinheit
from ..enum.preisstatus import Preisstatus
from ..enum.waehrungseinheit import Waehrungseinheit


class Preis(BaseModel):
    """
    Abbildung eines Preises mit Wert, Einheit, Bezugswert und Status.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Preis.svg" type="image/svg+xml"></object>

    .. HINT::
        `Preis JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Preis.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    bezugswert: Mengeneinheit | None = None
    einheit: Waehrungseinheit | None = None
    status: Preisstatus | None = None
    wert: Annotated[float | str | None, Field(None, title="Wert")]
