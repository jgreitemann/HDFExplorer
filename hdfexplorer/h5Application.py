import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from .tree_browser import BrowserWindow

class h5Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="de.greitemann.h5explorer",
                         flags=Gio.ApplicationFlags.HANDLES_OPEN,
                         **kwargs)
        self.windows = []

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        if not self.windows:
            self.windows.append(BrowserWindow(application=self))
        self.windows[-1].present()

    def do_open(self, files, n_files, hint):
        for file in files:
            if self.windows and self.windows[-1].model is None:
                self.windows[-1].load(file.get_path())
            else:
                self.windows.append(BrowserWindow(application=self,
                                                  path=file.get_path()))
            self.windows[-1].present()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
