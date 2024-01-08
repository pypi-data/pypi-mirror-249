import pathlib

import typer

from bakkeborg_xlsx_vcf import convert


def cli(
    src: pathlib.Path,
    dst: pathlib.Path = typer.Argument(pathlib.Path("vcards.vcf")),
):
    """Convert an excel file to a vcf file"""
    convert(src, dst)


def main():
    typer.run(cli)
