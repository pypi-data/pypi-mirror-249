"""
BO4E vunknown - Generated Python implementation of the BO4E standard

BO4E is a standard for the exchange of business objects in the energy industry.
All our software used to generate this BO4E-implementation is open-source and released under the Apache-2.0 license.

The BO4E version can be queried using `bo4e.__version__`.
"""

__all__ = [
    "Angebot",
    "Ansprechpartner",
    "Ausschreibung",
    "Bilanzierung",
    "Buendelvertrag",
    "Dokument",
    "Energiemenge",
    "File",
    "Fremdkosten",
    "Geschaeftsobjekt",
    "Geschaeftspartner",
    "Hinweis",
    "Kampagne",
    "Kosten",
    "Lastgang",
    "LastgangKompakt",
    "Marktlokation",
    "Marktteilnehmer",
    "Messlokation",
    "Netznutzungsrechnung",
    "Preisblatt",
    "PreisblattDienstleistung",
    "PreisblattHardware",
    "PreisblattKonzessionsabgabe",
    "PreisblattMessung",
    "PreisblattNetznutzung",
    "Rechnung",
    "Region",
    "Regionaltarif",
    "Standorteigenschaften",
    "Tarif",
    "Tarifinfo",
    "Tarifkosten",
    "Tarifpreisblatt",
    "Vertrag",
    "Zaehler",
    "ZaehlerGas",
    "Zeitreihe",
    "Adresse",
    "Angebotsposition",
    "Angebotsteil",
    "Angebotsvariante",
    "AufAbschlag",
    "AufAbschlagProOrt",
    "AufAbschlagRegional",
    "AufAbschlagstaffelProOrt",
    "Ausschreibungsdetail",
    "Ausschreibungslos",
    "Bankverbindung",
    "Betrag",
    "COM",
    "ConcessionFee",
    "Dienstleistung",
    "Energieherkunft",
    "Energiemix",
    "ExterneReferenz",
    "Fremdkostenblock",
    "Fremdkostenposition",
    "Geokoordinaten",
    "Geraet",
    "Geraeteeigenschaften",
    "Hardware",
    "Katasteradresse",
    "Kostenblock",
    "Kostenposition",
    "KriteriumWert",
    "Lastprofil",
    "MarktgebietInfo",
    "Menge",
    "Messlokationszuordnung",
    "PositionsAufAbschlag",
    "Preis",
    "Preisgarantie",
    "Preisposition",
    "Preisstaffel",
    "Rechnungsposition",
    "RegionaleGueltigkeit",
    "RegionalePreisgarantie",
    "RegionalePreisstaffel",
    "RegionalerAufAbschlag",
    "RegionaleTarifpreisposition",
    "Regionskriterium",
    "Rufnummer",
    "SepaInfo",
    "Sigmoidparameter",
    "StandorteigenschaftenGas",
    "StandorteigenschaftenStrom",
    "Steuerbetrag",
    "Tagesvektor",
    "Tarifberechnungsparameter",
    "Tarifeinschraenkung",
    "Tarifpreis",
    "Tarifpreisposition",
    "TarifpreispositionProOrt",
    "TarifpreisstaffelProOrt",
    "Unterschrift",
    "Verbrauch",
    "Vertragskonditionen",
    "Vertragskonto",
    "VertragskontoCBA",
    "VertragskontoMBA",
    "Vertragsteil",
    "Zaehlpunkt",
    "Zaehlwerk",
    "Zeitintervall",
    "Zeitraum",
    "Zeitreihenwert",
    "Zeitreihenwertkompakt",
    "Zustaendigkeit",
    "Abgabeart",
    "AblesendeRolle",
    "Ablesungsstatus",
    "Aggregationsverantwortung",
    "Angebotsstatus",
    "Anrede",
    "ArithmetischeOperation",
    "ArtikelId",
    "AufAbschlagstyp",
    "AufAbschlagsziel",
    "Ausschreibungsportal",
    "Ausschreibungsstatus",
    "Ausschreibungstyp",
    "BDEWArtikelnummer",
    "Bemessungsgroesse",
    "Bilanzierungsmethode",
    "BoTyp",
    "Dienstleistungstyp",
    "Energierichtung",
    "Erzeugungsart",
    "Gasqualitaet",
    "Gebiettyp",
    "Geraetemerkmal",
    "Geraetetyp",
    "Geschaeftspartnerrolle",
    "Gueltigkeitstyp",
    "HinweisThema",
    "Kalkulationsmethode",
    "Kontaktart",
    "Kostenklasse",
    "Kundengruppe",
    "KundengruppeKA",
    "Kundentyp",
    "Landescode",
    "Leistungstyp",
    "Lokationstyp",
    "Marktgebiet",
    "Marktrolle",
    "Medium",
    "Mengeneinheit",
    "Mengenoperator",
    "Messart",
    "Messgroesse",
    "Messpreistyp",
    "MesstechnischeEinordnung",
    "Messwerterfassung",
    "Messwertstatus",
    "Messwertstatuszusatz",
    "Netzebene",
    "NNRechnungsart",
    "NNRechnungstyp",
    "Oekolabel",
    "Oekozertifikat",
    "Preisgarantietyp",
    "Preismodell",
    "Preisstatus",
    "Preistyp",
    "Profiltyp",
    "Prognosegrundlage",
    "Rechnungslegung",
    "Rechnungsstatus",
    "Rechnungstyp",
    "Regelzone",
    "Regionskriteriumtyp",
    "Rollencodetyp",
    "Rufnummernart",
    "Sparte",
    "Steuerkennzeichen",
    "Tarifart",
    "Tarifkalkulationsmethode",
    "Tarifmerkmal",
    "Tarifregionskriterium",
    "Tariftyp",
    "Tarifzeit",
    "Themengebiet",
    "Titel",
    "Variant",
    "Verbrauchsart",
    "Vertragsart",
    "Vertragsform",
    "Vertragsstatus",
    "Voraussetzungen",
    "Waehrungscode",
    "Waehrungseinheit",
    "Wertermittlungsverfahren",
    "Zaehlerauspraegung",
    "Zaehlertyp",
    "Zeiteinheit",
    "__version__",
]

