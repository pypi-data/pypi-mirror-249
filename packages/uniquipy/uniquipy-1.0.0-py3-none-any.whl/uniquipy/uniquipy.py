"""
This module contains definitions implementing the uniquipy-logic.
"""

import hashlib

SUPPORTED_HASHING_METHODS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512
}
