# SPDX-FileCopyrightText: 2023-present Flavio Amurrio <25621374+FlavioAmurrioCS@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from fzf import fzf


if __name__ == "__main__":
    s1: list[int] = fzf([1], multi=True)
    s2: int | None = fzf([2], multi=False)
    s3: int | None = fzf(range(100))
