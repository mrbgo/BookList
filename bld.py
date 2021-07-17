#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Manipulate .bld files.

author:     Mr.Brain
date:       2021.7.17
"""


def reverse(s, m):
    """Encrypt or decrypt a string.

    Parameters
    ----------
    s : str
        The string to be manipulated.
    m : bool
        The mode of the conversion. Encrypt if True and vice versa.

    Returns
    -------
    str
        A string that has been converted.
    """
    if not s:
        return ""
    enc = ""
    for ch in s:
        rev_ch = "0b"
        if m:
            bin_ch = bin(ord(ch))[2:]
            rev_ch += "10"
        else:
            bin_ch = bin(ord(ch))[4:]
        for _ch in bin_ch:
            rev_ch += "1" if _ch == "0" else "0"
        enc += chr(int(rev_ch, 0))
    return enc


def load(s):
    """Parse the original 2-D array from the encrypted string.

    Parameters
    ----------
    s : str
        The string to be parsed.

    Returns
    -------
    list
        Parsed array.
    """
    return [[reverse(__l, False) for __l in _l.split(";")]
            for _l in s.split(":")]


def dump(li):
    """Reverse each character in a 2d array bit by bit.

    Parameters
    ----------
    li : list | tuple
        A 2d array for encryption.

    Returns
    -------
    str
        Encrypted data.
    """
    nl = []
    cnt = 0
    for i in li:
        nl.append([])
        for j in i:
            nl[cnt].append(reverse(j, True))
        cnt += 1
    return ":".join([";".join(_l) for _l in nl])


def write(s):
    """Write the string to the file.

    Parameters
    ----------
    s : str
        The string.

    Returns
    -------
    str | None
        The given string.
    """
    s = bytes(s.encode("utf-8"))
    bl_fio = open(".bld", "wb")
    bl_fio.write(s)
    bl_fio.close()
    return s


def read():
    """Read the string from the .bld file.

    Returns
    -------
    str | None
        Return the string in the file if it exists.
        Return None if the file does not exist.
    """
    bl_fio = open(".bld", "rb")
    s = bl_fio.read().decode("utf-8")
    bl_fio.close()
    return s


def reset():
    """Reset the .bld file."""
    bl_fio = open(".bld", "wb")
    bl_fio.truncate()
    bl_fio.close()
