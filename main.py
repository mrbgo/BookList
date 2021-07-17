#!/usr/bin/python
# -*- coding:utf-8 -*-

"""This is the main program for the Booklist open source tool.

author:     Mr.Brain
date:       2021.7.17
"""


import sys

if sys.version_info[0] >= 3:
    from tkinter import Label as _Label_o
    from tkinter import StringVar as _StringVar
    from tkinter import Tk as _Tk
    from tkinter.ttk import Button as _Button
    from tkinter.ttk import Combobox as _Combobox
    from tkinter.ttk import Entry as _Entry
    from tkinter.ttk import Frame as _Frame
    from tkinter.ttk import Label as _Label
    from tkinter.ttk import Labelframe as _Labelframe
    from tkinter.ttk import Scrollbar as _Scrollbar
    from tkinter.ttk import Treeview as _Treeview

elif sys.version_info[0] == 2:
    from Tkinter import Label as _Label_o
    from Tkinter import StringVar as _StringVar
    from Tkinter import Tk as _Tk
    from ttk import Button as _Button
    from ttk import Combobox as _Combobox
    from ttk import Entry as _Entry
    from ttk import Frame as _Frame
    from ttk import Label as _Label
    from ttk import Labelframe as _Labelframe
    from ttk import Scrollbar as _Scrollbar
    from ttk import Treeview as _Treeview

else:
    sys.stdout.write("Error: Unsupported Python version."
                     "\nFailed to execute module BookList")

from bld import dump as _dump
from bld import load as _load
from bld import read as _read
from bld import reset as _reset
from bld import write as _write
from dialog import alert as _alert
from dialog import question as _question


