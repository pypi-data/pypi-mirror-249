# SPDX-FileCopyrightText: 2023 Civic Hacker, LLC
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generator
import random

from otherworlds.klingon import FEMALE_KLINGON, MALE_KLINGON
from otherworlds.exoplanets import EXOPLANETS, STARNAMES

DEFAULT_SEED = 270055

PREFIX_TYPES = [
    "mathematical",
    "empty"
]


SUFFIX_TYPES = [
    'numerical',
    'mathematical',
    'empty'
]

NAME_SOURCES = [
    "starnames",
    "exoplanets"
]

MATHEMATICAL = [
    'Alpha',
    'Prime',
    'Beta',
    'Rho',
    'Delta',
    'Omega',
    'Epsilon',
    'Theta'
]

KLINGON = [nom for slist in zip(FEMALE_KLINGON, MALE_KLINGON) for nom in slist]


def generate_name(
      generator: random.Random = random.Random(DEFAULT_SEED),
      include_klingon: bool = False) -> Generator[str, None, None]:

    name_list = EXOPLANETS + STARNAMES
    if include_klingon:
        name_list += KLINGON

    while True:
        name = generator.choice(name_list)
        nsuffix = f'{generator.randrange(999, 9999)}'
        msuffix = generator.choice(MATHEMATICAL)
        yield f'{" ".join([name, msuffix, nsuffix]).strip()}'  # type: ignore
