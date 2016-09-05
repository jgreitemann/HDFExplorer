import h5py
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import hdfexplorer.h5TreeModel

class BrowserWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        f = h5py.File("/home/jgreitemann/bold_test.out.h5", "r")
        self.tree_store = hdfexplorer.h5TreeModel.h5TreeModel(f)

        self.tree_view = Gtk.TreeView(self.tree_store)
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

