from copy import copy
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk


class h5TreeModel(GObject.Object, Gtk.TreeModel):
    def __init__(self, d):
        self.data = d
        self.pool = {}
        GObject.GObject.__init__(self)

    def do_get_flags(self):
        return Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return 1

    def do_get_column_type(self, index):
        return str

    def do_get_iter(self, path):
        seq = []
        base = self.data
        for i in path.get_indices():
            if base is None or i >= len(base):
                return (False, None)
            sorted_keys = sorted(list(base.keys()))
            seq.append(sorted_keys[i])
            base = base[sorted_keys[i]]
        self.pool[id(seq)] = seq
        iter = Gtk.TreeIter()
        iter.user_data = id(seq)
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
        indices = []
        base = self.data
        for key in self.pool[iter.user_data]:
            if not key in base:
                return None
            sorted_keys = sorted(list(base.keys()))
            indices.append(sorted_keys.index(key))
            base = base[key]
        return Gtk.TreePath(tuple(indices))

    def do_get_value(self, iter, column):
        return self.pool[iter.user_data][-1]

    def do_iter_next(self, iter):
        if iter.user_data is None:
            sorted_keys = sorted(list(self.data.keys()))
            if not sorted_keys:
                return (False, None)
            iter.user_data = (sorted_keys[0],)
            self.pool[id(iter.user_data)] = iter.user_data
            return (True, iter)
        base = self.data
        for key in self.pool[iter.user_data][:-1]:
            if not key in base:
                return (False, None)
            base = base[key]
        sorted_keys = sorted(list(base.keys()))
        if not self.pool[iter.user_data][-1] in sorted_keys:
            return (False, None)
        i = sorted_keys.index(self.pool[iter.user_data][-1])
        ud = copy(self.pool[iter.user_data])
        if i + 1 >= len(sorted_keys):
            return (False, None)
        ud[-1] = sorted_keys[i + 1]
        iter.user_data = id(ud)
        self.pool[id(ud)] = ud
        return (True, iter)


    # def do_iter_children(self, parent):
    #     print("iter_children")

    def do_iter_has_child(self, iter):
        return False

    # def do_iter_n_children(self, iter):
    #     print("iter_n_children")

    def do_iter_nth_child(self, parent, n):
        base = self.data
        if parent is not None:
            for key in self.pool[parent.user_data]:
                if not key in base:
                    return (False, None)
                base = base[key]
            ud = copy(self.pool[parent.user_data])
        else:
            ud = []
        if n >= len(base):
            return (False, None)
        sorted_keys = sorted(list(base.keys()))
        ud.append(sorted_keys[n])
        self.pool[id(ud)] = ud
        iter = Gtk.TreeIter()
        iter.user_data = id(ud)
        return (True, iter)

    # def do_iter_parent(self, child):
    #     print("iter_parent")

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

