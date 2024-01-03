""" OAuth2 client for MusicBrainz API.

See https://musicbrainz.org/doc/Development/OAuth2
"""

from .app import AccessType, AuthClient, Scope, Token

__all__ = ["AuthClient", "Scope", "AccessType", "Token"]
