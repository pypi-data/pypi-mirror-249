#!/usr/bin/env python3

# This file is part of dbxfs.

# dbxfs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# dbxfs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with dbxfs.  If not, see <http://www.gnu.org/licenses/>.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import sys
import webbrowser

def can_interact():
    return True

def yes_no_input(message, default_yes = False):
    return messagebox.askyesno(message=message, title="dbxfs")

def warning(message):
    return messagebox.showwarning(message=message, title="dbxfs")

def error(message):
    return messagebox.showerror(message=message, title="dbxfs")

def check_exit_on_close(root):
    def dismiss(*args):
        sure = messagebox.askyesno(message="Are you sure you want to quit dbxfs?",
                                   title="dbxfs")
        if sure:
            sys.exit(1)

    root.protocol("WM_DELETE_WINDOW", dismiss)

DEFAULT_WRAP = 320

def getpass(label, title=None):
    root = Tk()
    if title is None:
        title = "dbxfs"
    check_exit_on_close(root)

    root.title(title)

    DEFAULT_PAD = 5

    mainframe = ttk.Frame(
        root,
        padding=(DEFAULT_PAD, DEFAULT_PAD, DEFAULT_PAD, DEFAULT_PAD),
    )
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    (ttk.Label(mainframe, text=label, wraplength=DEFAULT_WRAP,
               anchor="center", justify="center")
     .grid(column=0, row=0, pady=DEFAULT_PAD, sticky=(W,)))

    entry = ttk.Entry(mainframe, show='*')
    entry.grid(column=0, row=3, pady=DEFAULT_PAD)

    auth_code = [None]
    def submit(*args):
        auth_code[0] = entry.get()
        root.destroy()

    submit_button = ttk.Button(mainframe, text="Submit", command=submit)
    submit_button.grid(column=0, row=4, pady=DEFAULT_PAD)

    entry.bind("<Return>", submit)
    submit_button.bind("<Return>", submit)

    root.eval('tk::PlaceWindow . center')

    root.focus()
    entry.focus()

    root.mainloop()

    return auth_code[0]

def link_dbxfs(auth_url, title=None):
    root = Tk()
    if title is None:
        title = "dbxfs"

    root.title(title)

    check_exit_on_close(root)

    DEFAULT_PAD = 5

    mainframe = ttk.Frame(
        root,
        padding=(DEFAULT_PAD, DEFAULT_PAD, DEFAULT_PAD, DEFAULT_PAD),
    )
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    (ttk.Label(mainframe, text=(
        "We need to authorize dbxfs with Dropbox.\n"
        "To start the process, click the 'Begin' button below:"
    ), wraplength=DEFAULT_WRAP, anchor="center", justify="center")
     .grid(column=0, row=0, pady=DEFAULT_PAD))

    def open_browser(*args):
        webbrowser.open(auth_url, new=2)

    (ttk.Button(mainframe, text="Begin", command=open_browser)
     .grid(column=0, row=1, pady=DEFAULT_PAD))

    (ttk.Label(mainframe, text="Then enter the authorization code provided by Dropbox:",
               wraplength=DEFAULT_WRAP, anchor="center", justify="center")
     .grid(column=0, row=2, pady=DEFAULT_PAD))

    entry = ttk.Entry(mainframe)
    entry.grid(column=0, row=3, pady=DEFAULT_PAD)

    auth_code = [None]
    def submit(*args):
        auth_code[0] = entry.get()
        root.destroy()

    submit_button = ttk.Button(mainframe, text="Submit", command=submit)
    submit_button.grid(column=0, row=4, pady=DEFAULT_PAD)

    entry.bind("<Return>", submit)
    submit_button.bind("<Return>", submit)

    root.eval('tk::PlaceWindow . center')

    root.focus()
    entry.focus()

    root.mainloop()

    return auth_code[0]

def create_pass(header, title=None):
    root = Tk()
    if title is None:
        title = "dbxfs"

    check_exit_on_close(root)

    root.title(title)

    DEFAULT_PAD = 5

    mainframe = ttk.Frame(
        root,
        padding=(DEFAULT_PAD, DEFAULT_PAD, DEFAULT_PAD, DEFAULT_PAD),
    )
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    cr = 0
    if header is not None:
        (ttk.Label(mainframe, text=header, wraplength=DEFAULT_WRAP, anchor="center", justify="center")
         .grid(column=0, row=cr, pady=DEFAULT_PAD, columnspan=2, sticky=(W,)))
        cr += 1

    (ttk.Label(mainframe, text="Enter new passphase:")
     .grid(column=0, row=cr, pady=DEFAULT_PAD, sticky=(W,)))

    entrya = ttk.Entry(mainframe, show='*')
    entrya.grid(column=1, row=cr, pady=DEFAULT_PAD)

    cr += 1

    (ttk.Label(mainframe, text="Enter new passphase (again):")
     .grid(column=0, row=cr, pady=DEFAULT_PAD, sticky=(W,)))

    entryb = ttk.Entry(mainframe, show='*')
    entryb.grid(column=1, row=cr, pady=DEFAULT_PAD)

    cr += 1

    auth_code = [None]
    def submit(*args):
        if entrya.get() != entryb.get():
            messagebox.showerror(message="Passwords don't match!")
            return
        auth_code[0] = entrya.get()
        root.destroy()

    submit_button = ttk.Button(mainframe, text="Submit", command=submit)
    submit_button.grid(column=0, row=cr, columnspan=2, pady=DEFAULT_PAD)

    entrya.bind("<Return>", submit)
    entryb.bind("<Return>", submit)
    submit_button.bind("<Return>", submit)

    root.eval('tk::PlaceWindow . center')

    root.focus()
    entrya.focus()

    root.mainloop()

    return auth_code[0]

if __name__ == "__main__":
    print(create_pass("sup!"))
