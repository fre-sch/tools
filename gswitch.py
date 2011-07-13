"""
stand-alone application switcher
"""
import sys
import glib
import gtk
gdk = gtk.gdk
keysyms = gtk.keysyms
import wnck

sys.stderr = open('/tmp/gswitch.log', 'a')

class GSwitchIcon(gtk.EventBox):
  def __init__(self, window):
    super(GSwitchIcon, self).__init__()
    self.app_window = window
    img = gtk.image_new_from_pixbuf(window.get_icon())
    label = gtk.Label("<b>%s</b>"%window.get_application().get_name())
    label.set_use_markup(True)
    box = gtk.VBox(False, 0)
    box.set_border_width(8)
    box.pack_start(img, True, False, 0)
    box.pack_start(label, True, False, 0)
    self.set_property("above-child", False)
    self.set_property("visible-window", True)
    self.add(box)

  def unselect(self, timestamp):
    style = self.get_parent().get_style()
    bg_normal = style.bg[gtk.STATE_NORMAL]
    self.modify_bg(gtk.STATE_NORMAL,bg_normal)

  def select(self, timestamp):
    style = self.get_parent().get_style()
    bg_selected = style.bg[gtk.STATE_SELECTED]
    self.modify_bg(gtk.STATE_NORMAL,bg_selected)
    self.app_window_focus(timestamp)

  def app_window_focus(self, timestamp):
    if timestamp is None:
      timestamp = long(glib.get_current_time())
    #sel_child.app_window.activate(timestamp)
    xid = self.app_window.get_xid()
    gdk_win = gdk.window_foreign_new(xid)
    gdk_win.focus(timestamp)


class GSwitch(gtk.Window):
  def __init__(self):
    super(GSwitch, self).__init__(gtk.WINDOW_POPUP)
    self.set_position(gtk.WIN_POS_CENTER)
    self.set_default_size(64, 64)
    self.set_events(gdk.KEY_PRESS_MASK)
    self.connect("delete-event", gtk.main_quit)
    self.connect("key-press-event", self.on_key_press)
    self.connect("key-release-event", self.on_key_release)
    self.sel_child_idx = 1
    self.populate()
  
  # Show the window and plug required stuff
  def show_all(self):
    super(GSwitch, self).show_all()
    # Grab keyboard
    while gdk.keyboard_grab(self.window) != gtk.gdk.GRAB_SUCCESS:
      sleep (0.1)
  
  def populate(self):
    box = gtk.HBox(True, 0)
    self.add( box )

    self.screen = wnck.screen_get_default()
    self.screen.force_update()
    self.workspace = self.screen.get_active_workspace()
    active_window_idx = 0
    for window in self.screen.get_windows():
      if window.is_skip_tasklist():
        continue
      if not window.is_visible_on_workspace(self.workspace):
        continue
      if window.is_minimized():
        continue
      box.pack_start(GSwitchIcon(window), True, True, 0)
      # this will actually select the "next window"
      if window.is_active():
	active_window_idx = len(self.get_windows())

    self.select_window(active_window_idx, None)

  def get_windows(self):
    return self.get_children()[0].get_children()

  def select_window(self, i, timestamp):
    windows = self.get_windows()
    n_windows = len(windows)
    if n_windows > 0:
      idx = i % n_windows
      windows[self.sel_child_idx].unselect(timestamp)
      windows[idx].select(timestamp)
      self.sel_child_idx = idx

  def on_key_press(self, win, event):
    if event.keyval == keysyms.Escape:
      gtk.main_quit()

    elif event.keyval == keysyms.Tab:
      self.select_window(self.sel_child_idx + 1, event.get_time())

  def on_key_release(self, win, event):
    if event.keyval == keysyms.Super_L or event.keyval == keysyms.Super_R:
      gtk.main_quit()



if __name__ == "__main__":
  sys.stderr.write("\n\nSTART\n\n")
  sys.stderr.flush()
  win = GSwitch()
  if len(win.get_windows()) > 0:
    GSwitch().show_all()
    gtk.main()
  else:
    sys.stderr.write("no windows")
