from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.mengeneinheit import Mengeneinheit


class Zaehlpunkt(BaseModel):
    """
    The zaehlpunkt object was created during a migration project.
    It contains attributes needed for metering mapping.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    periodenverbrauch_vorhersage: Annotated[
        float | str, Field(alias="periodenverbrauchVorhersage", title="Periodenverbrauchvorhersage")
    ]
    einheit_vorhersage: Annotated[Mengeneinheit | None, Field(Mengeneinheit.KWH, alias="einheitVorhersage")]
    zeitreihentyp: Annotated[str | None, Field("Z21", title="Zeitreihentyp")]
    kunden_wert: Annotated[float | str | None, Field(alias="kundenWert", title="Kundenwert")]
    einheit_kunde: Annotated[Mengeneinheit | None, Field(None, alias="einheitKunde")]
    grundzustaendiger: Annotated[bool | None, Field(True, title="Grundzustaendiger")]
