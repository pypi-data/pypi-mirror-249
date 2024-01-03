""" MusicBrainz OAuth2 API client and helpers. """

import datetime
from dataclasses import dataclass, field
from enum import StrEnum, auto
from urllib.parse import urlencode, urljoin

import requests  # type: ignore

# ref https://musicbrainz.org/doc/Development/OAuth2

OAUTH_ENDPOINT = "https://musicbrainz.org/oauth2/authorize"
OAUTH_TOKEN_ENDPOINT = "https://musicbrainz.org/oauth2/token"


class Scope(StrEnum):
    """Scopes for the MusicBrainz OAuth2 API."""

    PROFILE = auto()
    """ View the user's public profile information """
    EMAIL = auto()
    """ View the user's email. """
    TAG = auto()
    """ View and modify the user's private tags. """
    RATING = auto()
    """ View and modify the user's private ratings. """
    COLLECTION = auto()
    """ View and modify the user's private collections. """
    SUBMIT_ISRC = auto()
    """ Submit new ISRCs to the database. """
    SUBMIT_BARCODE = auto()
    """ Submit barcodes to the database. """


class AccessType(StrEnum):
    """Access types for the MusicBrainz OAuth2 API."""

    ONLINE = auto()
    """ Access when the user is present at the browser. """
    OFFLINE = auto()
    """ Access when the user is not present at the browser. """


class ApprovalPrompt(StrEnum):
    """Approval prompts for the MusicBrainz OAuth2 API."""

    AUTO = auto()
    """ The user should only be prompted for consent the first time through the sequence. """  # noqa: E501
    FORCE = auto()
    """ The user should be prompted for consent every time. """


class GrantType(StrEnum):
    """Grant types for the MusicBrainz OAuth2 API."""

    AUTHORIZATION_CODE = auto()
    REFRESH_TOKEN = auto()


@dataclass
class Token:
    """bearer token for the MusicBrainz API."""

    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    last_refresh: datetime.datetime = field(
        default_factory=datetime.datetime.utcnow
    )
    _auth_client: "AuthClient" = field(init=False, repr=False)

    @property
    def expired(self) -> bool:
        """Returns True if the token is expired, False otherwise."""
        return (
            datetime.datetime.utcnow() - self.last_refresh
        ).total_seconds() > self.expires_in

    def refresh(self, force: bool = False) -> "Token":
        """Refreshes the token if it is expired."""
        if not self.expired and not force:
            return self
        new_token = self._auth_client.refresh_token(self.refresh_token)
        for key, value in new_token.__dict__.items():
            setattr(self, key, value)
        return self


class AuthClient:
    """OAuth2 client for helping with obtaining api token.

    See https://musicbrainz.org/doc/Development/OAuth2
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        session: requests.Session | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._session = session or requests.Session()

    def generate_auth_url(
        self,
        scopes: list[str] | None = None,
        state: str = "",
        access_type: str = AccessType.OFFLINE,
        approval_prompt: str = ApprovalPrompt.AUTO,
    ) -> str:
        """Generates the authorization url for the user to follow."""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scopes) if scopes else "",
            "access_type": access_type,
            "approval_prompt": approval_prompt,
            "state": state,
        }

        return urljoin(OAUTH_ENDPOINT, "?" + urlencode(params))

    def _generate_token_fetch_params(
        self,
        code: str = "",
        refresh_token: str = "",
        token_type: str = "",
        grant_type: GrantType = GrantType.AUTHORIZATION_CODE,
    ) -> dict[str, str]:
        params = {
            "code": code,
            "refresh_token": refresh_token,
            "grant_type": grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "token_type": token_type,
        }
        if grant_type == GrantType.AUTHORIZATION_CODE:
            del params["refresh_token"]
        if grant_type == GrantType.REFRESH_TOKEN:
            del params["code"]
        return params

    def _fetch_token(self, params: dict[str, str]) -> Token:
        response = self._session.post(OAUTH_TOKEN_ENDPOINT, data=params)
        response.raise_for_status()
        token = Token(**response.json())
        token._auth_client = self  # type: ignore
        return token

    def retrieve_token(
        self,
        code: str,
        token_type: str = "",
    ) -> Token:
        """Retrieves the token for the user once they have followed the authorization url."""  # noqa: E501
        params = self._generate_token_fetch_params(
            code=code,
            token_type=token_type,
            grant_type=GrantType.AUTHORIZATION_CODE,
        )
        return self._fetch_token(params)

    def refresh_token(
        self,
        refresh_token: str,
        token_type: str = "",
    ) -> Token:
        """Refreshes the token."""
        params = self._generate_token_fetch_params(
            refresh_token=refresh_token,
            token_type=token_type,
            grant_type=GrantType.REFRESH_TOKEN,
        )
        return self._fetch_token(params)
