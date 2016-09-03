import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk

words = ['correct', 'horse', 'battery', 'staple']

class h5TreeModel(GObject.Object, Gtk.TreeModel):
    def do_get_flags(self):
        return Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return 1

    def do_get_column_type(self, index):
        return str

    def do_get_iter(self, path):
        i = path.get_indices()[0]
        if i < len(words):
            iter_ = Gtk.TreeIter()
            iter_.user_data = i
            return (True, iter_)
        else:
            return (False, None)

    # def do_get_iter_from_string(self, path_string):
    #     print("get_iter_from_string")

    # def do_get_string_from_iter(self, iter):
    #     print("get_string_from_iter")

    # def do_get_iter_root(self):
    #     print("get_iter_root")

    # def do_get_iter_first(self):
    #     print("get_iter_first")

    def do_get_path(self, iter):
        if iter.user_data is not None:
            return Gtk.TreePath((iter.user_data,))
        else:
            return None

    def do_get_value(self, iter, column):
        return words[iter.user_data]

    def do_iter_next(self, iter):
        if iter.user_data is None:
            iter.user_data = 0
            return (True, iter)
        elif iter.user_data < len(words) - 1:
            iter.user_data += 1
            return (True, iter)
        else:
            return (False, None)


    # def do_iter_children(self, parent):
    #     print("iter_children")

    def do_iter_has_child(self, iter):
        return False

    # def do_iter_n_children(self, iter):
    #     print("iter_n_children")

    def do_iter_nth_child(self, parent, n):
        iter_ = Gtk.TreeIter()
        iter_.user_data = n
        return (True, iter_)

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

