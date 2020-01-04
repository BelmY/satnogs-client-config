"""
gr-satnogs module
"""


class GrSatnogs():
    """
    Get and set gr-satnogs configuration
    """
    @property
    def gr_satnogs_version(self):
        """
        Get gr-satnogs version
        """
        raise NotImplementedError

    def probe_soapysdr(self):
        """
        Probe SoapySDR hardware
        """
        raise NotImplementedError
