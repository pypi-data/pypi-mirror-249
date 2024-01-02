# SPDX-License-Identifier: MIT


# Import local modules.
from avro import config


# Functions.
def is_vowel(text: str) -> bool:
    """
    Check if given string is a vowel.
    """

    return text.lower() in config.AVRO_VOWELS


def is_consonant(text: str) -> bool:
    """
    Check if given string is a consonant.
    """

    return text.lower() in config.AVRO_CONSONANTS


def is_number(text: str) -> bool:
    """
    Check if given string is a number.
    """

    return text.lower() in config.AVRO_NUMBERS


def is_punctuation(text: str) -> bool:
    """
    Check if given string is a punctuation.
    """

    return not (text.lower() in config.AVRO_VOWELS or text.lower() in config.AVRO_CONSONANTS)


def is_case_sensitive(text: str) -> bool:
    """
    Check if given string is case sensitive.
    """

    return text.lower() in config.AVRO_CASESENSITIVES


def is_exact(needle: str, haystack: str, start: int, end: int, matchnot: bool) -> bool:
    """
    Check exact occurrence of needle in haystack.
    """

    return (start >= 0 and end < len(haystack) and haystack[start:end] == needle) != matchnot


def fix_string_case(text: str) -> str:
    """
    Converts case-insensitive characters to lower case.

    Case-sensitive characters as defined in config.AVRO_CASESENSITIVES
    retain their case, but others are converted to their lowercase
    equivalents. The result is a string with phonetic-compatible case
    which will the parser will understand without confusion.
    """

    fixed = []

    for i in text:
        if is_case_sensitive(i):
            fixed.append(i)
        else:
            fixed.append(i.lower())

    return ''.join(fixed)
