import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from os import path

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

        menu_file = path.join(path.dirname(__file__), "data/ui/menu.ui")
        builder = Gtk.Builder.new_from_file(menu_file)
        self.set_app_menu(builder.get_object("app-menu"))

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
        about_dialog = Gtk.AboutDialog(transient_for=self.windows[-1],
                                       modal=True)
        about_dialog.set_comments("The much-needed alternative to HDFView")
        about_dialog.set_authors(["Jonas Greitemann"])
        about_dialog.set_copyright("Copyright © 2016 Jonas Greitemann")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_logo_icon_name("jgreitemann-h5explorer")
        about_dialog.set_program_name("HDF Explorer")
        about_dialog.set_version("0.1")
        website = "https://www.github.com/jgreitemann/HDFExplorer"
        about_dialog.set_website(website)
        about_dialog.set_website_label("Website")
        about_dialog.add_credit_section("HDF5 backend", ["h5py"])
        about_dialog.add_credit_section("App icon based on", ["GNOME Terminal"])
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
