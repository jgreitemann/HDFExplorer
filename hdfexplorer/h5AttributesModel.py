import h5py
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk

class h5AttributesModel(GObject.Object, Gtk.TreeModel):
    def __init__(self, attrs):
        self._h5attr = attrs
        self._keys = sorted(attrs.keys())
        GObject.GObject.__init__(self)

    def do_get_flags(self):
        return Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return 2

    def do_get_column_type(self, index):
        return str

    def do_get_iter(self, path):
        if path[0] >= len(self._keys):
            return (False, None)
        iter = Gtk.TreeIter()
        iter.user_data = path[0]
        return (True, iter)

    def do_get_path(self, iter):
        return Gtk.TreePath((iter.user_data,))

    def do_get_value(self, iter, column):
        if column == 0:
            return self._keys[iter.user_data]
        else:
            return str(self._h5attr[self._keys[iter.user_data]])

    def do_iter_next(self, iter):
        if iter is None:
            if len(self._keys) == 0:
                return (False, None)
            else:
                iter = Gtk.TreeIter()
                iter.user_data = 0
                return (True, iter)
        if iter.user_data + 1 < len(self._keys):
            iter.user_data += 1
            return (True, iter)
        return (False, None)

    def do_iter_has_child(self, iter):
        return False

    def do_iter_nth_child(self, parent, n):
        if n >= len(self._keys):
            return (False, None)
        iter = Gtk.TreeIter()
        iter.user_data = n
        return (True, iter)
