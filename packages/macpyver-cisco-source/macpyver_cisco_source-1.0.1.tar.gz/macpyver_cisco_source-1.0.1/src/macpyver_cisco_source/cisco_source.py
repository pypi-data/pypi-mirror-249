"""Module that contains the CiscoSource class."""


from datetime import datetime

from cisco_support import SS  # type:ignore
from macpyver_core.model import Version
from macpyver_core.version_source import VersionSource

from .exceptions import CiscoCredentialsException, CiscoInvalidPIDException


class CiscoSource(VersionSource):
    """MacPyVer VersionSource for Cisco Support."""

    _client_key: str
    _client_secret: str

    @classmethod
    def set_credentials(cls, client_key: str, client_secret: str) -> None:
        """Set the credentials for the Cisco API.

        Sets the credentials for the Cisco API. This is a class method so it
        can be set ahead of time and for all objects.

        Args:
            client_key: the client key for Cisco Support.
            client_secret: the client secret for Cisco Support.
        """
        cls._client_key = client_key
        cls._client_secret = client_secret

    def _convert_cisco_datetime_to_datetime(
            self, cisco_datetime: str) -> datetime:
        """Convert a Cisco datetime to a Python datetime object.

        Args:
            cisco_datetime: the datetime string that we get from Cisco. This is
                in the format '26-Oct-1986'.

        Returns:
            A Python datetime object for the given date.
        """
        return datetime.strptime(cisco_datetime, '%d-%b-%Y')

    def _convert_cisco_version_to_version(
            self, cisco_version: dict) -> Version:
        """Convert a Cisco version to a `Version` object.

        When retrieving versions from Cisco, we have to convert them to a
        Version object.

        Args:
            cisco_version: the dict object we get from Cisco API.

        Returns:
            The created Version object.
        """
        version_name = cisco_version['releaseFormat1']
        return Version(
            version=version_name,
            release_datetime=self._convert_cisco_datetime_to_datetime(
                cisco_version['releaseDate'])
        )

    def get_all_versions(self) -> list[Version]:
        """Get all versions for this specific PID.

        Gets all versions for the given PID. The PID should be given in the
        'extra_information' attribute of the Software object with the keyname
        'cisco_device_pid'.

        If the 'cisco_only_suggested' key is given in the 'extra_information'
        field of the Software object and it evaluates to True, only suggested
        software will be returned.

        Returns:
            A list with Version objects that contains the versions for the
            given software.

        Raises:
            CiscoCredentialsException: credentials are incorrect.
            CiscoInvalidPIDException: the given PID is incorrect.
        """
        product_pid = self.software.extra_information.get(
            'cisco_device_pid', None)

        if not isinstance(product_pid, str):
            raise CiscoInvalidPIDException('Invalid PID-type given')

        try:
            sw_sug = SS(key=self._client_key,
                        secret=self._client_secret)
        except KeyError as exc:
            raise CiscoCredentialsException(
                'Invalid client credentials') from exc

        software = sw_sug.getCompatibleAndSuggestedSoftwareReleasesByProductID(
            product_pid
        )
        if 'suggestions' not in software:
            raise CiscoInvalidPIDException('Invalid PID given')

        suggestions = software['suggestions']

        only_suggested = self.software.extra_information.get(
            'cisco_only_suggested', False)
        if only_suggested:
            suggestions = filter(
                lambda release: release['isSuggested'] == 'Y', suggestions)

        return [self._convert_cisco_version_to_version(suggestion)
                for suggestion in suggestions]
