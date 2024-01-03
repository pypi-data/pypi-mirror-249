#!/usr/bin/python3
# (c) Carsten Engelke 2023 GPL
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from pathlib import Path
import subprocess
from threading import Thread


def updatecmdlist():
    s = ""
    for f in Path(directory.get()).iterdir():
        if filetype.get() == "" or (f.name.endswith(filetype.get())):
            cmd = cmdstr.get()
            cmd = cmd.replace("#name", str(f.name))
            cmd = cmd.replace("#parent", str(f.parent))
            cmd = cmd.replace("#stem", str(f.stem))
            cmd = cmd.replace("#ext", str(f.suffix))
            cmd = cmd.replace("#fullpath", str(f))
            s += cmd + "\n"
    text1.delete(1.0, "end")
    text1.insert(1.0, s[:-1])


def loaddir():
    directory.set(filedialog.askdirectory())


def loadtoclip():
    text1.clipboard_clear()
    text1.clipboard_append(text1.get(1.0, "end"))


def executescript():
    cmds = text1.get(1.0, "end").split("\n")
    Thread(target=executecmds, args=(cmds,)).start()


def executecmds(cmds):
    result = []
    for cmd in cmds:
        text2.delete(1.0, "end")
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        for line in process.stdout:
            result.append(line)
        errcode = process.returncode
        for line in result:
            text2.insert("end", line)
        if errcode is not None:
            raise Exception("cmd %s failed, see above for details", cmd)


def replacewithfirstfile():
    firstfile = ""
    for f in Path(directory.get()).iterdir():
        if (
            filetype.get() == "" or (f.name.endswith(filetype.get()))
        ) and firstfile == "":
            firstfile = str(f.stem)
    cmd = cmdstr.get().replace(firstfile, "#stem")
    cmdstr.set(cmd)


class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        global directory
        global cmdstr
        global filetype
        global text1
        global text2
        directory = tk.StringVar()
        directory.set(str(Path.cwd()))
        cmdstr = tk.StringVar()
        cmdstr.set("echo #fullpath")
        filetype = tk.StringVar()
        filetype.set("")

        self.main = ttk.Frame(master, name="batch command for file")
        self.main.configure(height=200, width=476, padding=5)
        self.main.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")
        label1 = ttk.Label(self.main)
        label1.configure(text="Command:")
        label1.grid(column=0, row=1, sticky="ew")
        entry1 = ttk.Entry(self.main, textvariable=cmdstr, width=120)
        entry1.grid(column=1, columnspan=1, row=1, sticky="nsew")
        text1 = tk.Text(self.main)
        text1.configure(height=10, width=50)
        text1.grid(column=0, columnspan=3, row=3, sticky="ew")
        button1 = ttk.Button(self.main, command=loadtoclip)
        button1.configure(text="Copy to Clipboard")
        button1.grid(column=0, columnspan=3, row=4, sticky="ew")
        button2 = ttk.Button(self.main, command=loaddir)
        button2.configure(text="Load Directory")
        button2.grid(column=2, row=0, sticky="ew")
        entry2 = ttk.Entry(self.main, textvariable=directory)
        entry2.grid(column=1, row=0, sticky="ew")
        label2 = ttk.Label(self.main)
        label2.configure(text="Suffix-Filter:")
        label2.grid(column=0, row=2, sticky="ew")
        entry3 = ttk.Entry(self.main, textvariable=filetype)
        entry3.configure(validate="none")
        entry3.grid(column=1, row=2, sticky="ew")
        button3 = ttk.Button(self.main, command=updatecmdlist)
        button3.configure(
            text="Update Command List\n(Replace #fullpath\n"
            + "#parent\\#name\n"
            + "#parent\\#stem.#ext)"
        )
        button3.grid(column=2, row=1, rowspan=2, sticky="nsew")
        button4 = ttk.Button(self.main, command=executescript)
        button4.configure(text="Run Script")
        button4.grid(column=0, row=5, columnspan=2, sticky="ew")
        button5 = ttk.Button(self.main, command=replacewithfirstfile)
        button5.configure(text="Modify command")
        button5.grid(column=2, row=5, sticky="ew")
        text2 = tk.Text(self.main)
        text2.configure(height=5, width=50)
        text2.grid(column=0, columnspan=3, row=6, sticky="ew")

        self.main.columnconfigure(1, weight=1)
        self.main.columnconfigure(0, weight=0)
        self.main.rowconfigure(3, weight=1)

        # Main widget
        self.mainwindow = self.main

    def run(self):
        self.mainwindow.mainloop()


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m batchcmd` and `$ batchcmd `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    root = tk.Tk()
    root.title("Batch Command Creation Tool")
    app = NewprojectApp(root)
    app.run()


if __name__ == "__main__":
    main()