from .__version__ import __version__
from .bo.angebot import Angebot
from .bo.ansprechpartner import Ansprechpartner
from .bo.ausschreibung import Ausschreibung
from .bo.bilanzierung import Bilanzierung
from .bo.buendelvertrag import Buendelvertrag
from .bo.dokument import Dokument
from .bo.energiemenge import Energiemenge
from .bo.file import File
from .bo.fremdkosten import Fremdkosten
from .bo.geschaeftsobjekt import Geschaeftsobjekt
from .bo.geschaeftspartner import Geschaeftspartner
from .bo.hinweis import Hinweis
from .bo.kampagne import Kampagne
from .bo.kosten import Kosten
from .bo.lastgang import Lastgang
from .bo.lastgang_kompakt import LastgangKompakt
from .bo.marktlokation import Marktlokation
from .bo.marktteilnehmer import Marktteilnehmer
from .bo.messlokation import Messlokation
from .bo.netznutzungsrechnung import Netznutzungsrechnung
from .bo.preisblatt import Preisblatt
from .bo.preisblatt_dienstleistung import PreisblattDienstleistung
from .bo.preisblatt_hardware import PreisblattHardware
from .bo.preisblatt_konzessionsabgabe import PreisblattKonzessionsabgabe
from .bo.preisblatt_messung import PreisblattMessung
from .bo.preisblatt_netznutzung import PreisblattNetznutzung
from .bo.rechnung import Rechnung
from .bo.region import Region
from .bo.regionaltarif import Regionaltarif
from .bo.standorteigenschaften import Standorteigenschaften
from .bo.tarif import Tarif
from .bo.tarifinfo import Tarifinfo
from .bo.tarifkosten import Tarifkosten
from .bo.tarifpreisblatt import Tarifpreisblatt
from .bo.vertrag import Vertrag
from .bo.zaehler import Zaehler
from .bo.zaehler_gas import ZaehlerGas
from .bo.zeitreihe import Zeitreihe
from .com.adresse import Adresse
from .com.angebotsposition import Angebotsposition
from .com.angebotsteil import Angebotsteil
from .com.angebotsvariante import Angebotsvariante
from .com.auf_abschlag import AufAbschlag
from .com.auf_abschlag_pro_ort import AufAbschlagProOrt
from .com.auf_abschlag_regional import AufAbschlagRegional
from .com.auf_abschlagstaffel_pro_ort import AufAbschlagstaffelProOrt
from .com.ausschreibungsdetail import Ausschreibungsdetail
from .com.ausschreibungslos import Ausschreibungslos
from .com.bankverbindung import Bankverbindung
from .com.betrag import Betrag
from .com.com import COM
from .com.concession_fee import ConcessionFee
from .com.dienstleistung import Dienstleistung
from .com.energieherkunft import Energieherkunft
from .com.energiemix import Energiemix
from .com.externe_referenz import ExterneReferenz
from .com.fremdkostenblock import Fremdkostenblock
from .com.fremdkostenposition import Fremdkostenposition
from .com.geokoordinaten import Geokoordinaten
from .com.geraet import Geraet
from .com.geraeteeigenschaften import Geraeteeigenschaften
from .com.hardware import Hardware
from .com.katasteradresse import Katasteradresse
from .com.kostenblock import Kostenblock
from .com.kostenposition import Kostenposition
from .com.kriterium_wert import KriteriumWert
from .com.lastprofil import Lastprofil
from .com.marktgebiet_info import MarktgebietInfo
from .com.menge import Menge
from .com.messlokationszuordnung import Messlokationszuordnung
from .com.positions_auf_abschlag import PositionsAufAbschlag
from .com.preis import Preis
from .com.preisgarantie import Preisgarantie
from .com.preisposition import Preisposition
from .com.preisstaffel import Preisstaffel
from .com.rechnungsposition import Rechnungsposition
from .com.regionale_gueltigkeit import RegionaleGueltigkeit
from .com.regionale_preisgarantie import RegionalePreisgarantie
from .com.regionale_preisstaffel import RegionalePreisstaffel
from .com.regionale_tarifpreisposition import RegionaleTarifpreisposition
from .com.regionaler_auf_abschlag import RegionalerAufAbschlag
from .com.regionskriterium import Regionskriterium
from .com.rufnummer import Rufnummer
from .com.sepa_info import SepaInfo
from .com.sigmoidparameter import Sigmoidparameter
from .com.standorteigenschaften_gas import StandorteigenschaftenGas
from .com.standorteigenschaften_strom import StandorteigenschaftenStrom
from .com.steuerbetrag import Steuerbetrag
from .com.tagesvektor import Tagesvektor
from .com.tarifberechnungsparameter import Tarifberechnungsparameter
from .com.tarifeinschraenkung import Tarifeinschraenkung
from .com.tarifpreis import Tarifpreis
from .com.tarifpreisposition import Tarifpreisposition
from .com.tarifpreisposition_pro_ort import TarifpreispositionProOrt
from .com.tarifpreisstaffel_pro_ort import TarifpreisstaffelProOrt
from .com.unterschrift import Unterschrift
from .com.verbrauch import Verbrauch
from .com.vertragskonditionen import Vertragskonditionen
from .com.vertragskonto import Vertragskonto
from .com.vertragskonto_cba import VertragskontoCBA
from .com.vertragskonto_mba import VertragskontoMBA
from .com.vertragsteil import Vertragsteil
from .com.zaehlpunkt import Zaehlpunkt
from .com.zaehlwerk import Zaehlwerk
from .com.zeitintervall import Zeitintervall
from .com.zeitraum import Zeitraum
from .com.zeitreihenwert import Zeitreihenwert
from .com.zeitreihenwertkompakt import Zeitreihenwertkompakt
from .com.zustaendigkeit import Zustaendigkeit
from .enum.abgabeart import Abgabeart
from .enum.ablesende_rolle import AblesendeRolle
from .enum.ablesungsstatus import Ablesungsstatus
from .enum.aggregationsverantwortung import Aggregationsverantwortung
from .enum.angebotsstatus import Angebotsstatus
from .enum.anrede import Anrede
from .enum.arithmetische_operation import ArithmetischeOperation
from .enum.artikel_id import ArtikelId
from .enum.auf_abschlagstyp import AufAbschlagstyp
from .enum.auf_abschlagsziel import AufAbschlagsziel
from .enum.ausschreibungsportal import Ausschreibungsportal
from .enum.ausschreibungsstatus import Ausschreibungsstatus
from .enum.ausschreibungstyp import Ausschreibungstyp
from .enum.bdew_artikelnummer import BDEWArtikelnummer
from .enum.bemessungsgroesse import Bemessungsgroesse
from .enum.bilanzierungsmethode import Bilanzierungsmethode
from .enum.bo_typ import BoTyp
from .enum.dienstleistungstyp import Dienstleistungstyp
from .enum.energierichtung import Energierichtung
from .enum.erzeugungsart import Erzeugungsart
from .enum.gasqualitaet import Gasqualitaet
from .enum.gebiettyp import Gebiettyp
from .enum.geraetemerkmal import Geraetemerkmal
from .enum.geraetetyp import Geraetetyp
from .enum.geschaeftspartnerrolle import Geschaeftspartnerrolle
from .enum.gueltigkeitstyp import Gueltigkeitstyp
from .enum.hinweis_thema import HinweisThema
from .enum.kalkulationsmethode import Kalkulationsmethode
from .enum.kontaktart import Kontaktart
from .enum.kostenklasse import Kostenklasse
from .enum.kundengruppe import Kundengruppe
from .enum.kundengruppe_ka import KundengruppeKA
from .enum.kundentyp import Kundentyp
from .enum.landescode import Landescode
from .enum.leistungstyp import Leistungstyp
from .enum.lokationstyp import Lokationstyp
from .enum.marktgebiet import Marktgebiet
from .enum.marktrolle import Marktrolle
from .enum.medium import Medium
from .enum.mengeneinheit import Mengeneinheit
from .enum.mengenoperator import Mengenoperator
from .enum.messart import Messart
from .enum.messgroesse import Messgroesse
from .enum.messpreistyp import Messpreistyp
from .enum.messtechnische_einordnung import MesstechnischeEinordnung
from .enum.messwerterfassung import Messwerterfassung
from .enum.messwertstatus import Messwertstatus
from .enum.messwertstatuszusatz import Messwertstatuszusatz
from .enum.netzebene import Netzebene
from .enum.nn_rechnungsart import NNRechnungsart
from .enum.nn_rechnungstyp import NNRechnungstyp
from .enum.oekolabel import Oekolabel
from .enum.oekozertifikat import Oekozertifikat
from .enum.preisgarantietyp import Preisgarantietyp
from .enum.preismodell import Preismodell
from .enum.preisstatus import Preisstatus
from .enum.preistyp import Preistyp
from .enum.profiltyp import Profiltyp
from .enum.prognosegrundlage import Prognosegrundlage
from .enum.rechnungslegung import Rechnungslegung
from .enum.rechnungsstatus import Rechnungsstatus
from .enum.rechnungstyp import Rechnungstyp
from .enum.regelzone import Regelzone
from .enum.regionskriteriumtyp import Regionskriteriumtyp
from .enum.rollencodetyp import Rollencodetyp
from .enum.rufnummernart import Rufnummernart
from .enum.sparte import Sparte
from .enum.steuerkennzeichen import Steuerkennzeichen
from .enum.tarifart import Tarifart
from .enum.tarifkalkulationsmethode import Tarifkalkulationsmethode
from .enum.tarifmerkmal import Tarifmerkmal
from .enum.tarifregionskriterium import Tarifregionskriterium
from .enum.tariftyp import Tariftyp
from .enum.tarifzeit import Tarifzeit
from .enum.themengebiet import Themengebiet
from .enum.titel import Titel
from .enum.variant import Variant
from .enum.verbrauchsart import Verbrauchsart
from .enum.vertragsart import Vertragsart
from .enum.vertragsform import Vertragsform
from .enum.vertragsstatus import Vertragsstatus
from .enum.voraussetzungen import Voraussetzungen
from .enum.waehrungscode import Waehrungscode
from .enum.waehrungseinheit import Waehrungseinheit
from .enum.wertermittlungsverfahren import Wertermittlungsverfahren
from .enum.zaehlerauspraegung import Zaehlerauspraegung
from .enum.zaehlertyp import Zaehlertyp
from .enum.zeiteinheit import Zeiteinheit
