#!/usr/bin/python
# -*- coding:utf-8 -*-

"""Open a new Question dialog window or Alert dialog window.

author:     Mr.Brain
date:       2021.7.17
"""

from tkinter import Tk as _Tk

opened = False


def alert(title, message):
    """Open a new Alert dialog window.

    Parameters
    ----------
    title : str
        The title of the dialog window.
    message : str
        The text message of the dialog window.

    Returns
    -------
    str
        The return value of the dialog window.
    """
    global opened
    if not opened:
        opened = True
        w = _Tk()
        w.withdraw()
        res = w.tk.call(
            "tk_messageBox",
            *w._options({"icon": "info", "type": "ok",
                        "title": title, "message": message}))
        w.destroy()
        opened = False
        return res


def question(title, message):
    """Open a new Question dialog window.

    Parameters
    ----------
    title : str
        The title of the dialog window.
    message : str
        The text message of the dialog window.

    Returns
    -------
    str
        The return value of the dialog window.
    """
    global opened
    if not opened:
        opened = True
        w = _Tk()
        w.withdraw()
        res = w.tk.call(
            "tk_messageBox",
            *w._options({"icon": "info", "type": "yesno",
                        "title": title, "message": message}))
        w.destroy()
        opened = False
        return res
