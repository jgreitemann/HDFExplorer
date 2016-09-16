import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from os import path

from .h5Document import h5Document

class h5Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="de.greitemann.h5explorer",
                         flags=Gio.ApplicationFlags.HANDLES_OPEN,
                         **kwargs)
        self.documents = []

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.on_open)
        self.add_action(action)

        menu_file = path.join(path.dirname(__file__), "data/ui/menu.ui")
        builder = Gtk.Builder.new_from_file(menu_file)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        if not self.documents:
            self.documents.append(h5Document(self))

    def do_open(self, files, n_files, hint):
        for file in files:
            self.open_filename(file.get_path())

    def on_open(self, action, param):
        chooser = Gtk.FileChooserDialog("Open HDF5 File",
                                        self.get_active_window(),
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL,
                                         Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN,
                                         Gtk.ResponseType.ACCEPT))
        filter_hdf = Gtk.FileFilter()
        filter_hdf.set_name("HDF5 files")
        filter_hdf.add_mime_type("application/x-hdf")
        chooser.add_filter(filter_hdf)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        chooser.add_filter(filter_any)

        res = chooser.run()
        if res == Gtk.ResponseType.ACCEPT:
            self.open_filename(chooser.get_filename())

        chooser.destroy()

    def open_filename(self, filename):
        if self.documents and self.documents[-1].model is None:
            self.documents[-1].load(filename)
        else:
            self.documents.append(h5Document(self, path=filename))

    def on_about(self, action, param):
        about_file = path.join(path.dirname(__file__), "data/glade/about.glade")
        builder = Gtk.Builder.new_from_file(about_file)
        about_dialog = builder.get_object("about-dialog")
        about_dialog.set_transient_for(self.get_active_window())
        about_dialog.add_credit_section("HDF5 backend", ["h5py"])
        about_dialog.add_credit_section("App icon based on", ["GNOME Terminal"])
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
