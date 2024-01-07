<!--
SPDX-FileCopyrightText: 2023 Civic Hacker, LLC

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Otherworlds

![PyPI](https://img.shields.io/pypi/v/otherworlds?style=for-the-badge) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/otherworlds?style=for-the-badge)


A simple name generator for non-sensitive things. Mixes Klingon and real Exoplanets and star designations.

### generator use cases

- usernames
- names for teams/places/campaigns in your favorite MMORPG
- subdomains
- emphemeral service names


## Installation

Install this package using the usual suspects (e.g., Pypi)

```
pip install otherworlds
```

## How to use the generator


This command generates names using real stars and exoplanets:

```
pipx otherworlds
```

To mix in some Klingon, use the '--klingon' flag:


```
pipx otherworlds --klingon
```

You can supply your own seed using the `--seed` argument:

```
pipx otherworlds --klingon --seed 42
```


By default, `otherworlds` returns a single name. You can specify hoe=w many names it shoud return:

```
pipx otherworlds --klingon --num 5
```

You can view the full help with this command:

```
pipx otherworlds --help
```

## License

This codebase is licensed under the GPLv3+ and therefore the use, inclusion, modification, and distribution of this software is governed by the GPL.

If you are planning to use otherworlds in a commercial product and wish to opt-out of the obligations of the GPL, please reach out to license@civichacker.com.
