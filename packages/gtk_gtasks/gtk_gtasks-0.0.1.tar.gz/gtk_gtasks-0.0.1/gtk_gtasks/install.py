from pathlib import Path
import sys
from importlib.util import find_spec

ICON = "icon.png"

def get_icon_path():
    mypkg = find_spec(__package__)
    if mypkg is None or mypkg.submodule_search_locations is None:
        raise Exception("Installation is screwed up")
    pkg_path = Path(next(iter(mypkg.submodule_search_locations)))
    return pkg_path / ICON

class DesktopInstaller():
    def __init__(self):
        self.install_path = Path.home() / ".local" / "share" / "applications" / "gtasks.desktop"
        self.executable_path = Path(sys.argv[0])
        self.icon_path = get_icon_path()
    
    def is_installed(self):
        return self.install_path.exists()

    def get_config(self) -> str:
        return f"""[Desktop Entry]
    Name=GTK Google Tasks
    Exec={self.executable_path.absolute()}
    Icon={self.icon_path.absolute()}
    Type=Application
    Categories=Utility"""

    def install(self):
        with open(self.install_path, "w") as f:
            f.write(self.get_config())

    def uninstall(self):
        self.install_path.unlink()