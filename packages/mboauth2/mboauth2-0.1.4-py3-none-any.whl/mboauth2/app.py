""" MusicBrainz OAuth2 API client and helpers. """

import datetime
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlencode, urljoin

import requests  # type: ignore

# ref https://musicbrainz.org/doc/Development/OAuth2

OAUTH_ENDPOINT = "https://musicbrainz.org/oauth2/authorize"
OAUTH_TOKEN_ENDPOINT = "https://musicbrainz.org/oauth2/token"


class Scope(str, Enum):
    """Scopes for the MusicBrainz OAuth2 API."""

    PROFILE = "profile"
    """ View the user's public profile information """
    EMAIL = "email"
    """ View the user's email. """
    TAG = "tag"
    """ View and modify the user's private tags. """
    RATING = "rating"
    """ View and modify the user's private ratings. """
    COLLECTION = "collection"
    """ View and modify the user's private collections. """
    SUBMIT_ISRC = "submit_isrc"
    """ Submit new ISRCs to the database. """
    SUBMIT_BARCODE = "submit_barcode"
    """ Submit barcodes to the database. """


class AccessType(str, Enum):
    """Access types for the MusicBrainz OAuth2 API."""

    ONLINE = "online"
    """ Access when the user is present at the browser. """
    OFFLINE = "offline"
    """ Access when the user is not present at the browser. """


class ApprovalPrompt(str, Enum):
    """Approval prompts for the MusicBrainz OAuth2 API."""

    AUTO = "auto"
    """ The user should only be prompted for consent the first time through the sequence. """  # noqa: E501
    FORCE = "force"
    """ The user should be prompted for consent every time. """


class GrantType(str, Enum):
    """Grant types for the MusicBrainz OAuth2 API."""

    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"


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
            "access_type": access_type.lower(),
            "approval_prompt": approval_prompt.lower(),
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
