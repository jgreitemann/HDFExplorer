import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import hdfexplorer.h5TreeModel

class BrowserWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        data = {'correct': None,
                'horse': {'Shetland pony': None,
                          'Spanish Mustang': None,
                          'Brandenburger': None,
                          'Freiberger': None},
                'battery': {'AA': None,
                            'AAA': None,
                            'AAAA': None},
                'staple': None}
        self.tree_store = hdfexplorer.h5TreeModel.h5TreeModel(data)

        self.tree_view = Gtk.TreeView(self.tree_store)
        name_col = Gtk.TreeViewColumn("Dataset",
                                      Gtk.CellRendererText(),
                                      text=0)
        self.tree_view.append_column(name_col)
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.tree_view)
        self.add(self.scroll)

