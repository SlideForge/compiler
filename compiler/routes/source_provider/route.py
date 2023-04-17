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

from fastapi import APIRouter, status

from compiler.config import Config

from .models import Repo


router = APIRouter(prefix="/source")


@router.get("/repo", status_code=status.HTTP_200_OK)
async def source_repo() -> Repo:
    """
    Route providing a link to the source code
    """
    return Repo(repo=Config.REPO_LINK)
