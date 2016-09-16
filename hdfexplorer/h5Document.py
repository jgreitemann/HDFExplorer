import h5py
from os.path import join, dirname, basename
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Pango

from .h5TreeModel import h5TreeModel
from .h5DatasetModel import h5DatasetModel

class h5Document(GObject.Object):

    def __init__(self, application, *args, path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = application

        self._h5f = None
        self.model = None
        self.entities = {}

        document_file = join(dirname(__file__), "data/glade/document.glade")
        builder = Gtk.Builder.new_from_file(document_file)
        self.window = builder.get_object("app-window")
        self.app.add_window(self.window)
        self.tree_view = builder.get_object("content-view")
        self.stack = builder.get_object("stack")
        self.dset_tree = builder.get_object("dataset-tree")

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

        handlers = {"on_close": self.on_close,
                    "on_selection_changed": self.on_selection_changed}
        builder.connect_signals(handlers)

        self.window.present()

    def load(self, path):
        if self._h5f:
            self.tree_view.set_model(None)
            self.model = None
            self._h5f.close()
        try:
            self._h5f = h5py.File(path, "r")
        except OSError as e:
            message = Gtk.MessageDialog(self.window,
                                        Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                        Gtk.MessageType.ERROR,
                                        Gtk.ButtonsType.CANCEL,
                                        "Error opening file \"{}\""
                                        .format(basename(path)))
            message.format_secondary_text("{}".format(e))
            message.run()
            message.destroy()
            return
        self.window.set_title(basename(path))
        self.model = h5TreeModel(self._h5f)
        self.tree_view.set_model(self.model)

    def on_selection_changed(self, tree_selection):
        model, iter = tree_selection.get_selected()
        if model is None or iter is None:
            self.stack.set_visible_child_name("placeholder")
            return
        h5_path, h5_object = model.get_h5_object(iter)
        if not isinstance(h5_object, h5py.Dataset):
            self.stack.set_visible_child_name("placeholder")
            return
        # dataset has been selected

        # retrieve existing model or create a new one
        if not h5_path in self.entities:
            self.entities[h5_path] = h5DatasetModel(h5_object)

        # clear tree view columns & create new ones
        for c in self.dset_tree.get_columns():
            self.dset_tree.remove_column(c)
        col = Gtk.TreeViewColumn("")
        cell = Gtk.CellRendererText()
        cell.set_property("foreground", "#979a9b")
        cell.set_property("xalign", 0.5)
        cell.set_property("font", "Cantarell Bold 11")
        col.pack_start(cell, False)
        col.add_attribute(cell, "text", 0)
        self.dset_tree.append_column(col)
        for i in range(self.entities[h5_path].do_get_n_columns() - 1):
            col = Gtk.TreeViewColumn(str(i))
            cell = Gtk.CellRendererText()
            cell.set_property("xalign", 1.0)
            col.pack_start(cell, False)
            col.add_attribute(cell, "text", i+1)
            self.dset_tree.append_column(col)

        # put changes in effect
        self.dset_tree.set_model(self.entities[h5_path])
        self.stack.set_visible_child_name("dataset-scroll")

    def on_close(self, window, event):
        self.app.remove_window(window)
        if self._h5f:
            self.tree_view.set_model(None)
            self.dset_tree.set_model(None)
            self.model = None
            self._h5f.close()
        self.app.documents.remove(self)
