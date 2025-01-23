#!/usr/bin/env python3
"""
Implementation that adds an expiration date to session_id
"""
from api.v1.auth.session_auth import SessionAuth
from os import environ
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Extension of SessionAuth that handles expiration of session_id"""

    def __init__(self):
        """Initialize with session expiration duration"""
        try:
            self.session_duration = int(environ.get("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Overload create_session method to include session expiration
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user_id from a session_id with expiration handling
        """
        if not session_id:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if not session_dictionary:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get("user_id")

        created_at = session_dictionary.get("created_at")
        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_dictionary.get("user_id")
