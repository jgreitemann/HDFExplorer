import h5py
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk

class h5DatasetModel(GObject.Object, Gtk.TreeModel):
    def __init__(self, d):
        self._h5dset = d
        self._h5view = self._h5dset
        GObject.GObject.__init__(self)

    def do_get_flags(self):
        return Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        if len(self._h5view.shape) <= 1:
            return 2
        return self._h5view.shape[1] + 1

    def do_get_column_type(self, index):
        return str

    def do_get_iter(self, path):
        if len(self._h5view.shape) == 0 and path[0] > 0:
            return (False, None)
        if len(self._h5view.shape) > 0 and path[0] >= self._h5view.shape[0]:
            return (False, None)
        iter = Gtk.TreeIter()
        iter.user_data = path[0]
        return (True, iter)

    # def do_get_iter_from_string(self, path_string):
    #     print("get_iter_from_string")

    # def do_get_string_from_iter(self, iter):
    #     print("get_string_from_iter")

    # def do_get_iter_root(self):
    #     print("get_iter_root")

    # def do_get_iter_first(self):
    #     print("get_iter_first")

    def do_get_path(self, iter):
        return Gtk.TreePath((iter.user_data,))

    def do_get_value(self, iter, column):
        if column == 0:
            return str(iter.user_data)
        if len(self._h5view.shape) == 0:
            return str(self._h5view[...])
        if len(self._h5view.shape) == 1:
            return str(self._h5view[iter.user_data])
        return str(self._h5view[iter.user_data, column - 1])

    def do_iter_next(self, iter):
        if len(self._h5view.shape) > 0:
            if iter.user_data + 1 < self._h5view.shape[0]:
                iter.user_data += 1
                return (True, iter)
        return (False, None)

    def do_iter_has_child(self, iter):
        return False

    def do_iter_nth_child(self, parent, n):
        if len(self._h5view.shape) == 0:
            if n != 0:
                return (False, None)
        else:
            if n >= self._h5view.shape[0]:
                return (False, None)
        iter = Gtk.TreeIter()
        iter.user_data = n
        return (True, iter)

    # def do_ref_node(self, iter):
    #     print("ref_node")

    # def do_unref_node(self, iter):
    #     print("unref_node")

    # def do_get(self, iter, column):
    #     print("get")

    # def do_foreach(self, func, user_data):
    #     print("foreach")

    # def do_row_changed(self, path, iter):
    #     print("row_changed")

    # def do_row_inserted(self, path, iter):
    #     print("row_inserted")

    # def do_row_has_child_toggled(self, path, iter):
    #     print("row_has_child_toggled")

    # def do_row_deleted(self, path):
    #     print("row_deleted")

    # def do_rows_reordered(self, path, iter, new_order):
    #     print("rows_reordered")

    # def do_filter_new(self, root=None):
    #     print("filter_new")

