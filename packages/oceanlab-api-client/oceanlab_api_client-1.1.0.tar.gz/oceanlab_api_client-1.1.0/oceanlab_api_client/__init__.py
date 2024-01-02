""" A client library for accessing TIBCO Data Virtualization -- Published Web Services REST API """
from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
