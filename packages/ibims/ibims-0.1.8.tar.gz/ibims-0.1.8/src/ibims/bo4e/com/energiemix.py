from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.oekolabel import Oekolabel
from ..enum.oekozertifikat import Oekozertifikat
from ..enum.sparte import Sparte
from .energieherkunft import Energieherkunft


class Energiemix(BaseModel):
    """
    Zusammensetzung der gelieferten Energie aus den verschiedenen Primärenergieformen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Energiemix.svg" type="image/svg+xml"></object>

    .. HINT::
        `Energiemix JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Energiemix.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    anteil: Annotated[list[Energieherkunft] | None, Field(None, title="Anteil")]
    atommuell: Annotated[float | str | None, Field(None, title="Atommuell")]
    bemerkung: Annotated[str | None, Field(None, title="Bemerkung")]
    bezeichnung: Annotated[str | None, Field(None, title="Bezeichnung")]
    co2_emission: Annotated[float | str | None, Field(None, alias="co2Emission", title="Co2Emission")]
    energieart: Sparte | None = None
    energiemixnummer: Annotated[int | None, Field(None, title="Energiemixnummer")]
    gueltigkeitsjahr: Annotated[int | None, Field(None, title="Gueltigkeitsjahr")]
    oeko_top_ten: Annotated[bool | None, Field(None, alias="oekoTopTen", title="Oekotopten")]
    oekolabel: Annotated[list[Oekolabel] | None, Field(None, title="Oekolabel")]
    oekozertifikate: Annotated[list[Oekozertifikat] | None, Field(None, title="Oekozertifikate")]
    website: Annotated[str | None, Field(None, title="Website")]
