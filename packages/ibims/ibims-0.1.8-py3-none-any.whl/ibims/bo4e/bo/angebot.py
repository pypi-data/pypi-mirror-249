from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..com.angebotsvariante import Angebotsvariante
from ..com.externe_referenz import ExterneReferenz
from ..enum.bo_typ import BoTyp
from ..enum.sparte import Sparte
from .ansprechpartner import Ansprechpartner
from .geschaeftspartner import Geschaeftspartner


class Angebot(BaseModel):
    """
    Mit diesem BO kann ein Versorgungsangebot zur Strom- oder Gasversorgung oder die Teilnahme an einer Ausschreibung
    übertragen werden. Es können verschiedene Varianten enthalten sein (z.B. ein- und mehrjährige Laufzeit).
    Innerhalb jeder Variante können Teile enthalten sein, die jeweils für eine oder mehrere Marktlokationen erstellt
    werden.

    .. raw:: html

        <object data="../_static/images/bo4e/bo/Angebot.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebot JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/bo/Angebot.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    anfragereferenz: Annotated[str | None, Field(None, title="Anfragereferenz")]
    angebotsdatum: Annotated[AwareDatetime | None, Field(None, title="Angebotsdatum")]
    angebotsgeber: Geschaeftspartner | None = None
    angebotsnehmer: Geschaeftspartner | None = None
    angebotsnummer: Annotated[str | None, Field(None, title="Angebotsnummer")]
    bindefrist: Annotated[AwareDatetime | None, Field(None, title="Bindefrist")]
    bo_typ: Annotated[BoTyp | None, Field(BoTyp.ANGEBOT, alias="boTyp")]
    externe_referenzen: Annotated[
        list[ExterneReferenz] | None, Field(None, alias="externeReferenzen", title="Externereferenzen")
    ]
    sparte: Sparte | None = None
    unterzeichner_angebotsgeber: Annotated[Ansprechpartner | None, Field(None, alias="unterzeichnerAngebotsgeber")]
    unterzeichner_angebotsnehmer: Annotated[Ansprechpartner | None, Field(None, alias="unterzeichnerAngebotsnehmer")]
    varianten: Annotated[list[Angebotsvariante] | None, Field(None, title="Varianten")]
    versionstruktur: Annotated[str | None, Field("2", title="Versionstruktur")]
