#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Create initial admin user for SearXNG"""

import sys
from searx import settings
from searx.webapp import app
from searx.models import db
from searx import userdb

def create_admin():
    """Create initial admin user"""
    with app.app_context():
        db.create_all()

        username = input("Admin username: ").strip()
        email = input("Admin email: ").strip()
        password = input("Admin password: ").strip()

        if not username or not email or not password:
            print("All fields are required!")
            sys.exit(1)

        if userdb.get_user_by_username(username):
            print(f"User {username} already exists!")
            sys.exit(1)

        user = userdb.create_user(username, email, password, is_admin=True)
        print(f"Admin user {username} created successfully!")

if __name__ == '__main__':
    create_admin()
