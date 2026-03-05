# SPDX-License-Identifier: AGPL-3.0-or-later
"""Authentication decorators."""

from functools import wraps
from flask import redirect, url_for, flash
from flask_babel import gettext
from flask_login import current_user


def admin_required(f):
    """Decorator to require admin privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash(gettext('Please log in to access this page.'), 'error')
            return redirect(url_for('login'))
        if not current_user.is_admin:
            flash(gettext('Admin privileges required.'), 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
