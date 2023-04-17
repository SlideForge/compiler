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

from pathlib import Path

from fastapi import FastAPI, status
from pydantic import BaseModel

from compiler.config import load_config
from compiler.logger import get_logger
from compiler.routes.compiler import route as compiler
from compiler.routes.source_provider import route as source_provider


load_config(Path("config.yml"))
logger = get_logger(__name__)

app = FastAPI()

app.include_router(source_provider.router)
app.include_router(compiler.router)

logger.info("Application startup successful")


class StatusResponse(BaseModel):
    status: str


@app.get("/", status_code=status.HTTP_200_OK)
async def root() -> StatusResponse:
    return StatusResponse(status="Connection successful")
