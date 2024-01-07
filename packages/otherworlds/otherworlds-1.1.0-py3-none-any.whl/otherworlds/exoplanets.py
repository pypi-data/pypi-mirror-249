# SPDX-FileCopyrightText: 2023 Civic Hacker, LLC
#
# SPDX-License-Identifier: GPL-3.0-or-later

import csv

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
    "male_klingon",
    "exoplanets",
    "female_klingon"
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

EXOPLANETS = list()
STARNAMES = list()

with open('./data/NameExoWorlds.csv', 'r') as f:
    reader = csv.DictReader(f)
    for line in reader:
        EXOPLANETS.append(line.get("Name Exoplanet"))
        STARNAMES.append(line.get("Name Star"))
