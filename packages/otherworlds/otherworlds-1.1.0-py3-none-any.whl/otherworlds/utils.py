# SPDX-FileCopyrightText: 2023 Civic Hacker, LLC
#
# SPDX-License-Identifier: GPL-3.0-or-later

def slugify(original_string: str) -> str:
    s_encode = original_string.encode('ascii', 'ignore')
    s_decode = s_encode.decode()
    return s_decode.replace("'", '').replace(' ', '-').lower()
