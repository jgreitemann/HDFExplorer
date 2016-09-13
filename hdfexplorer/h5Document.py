import h5py
from os.path import join, dirname, basename
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk

import hdfexplorer.h5TreeModel

class h5Document(GObject.Object):

    def __init__(self, application, *args, path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = application

        self._h5f = None
        self.model = None

        document_file = join(dirname(__file__), "data/glade/document.glade")
        builder = Gtk.Builder.new_from_file(document_file)
        self.window = builder.get_object("app-window")
        self.app.add_window(self.window)
        self.tree_view = builder.get_object("content-view")

        dset_col = Gtk.TreeViewColumn("Datasets")
        icon_cell = Gtk.CellRendererPixbuf()
        name_cell = Gtk.CellRendererText()
        dset_col.pack_start(icon_cell, False)
        dset_col.add_attribute(icon_cell, "pixbuf", 1)
        dset_col.pack_start(name_cell, False)
        dset_col.add_attribute(name_cell, "text", 0)
        self.tree_view.append_column(dset_col)

        if path is not None:
            self.load(path)

        handlers = {"on_close": self.on_close}
        builder.connect_signals(handlers)

        self.window.present()

    def load(self, path):
        if self._h5f:
            self.tree_view.set_model(None)
            self.model = None
            self._h5f.close()
        self._h5f = h5py.File(path, "r")
        self.window.set_title(basename(path))
        self.model = hdfexplorer.h5TreeModel.h5TreeModel(self._h5f)
        self.tree_view.set_model(self.model)

    def on_close(self, window, event):
        self.app.remove_window(window)
        if self._h5f:
            self.tree_view.set_model(None)
            self.model = None
            self._h5f.close()
        self.app.documents.remove(self)
