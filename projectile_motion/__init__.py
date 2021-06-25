"""CoSApp project Projectile Motion

Projectile Motion Simulation
"""
from ._version import __version__


def find_resources(filename: str = "") -> str:
    """Returns the fullpath of a file in resources folder.
    
    Parameters
    ----------
    filename: str, optional
        File or directory looked for; default resources folder
    
    Returns
    -------
    str
        Full path to resources
    """
    import os
    fullpath = os.path.realpath(os.path.join(__path__[0], "resources", filename))
    if not os.path.exists(fullpath):
        raise FileNotFoundError(fullpath)
    return fullpath


def _cosapp_lab_load_module():
    from projectile_motion.systems import ProjectileMotion
    from cosapp_lab.widgets import SysExplorer
    s = ProjectileMotion("s")
    s.run_once()
    a = SysExplorer(s, template = find_resources('ui.json'))

def _cosapp_lab_module_meta():
    return {"title": "Projectile Motion Demo", "description": "Projectile motion modelling demo", "version": "0.1.0"}



__all__ = ["drivers", "ports", "systems", "tools"]
