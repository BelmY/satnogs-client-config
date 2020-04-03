"""
APT helper module
"""
import apt
import lsb_release


def has_updates():
    """
    Check for package upgrades

    :return: Whether package upgrades are available
    :rtype: bool
    """
    cache = apt.Cache()
    cache.update()
    cache.open(None)
    cache.upgrade(dist_upgrade=True)
    if cache.get_changes():
        return True
    return False


def get_distro():
    """
    Get distribution information from lsb_release

    :return: Distribution information
    :rtype: dict
    """
    return lsb_release.get_distro_information()
