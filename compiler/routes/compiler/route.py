"""
Copyright (c) 2023 SlideForge.

This file is part of SlideForge compiler.

SlideForge compiler is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SlideForge compiler.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess
from os import getenv, mkdir, remove
from os.path import exists, isdir, isfile
from pathlib import Path
from typing import Iterator
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import StreamingResponse

from .models import LatexCode


DIR = getenv("COMPILE_DIR", "compile")


router = APIRouter(prefix="/compiler")


def check_compile_dir() -> None:
    """
    Function that checks whether the compiler directory exists and creates it if necessary
    """
    if (not exists(DIR)) or (not isdir(DIR)):
        mkdir(DIR)


def cleanup_file(file_path: Path) -> None:
    """
    Remove the compiled pdf file when it is no longer needed
    :param file_path: the path to the file
    """
    remove(file_path)


def compile_tex(tex_code: str) -> Path:
    """
    Function that compiles LaTeX code into a pdf file
    :param tex_code: the LaTeX code to be compiled
    :return: the compiled LaTeX code as a pdf
    """
    file_uuid = str(uuid4().int)

    file_path = f"{DIR}/{file_uuid}"

    check_compile_dir()

    try:
        with open(f"{file_path}.tex", "w") as texfile:
            texfile.write(tex_code)

    except (OSError, IOError):
        raise IOError("Not able to write tex to file")

    command = ["latexmk", "--pdf", "--interaction=nonstopmode", f"-output-directory={DIR}", f"{file_path}.tex"]

    try:
        subprocess.run(command, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise OSError("Compiling LaTeX failed")

    try:
        subprocess.run(["latexmk", "-cd", "-c", file_path], stdout=subprocess.DEVNULL)
    except (OSError, IOError, subprocess.CalledProcessError):
        extensions = ["aux", "log", "out", "fls", "fdb_latexmk"]

        for ext in extensions:
            try:
                remove(f"{file_path}.{ext}")
            except FileNotFoundError:
                pass

    remove(f"{file_path}.tex")

    return Path(f"{file_path}.pdf")


def read_pdf(pdf_path: Path) -> Iterator[bytes]:
    with open(pdf_path, "rb") as pdf_file:
        yield from pdf_file


@router.post(path="/compile", status_code=status.HTTP_200_OK, response_class=StreamingResponse)
async def compiler_compile(code: LatexCode, tasks: BackgroundTasks) -> StreamingResponse:
    """
    Route that compiles LaTeX code into a pdf and returns the resulting file
    :param code: the LaTeX code
    :param tasks: fastapi background tasks
    :return: the compiled pdf file as a stream
    """

    pdf_path = compile_tex(code.code)

    if not (exists(pdf_path) and isfile(pdf_path)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The compiler was unable to compile the provided LaTeX code",
        )

    # add a background task so that FastAPI cn clean up the pdf file after it has been returned
    tasks.add_task(cleanup_file, file_path=Path(pdf_path))

    return StreamingResponse(content=read_pdf(pdf_path), media_type="application/pdf")
