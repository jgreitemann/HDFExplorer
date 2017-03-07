import h5py
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf
from os import path

abshash = lambda x: abs(hash(x))

class h5TreeModel(GObject.Object, Gtk.TreeModel):
    def __init__(self, f):
        self.h5file = f
        self.pool = {}
        self.group_pixbuf = Gtk.IconTheme.get_default() \
                                         .choose_icon(["folder"], 16, 0) \
                                         .load_icon()
        icon_file = path.join(path.dirname(__file__), "data/icons/dataset.png")
        self.dataset_pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_file)
        icon_file = path.join(path.dirname(__file__), "data/icons/document.png")
        self.document_pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_file)
        GObject.GObject.__init__(self)

    def do_get_flags(self):
        return Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return 1

    def do_get_column_type(self, index):
        return str

    def do_get_iter(self, path):
        seq = []
        base = self.h5file
        if len(path.get_indices()) > 1:
            for i in path.get_indices()[1:]:
                if base is None or i >= len(base):
                    return (False, None)
                sorted_keys = sorted(list(base.keys()))
                seq.append(sorted_keys[i])
                base = base[sorted_keys[i]]
        seq = tuple(seq)
        self.pool[abshash(seq)] = seq
        iter = Gtk.TreeIter()
        iter.user_data = abshash(seq)
        iter.user_data2 = 42
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
        indices = [0]
        base = self.h5file
        for key in self.pool[iter.user_data]:
            if not key in base:
                return None
            sorted_keys = sorted(list(base.keys()))
            indices.append(sorted_keys.index(key))
            base = base[key]
        return Gtk.TreePath(tuple(indices))

    def get_h5_object(self, iter):
        base = self.h5file
        pathstr = "/"
        for key in self.pool[iter.user_data]:
            if not key in base:
                return None
            sorted_keys = sorted(list(base.keys()))
            base = base[key]
            pathstr += key
        return (pathstr, base)

    def do_get_value(self, iter, column):
        if self.pool[iter.user_data] == ():
            if column == 0:
                return path.basename(self.h5file.filename)
            elif column == 1:
                return self.document_pixbuf
        if column == 0:
            return self.pool[iter.user_data][-1]
        elif column == 1:
            base = self.h5file
            for key in self.pool[iter.user_data]:
                base = base[key]
            return self.group_pixbuf if isinstance(base, h5py.Group) \
                    else self.dataset_pixbuf

    def do_iter_next(self, iter):
        if iter.user_data is None:
            ud = ()
            self.pool[abshash(ud)] = ud
            iter.user_data = abshash(ud)
            return (True, iter)
        if self.pool[iter.user_data] == ():
            return (False, None)
        base = self.h5file
        for key in self.pool[iter.user_data][:-1]:
            if not key in base:
                return (False, None)
            base = base[key]
        sorted_keys = sorted(list(base.keys()))
        if not self.pool[iter.user_data][-1] in sorted_keys:
            return (False, None)
        i = sorted_keys.index(self.pool[iter.user_data][-1])
        if i + 1 >= len(sorted_keys):
            return (False, None)
        ud = self.pool[iter.user_data][:-1] + (sorted_keys[i + 1], )
        self.pool[abshash(ud)] = ud
        iter.user_data = abshash(ud)
        iter.user_data2 = 43
        return (True, iter)


    def do_iter_children(self, parent):
        return self.do_iter_nth_child(parent, 0)

    def do_iter_has_child(self, iter):
        base = self.h5file
        for key in self.pool[iter.user_data]:
            base = base[key]
        return isinstance(base, h5py.Group) and len(base) > 0

    # def do_iter_n_children(self, iter):
    #     print("iter_n_children")

    def do_iter_nth_child(self, parent, n):
        if parent is None:
            if n >= 1:
                return (False, None)
            else:
                iter = Gtk.TreeIter()
                iter.user_data = abshash(())
                iter.user_data2 = 82
                return (True, iter)
        base = self.h5file
        if self.pool[parent.user_data] != ():
            for key in self.pool[parent.user_data]:
                if not key in base:
                    return (False, None)
                base = base[key]
            ud = self.pool[parent.user_data]
        else:
            ud = ()
        if n >= len(base):
            return (False, None)
        sorted_keys = sorted(list(base.keys()))
        ud += (sorted_keys[n],)
        self.pool[abshash(ud)] = ud
        iter = Gtk.TreeIter()
        iter.user_data = abshash(ud)
        iter.user_data2 = 44
        return (True, iter)

    def do_iter_parent(self, child):
        ud = self.pool[child.user_data][:-1]
        self.pool[abshash(ud)] = ud
        iter = Gtk.TreeIter()
        iter.user_data = abshash(ud)
        iter.user_data2 = 45
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

