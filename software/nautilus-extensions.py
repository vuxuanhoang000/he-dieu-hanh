import os
from subprocess import call

from gi.repository import Gdk, GObject, Gtk, Nautilus


class CopyPath(GObject.GObject, Nautilus.MenuProvider):
    def copy_path(self, menu, files):
        text = ""

        for file in files:
            text += file.get_location().get_path() + "\n"

        text = text[:-1]

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)

    def get_file_items(self, *args):
        files = args[-1]
        item = Nautilus.MenuItem(
            name="CopyItemsPath",
            label="Copy Path",
        )

        item.connect("activate", self.copy_path, files)

        return [item]

    def get_background_items(self, *args):
        file_ = args[-1]
        item = Nautilus.MenuItem(
            name="CopyBackgroundPath",
            label="Copy Path",
        )

        item.connect("activate", self.copy_path, [file_])

        return [item]


class LaunchVsCode(GObject.GObject, Nautilus.MenuProvider):
    # path to vscode
    VSCODE = "code"

    # what name do you want to see in the context menu?
    VSCODENAME = "Code"

    # always create new window?
    NEWWINDOW = False

    def launch_vscode(self, menu, files):
        safepaths = ""
        args = ""

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '

            # If one of the files we are trying to open is a folder
            # create a new instance of vscode
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = "--new-window "

        if self.NEWWINDOW:
            args = "--new-window "

        call(self.VSCODE + " " + args + safepaths + "&", shell=True)

    def get_file_items(self, *args):
        files = args[-1]
        item = Nautilus.MenuItem(
            name="VSCodeOpen",
            label="Open with " + self.VSCODENAME,
            tip="Opens the selected files with VSCode",
        )
        item.connect("activate", self.launch_vscode, files)

        return [item]

    def get_background_items(self, *args):
        file_ = args[-1]
        item = Nautilus.MenuItem(
            name="VSCodeOpenBackground",
            label="Open with " + self.VSCODENAME,
            tip="Opens the current directory in VSCode",
        )
        item.connect("activate", self.launch_vscode, [file_])

        return [item]