import h5py
from os.path import basename
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import hdfexplorer.h5TreeModel

class BrowserWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, path=None, **kwargs):
        super().__init__(title="(Empty)", *args, **kwargs)

        self._h5f = None
        self.model = None
        self.tree_view = Gtk.TreeView()
        if path is not None:
            self.load(path)

        dset_col = Gtk.TreeViewColumn("Datasets")
        icon_cell = Gtk.CellRendererPixbuf()
        name_cell = Gtk.CellRendererText()
        dset_col.pack_start(icon_cell, False)
        dset_col.add_attribute(icon_cell, 'icon_name', 1)
        dset_col.pack_start(name_cell, False)
        dset_col.add_attribute(name_cell, 'text', 0)
        self.tree_view.append_column(dset_col)
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.tree_view)
        self.add(self.scroll)
        self.scroll.show_all()

        self.connect("delete-event", self.on_close)

    def load(self, path):
        if self._h5f:
            self.tree_view.set_model(None)
            self.model = None
            self._h5f.close()
        self._h5f = h5py.File(path, "r")
        self.set_title(basename(path))
        self.model = hdfexplorer.h5TreeModel.h5TreeModel(self._h5f)
        self.tree_view.set_model(self.model)

    def on_close(self, window, event):
        if self._h5f:
            self.tree_view.set_model(None)
            self.model = None
            self._h5f.close()
