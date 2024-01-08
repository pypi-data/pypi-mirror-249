import pkgutil
from pathlib import Path
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.1')
from gi.repository import Gtk, WebKit2, GdkPixbuf
from .version import __version__
from .install import DesktopInstaller, ICON

class WebViewWindow(Gtk.Window):
    URL = "https://assistant.google.com/tasks"
    PERSISTENCE_PATH = Path.home() / '.local' / 'share' / __package__ / f"{__package__}.db"
    
    def on_context_menu(self, web_view, context_menu, event, hit_test_result):
        if len(context_menu.get_items()) == 0:
            # Skip when a custom right click menu is showed.
            # Hacky but working :)
            return
        #context_menu.remove_all()
        action = Gtk.Action.new("InstallUninstallDesktop", "Install/Uninstall", "Install / Uninstall .desktop entry", Gtk.STOCK_NEW)
        action.connect("activate", self.on_install_uninstall)
        option = WebKit2.ContextMenuItem.new(action)
        context_menu.append(WebKit2.ContextMenuItem.new_separator())
        context_menu.append(option)

    def on_install_uninstall(self, menu_item):
        installer = DesktopInstaller()
        if installer.is_installed():
            action = "Uninstall"
            installer.uninstall()
        else:
            action = "Install"
            installer.install()
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, f"{action}ed correctly.\nPlease logout and login to see the difference.")
        dialog.set_title(f"{action} result")
        dialog.run()
        dialog.destroy()

    def __init__(self):
        Gtk.Window.__init__(self, title=f"GTK Google Tasks v{__version__}")
        self.set_default_size(350, 600)
        if not self.PERSISTENCE_PATH.parent.exists():
            self.PERSISTENCE_PATH.parent.mkdir(parents=True)
        icon_data = pkgutil.get_data(__package__, ICON)
        if icon_data:
            icon_pixbuf = GdkPixbuf.PixbufLoader.new_with_type('png')
            icon_pixbuf.write(icon_data)
            icon_pixbuf.close()
            self.set_icon(icon_pixbuf.get_pixbuf())
        webview = WebKit2.WebView()
        webview.connect("context-menu", self.on_context_menu)
        webview.load_uri(self.URL)
        ctx = WebKit2.WebContext.get_default()
        cookie_manager = ctx.get_cookie_manager()
        cookie_manager.set_persistent_storage(f"{self.PERSISTENCE_PATH.absolute()}", WebKit2.CookiePersistentStorage.SQLITE)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(webview)
        self.add(scrolled_window)
    

def main():
    win = WebViewWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.IconTheme.get_default().rescan_if_needed()
    Gtk.main()