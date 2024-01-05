"""Module with exceptions for the Cisco Source."""


class CiscoSource(Exception):
    """Base class for all exceptions related to Cisco Support Source."""


class CiscoInvalidPIDException(CiscoSource):
    """Exception when a invalid PID is given."""


class CiscoCredentialsException(CiscoSource):
    """Exception when a invalid credentials are given."""