class Interface(object):
    """The main interface."""

    def __init__(self):
        """Interface initialization."""
        try:
            open(".bld").close()
        except FileNotFoundError:
            open(".bld", "x").close()

        self.root = _Tk()
        self.root.title("Book List")
        self.root.iconbitmap("./todo.ico")
        # self.root.attributes("-topmost", 1)       # You can try it!

        self.titles = ["Book Id", "Book Type",
                       "Book Name", "Start Reading Date",
                       "Stop Reading Date", "Book Infomation"]
        self.titlewidth = [100, 100, 250, 150, 150, 350]

        self.buttonname = ["submit", "exit", "reset all inputs",
                           "reset .bld data file"]
        self.button_cmd = [self.submit, self.root.quit,
                           self.reset, self.resetfile]

        tableframe = _Frame(self.root)

        self.table = _Treeview(
            tableframe,
            show="headings",
            selectmode="browse",
            columns=self.titles)

        tablexscroll = _Scrollbar(
            self.root,
            orient="horizontal",
            command=self.table.xview)

        tableyscroll = _Scrollbar(
            tableframe,
            command=self.table.yview)

        self.table["xscrollcommand"] = tablexscroll.set
        self.table["yscrollcommand"] = tableyscroll.set

        try:
            self.idx = len(self.load())
        except TypeError:
            self.idx = 0

        cnt = 0
        for title in self.titles:
            self.table.column(
                title,
                width=self.titlewidth[cnt],
                minwidth=self.titlewidth[cnt], anchor="center")
            self.table.heading(
                title,
                text=title)
            cnt += 1

        tableyscroll.pack(side="right", fill="y")
        self.table.pack(side="top", expand=True, fill="both")
        tableframe.pack(side="top", expand=True, fill="both")
        tablexscroll.pack(anchor="w", fill="x")

        self.conf = _Frame(self.root)

        self.new = _Labelframe(
            self.conf,
            text="Add Book Information")
        cnt = 0
        for title in self.titles[1:]:
            _Label(
                self.new,
                text=title+"：").grid(row=cnt, column=0, sticky="nsw")
            cnt += 1

        self.inputvars = []
        for title in self.titles[2:]:
            self.inputvars.append(_StringVar(name=title))
        self.modelist = _Combobox(
            self.new,
            state="readonly",
            values=["literature", "science", "foreign language", "others"])
        self.modelist.grid(row=0, column=1, sticky="nsew", padx=7)
        cnt = 0
        for var in self.inputvars:
            cnt += 1
            _Entry(
                self.new,
                textvariable=var,
                width=35).grid(row=cnt, column=1, sticky="ew", padx=7)

        self.fileconf = _Labelframe(self.conf, text="File Manipulate")

        cnt = 0
        for name in self.buttonname:
            _Button(
                self.fileconf,
                text=name,
                command=self.button_cmd[cnt],
                style="Lightyellow.TButton",
                width=22).grid(sticky="nsew", row=cnt//2, column=cnt % 2)
            cnt += 1
        self.new.grid(sticky="nsew", row=0, column=0)
        self.fileconf.grid(sticky="nsew", row=0, column=1)

        self.conf.pack()

        self.root.update()
        self.root.geometry("%dx%d+%d+%d" % (
            self.root.winfo_width(),
            self.root.winfo_height(),
            (self.root.winfo_screenwidth()
                - self.root.winfo_width())/2,
            (self.root.winfo_screenheight()
                - self.root.winfo_height())/2))

        self.root.mainloop()

    def resetfile(self):
        """Clear all reading information from the list and .bld file."""
        if _question(
                "Secondary Confirmation",
                "You have clicked the \"reset .bld data file\" button. "
                "The function of \"reset .bld data file\" is to clear "
                "all the reading information from your list and .bld "
                "data file. Do you want to confirm the operation?") == "yes":
            for item in self.table.get_children():
                self.table.delete(item)
            _reset()
            self.idx = 0

    def submit(self):
        """Submit reading information."""
        if self.modelist.get() == "":
            _f = True
            for var in self.inputvars:
                if var.get() != "":
                    _f = False
            if _f:
                _alert("Input Error", "Please enter at least one item.")
                return
        if "" in [self.modelist.get()]+[var.get() for var in self.inputvars]\
                and not _question(
                    "Secondary Confirmation",
                    "You have some unfilled item, which will be "
                    "displayed as a \"-\". confirm the operation?") == "yes":
            return
        insert_args = [self.modelist.get()]+[var.get()
                                             for var in self.inputvars]
        cnt = 0
        for arg in insert_args:
            if arg == "":
                insert_args[cnt] = "-"
            cnt += 1

        self.insert(*insert_args)

    def load(self):
        """Import reading information from the .bld file.

        Returns
        -------
        list
            A 2d array that is read and decrypted from a .bld file.
        """
        items = _load(_read() if _read() else "")
        if items != [['']]:
            for item in self.table.get_children():
                self.table.delete(item)
            for item in items:
                self.table.insert("", 'end', text="1", values=item)
                self.table.yview_scroll(1, "units")
            return items

    def reset(self):
        """Clear the reading information that is ready to insert."""
        if _question(
                "Secondary Confirmation",
                "You have clicked the reset all inputs button. "
                "The function of \"reset all inputs\" is to clear "
                "the reading information that you are preparing "
                "to enter into the list. Do you want to"
                " confirm the operation?"):
            self.modelist.set("")
            for var in self.inputvars:
                var.set("")

    def insert(self, mode, title, start, end, info):
        """Insert reading information.

        Parameters
        ----------
        mode : str
            Type of this book.
        title : str
            Title of this book.
        start : str
            Time the user starts reading this book.
        end : str
            Time the user stops reading this book.
        info : str
            Information of this book.

        Returns
        -------
        str
            Encrypted data.
        """
        self.idx += 1
        self.table.insert("", 'end', text="1", values=[
                          self.idx, mode, title, start, end, info])
        self.table.yview_scroll(1, "units")
        return _write(
            _dump([self.table.item(item, "values")
                   for item in self.table.get_children()]))


Interface()
