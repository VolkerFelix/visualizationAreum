from flask import session


def is_authenticated():
    """Check if user is authenticated"""
    return "token" in session and session["token"]
