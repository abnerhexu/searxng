# SPDX-License-Identifier: AGPL-3.0-or-later
"""User database operations."""

from datetime import datetime
from searx.models import db, User, UserPreference, SearchHistory


def create_user(username, email, password, is_admin=False):
    """Create a new user."""
    user = User(username=username, email=email, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(user_id):
    """Get user by ID."""
    return db.session.get(User, user_id)


def get_user_by_username(username):
    """Get user by username."""
    return db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()


def get_user_by_email(email):
    """Get user by email."""
    return db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()


def update_last_login(user_id):
    """Update user's last login time."""
    user = db.session.get(User, user_id)
    if user:
        user.last_login = datetime.utcnow()
        db.session.commit()


def get_user_preference(user_id, key, default=None):
    """Get user preference."""
    pref = db.session.execute(
        db.select(UserPreference).filter_by(user_id=user_id, setting_key=key)
    ).scalar_one_or_none()
    return pref.setting_value if pref else default


def set_user_preference(user_id, key, value):
    """Set user preference."""
    pref = db.session.execute(
        db.select(UserPreference).filter_by(user_id=user_id, setting_key=key)
    ).scalar_one_or_none()
    if pref:
        pref.setting_value = value
        pref.updated_at = datetime.utcnow()
    else:
        pref = UserPreference(user_id=user_id, setting_key=key, setting_value=value)
        db.session.add(pref)
    db.session.commit()


def get_all_user_preferences(user_id):
    """Get all preferences for a user."""
    prefs = db.session.execute(
        db.select(UserPreference).filter_by(user_id=user_id)
    ).scalars().all()
    return {p.setting_key: p.setting_value for p in prefs}


def add_search_history(user_id, query, engines=None, language=None, safe_search=None, results_count=None):
    """Add search history entry."""
    history = SearchHistory(
        user_id=user_id,
        query=query,
        engines=engines,
        language=language,
        safe_search=safe_search,
        results_count=results_count
    )
    db.session.add(history)
    db.session.commit()


def get_search_history(user_id, limit=50):
    """Get user's search history."""
    return db.session.execute(
        db.select(SearchHistory).filter_by(user_id=user_id).order_by(SearchHistory.created_at.desc()).limit(limit)
    ).scalars().all()


def delete_search_history(user_id, history_id):
    """Delete a search history entry."""
    history = db.session.execute(
        db.select(SearchHistory).filter_by(id=history_id, user_id=user_id)
    ).scalar_one_or_none()
    if history:
        db.session.delete(history)
        db.session.commit()
        return True
    return False


def clear_search_history(user_id):
    """Clear all search history for a user."""
    db.session.execute(
        db.delete(SearchHistory).filter_by(user_id=user_id)
    )
    db.session.commit()


def get_all_users():
    """Get all users (admin only)."""
    return db.session.execute(db.select(User)).scalars().all()


def toggle_user_status(user_id, is_active):
    """Enable or disable a user."""
    user = db.session.get(User, user_id)
    if user:
        user.is_active = is_active
        db.session.commit()
        return True
    return False


def set_admin_status(user_id, is_admin):
    """Set user admin status."""
    user = db.session.get(User, user_id)
    if user:
        user.is_admin = is_admin
        db.session.commit()
        return True
    return False
