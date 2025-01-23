#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True

        # Normalize the path by ensuring it does not end with a trailing slash
        path = path.rstrip('/')
        excluded_paths = [excluded.rstrip('/') for excluded in excluded_paths]

        for excluded_path in excluded_paths:
            # Handle wildcard at the end of the excluded path
            if excluded_path.endswith('*'):
                base_path = excluded_path[:-1]  # Remove the '*'
                if path.startswith(base_path):
                    return False
            else:
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None
