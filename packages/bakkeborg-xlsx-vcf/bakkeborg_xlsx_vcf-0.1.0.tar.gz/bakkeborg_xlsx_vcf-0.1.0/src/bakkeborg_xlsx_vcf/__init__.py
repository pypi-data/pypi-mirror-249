import dataclasses
import pathlib
import re
from datetime import datetime
from itertools import islice
from typing import Literal, overload

import openpyxl
from openpyxl.cell.cell import Cell

# region XLSX Helpers


def parse_opt_str(cell: Cell) -> str | None:
    """Parse a cell from the xlsx file and return a string"""
    if cell.value is None:
        return None
    if isinstance(cell.value, str):
        if cell.value == "":
            return None
        return cell.value
    raise ValueError(f"Expected str, got {type(cell.value)} at {cell.coordinate}")


def parse_str(cell: Cell) -> str:
    """Parse a cell from the xlsx file and return a string"""
    if isinstance(cell.value, str):
        return cell.value
    raise ValueError(f"Expected str, got {type(cell.value)} at {cell.coordinate}")


def parse_int(cell: Cell) -> int:
    """Parse a cell from the xlsx file and return a int"""
    if isinstance(cell.value, int):
        return cell.value
    raise ValueError(f"Expected int, got {type(cell.value)} at {cell.coordinate}")


def parse_bool(cell: Cell) -> bool:
    """Parse a cell from the xlsx file and return a bool"""
    return cell.value == "x"


def parse_date(cell: Cell) -> datetime:
    """Parse a cell from the xlsx file and return a datetime"""
    if isinstance(cell.value, datetime):
        return cell.value
    raise ValueError(f"Expected datetime, got {type(cell.value)} at {cell.coordinate}")


def parse_opt_date(cell: Cell) -> datetime | None:
    """Parse a cell from the xlsx file and return a datetime"""
    if cell.value is None:
        return None
    if isinstance(cell.value, datetime):
        return cell.value
    raise ValueError(f"Expected datetime, got {type(cell.value)} at {cell.coordinate}")


# endregion


@dataclasses.dataclass(frozen=True, slots=True)
class Person:
    navn_fuld: str
    navn_alt: str | None
    navn: str
    mail: str | None
    addresse: str

    @property
    def fornavn(self) -> str:
        return self.navn_fuld.split(" ")[0]

    @property
    def efternavn(self) -> str:
        return self.navn_fuld.split(" ")[-1]

    @property
    def mellemnavne(self) -> str:
        return ",".join(self.navn_fuld.split(" ")[1:-1])


@dataclasses.dataclass(frozen=True, slots=True)
class Matrikkel:
    id: str
    vej: str
    husnummer: int
    udlejning: bool
    tilflyttet: datetime | None
    betalt: bool
    primary: Person
    sekundary: Person | None


@overload
def parse_person(row: tuple[Cell, ...], opt: Literal[True] | bool) -> Person | None:
    ...


@overload
def parse_person(row: tuple[Cell, ...], opt: Literal[False] = ...) -> Person:
    ...


def parse_person(row: tuple[Cell, ...], opt: bool = False) -> Person | None:
    """Parse a row from the xlsx file and return a Person object"""
    if row[0].value is None:
        if opt:
            return None
        raise ValueError(f"Expected a person {row}")
    return Person(
        navn_fuld=parse_str(row[0]),
        navn_alt=parse_opt_str(row[1]),
        navn=parse_str(row[2]),
        mail=parse_opt_str(row[3]),
        addresse=parse_str(row[4]),
    )


def parse_matrikkel(row: tuple[Cell, ...]) -> Matrikkel:
    """Parse a row from the xlsx file and return a Matrikkel object"""
    return Matrikkel(
        id=parse_str(row[0]),
        vej=parse_str(row[1]),
        husnummer=parse_int(row[2]),
        udlejning=parse_bool(row[3]),
        tilflyttet=parse_opt_date(row[4]),
        betalt=parse_bool(row[5]),
        primary=parse_person(row[6:11]),
        sekundary=parse_person(row[11:16], opt=True),
    )


def load_xlsx(path: pathlib.Path) -> list[Matrikkel]:
    """Load xlsx file and return a list of dicts"""
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["2024"]
    result: list[Matrikkel] = []
    for row in islice(ws.rows, 1, None):  # Skip first row
        result.append(parse_matrikkel(row))

    return result


def vcard_adr(line: str):
    m = re.match(r"(.+) (\d\d\d\d) (.+)", line)
    if m:
        return f";;{m.group(1)};{m.group(3)};;{m.group(2)};;Denmark"
    raise ValueError(f"Could not parse address {line}")


def create_vcard(person: Person, groups: list[str]) -> str:
    """Create a vcard from a person"""
    return f"""BEGIN:VCARD
VERSION:3.0
N:{person.efternavn};{person.fornavn};{person.mellemnavne};;
FN:{person.navn_fuld}
EMAIL;TYPE=home:{person.mail}
ADR;TYPE=home:{vcard_adr(person.addresse)}
CATEGORIES:{",".join(groups)}
END:VCARD
"""


def create_vcards(matrikler: list[Matrikkel]) -> str:
    vcards: list[str] = []

    for mat in [m for m in matrikler if not m.udlejning]:
        vcards.append(
            create_vcard(
                mat.primary, ["Bakkeborg", mat.vej, f"{mat.vej} {mat.husnummer}"]
            )
        )
        if mat.sekundary:
            vcards.append(
                create_vcard(
                    mat.sekundary,
                    ["Bakkeborg", mat.vej, f"{mat.vej} {mat.husnummer}"],
                )
            )
    udlejere: set[Person] = set()
    for mat in [m for m in matrikler if m.udlejning]:
        udlejere.add(mat.primary)
        if mat.sekundary:
            udlejere.add(mat.sekundary)
    for udlejer in udlejere:
        vcards.append(create_vcard(udlejer, ["Bakkeborg"]))
    return "".join(vcards)


def convert(src: pathlib.Path, dst: pathlib.Path):
    matrikler = load_xlsx(src)
    vcards = create_vcards(matrikler)
    with open(dst, "w") as f:
        f.write(vcards)


if __name__ == "__main__":
    convert(pathlib.Path("data/Ejer Kartotek.xlsx"), pathlib.Path("data/vcards.vcf"))
