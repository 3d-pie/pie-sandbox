"""HTTP routes for the Flask application.

This module defines a blueprint that aggregates all URL routes for the
application.  Routes handle authentication (in a very rudimentary
fashion), file uploads, and listing items.  Real authentication,
RBAC, and file parsing/rendering are deferred to a human developer.
"""

import os
from typing import List, Optional

from flask import (
    Blueprint,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from .models import db, Item, User
from . import services


bp = Blueprint('main', __name__)


def _get_current_user() -> Optional[User]:
    """Retrieve the currently logged in user from the session.

    Returns:
        The :class:`User` instance if a user_id exists in the session,
        otherwise ``None``.
    """
    user_id = session.get('user_id')
    if user_id is None:
        return None
    return User.query.get(user_id)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Render the login form and handle dummy authentication.

    On GET requests this route returns the login form.  On POST
    requests it creates or retrieves a user with the provided
    username, stores the user ID in the session and then redirects
    to the RBAC demo page.  Passwords are ignored for this stub.
    """
    if request.method == 'POST':
        username = request.form.get('username') or 'user'
        # Create or fetch a user with the given username.  In a real
        # application you would verify the password and use a proper
        # authentication mechanism.  This is a stub.
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username, password=generate_password_hash(request.form.get('password', '')))
            db.session.add(user)
            db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('main.rbac_demo'))
    return render_template('login.html')


@bp.route('/logout')
def logout():
    """Log out the current user by clearing the session."""
    session.pop('user_id', None)
    return redirect(url_for('main.login'))


@bp.route('/rbac/demo')
def rbac_demo():
    """Demonstration page for role‑based access control.

    If a user is logged in, renders a template showing the user's
    username and a placeholder list of roles.  Otherwise redirects
    to the login page.
    """
    user = _get_current_user()
    if user is None:
        return redirect(url_for('main.login'))
    # Placeholder roles list.  A future implementation will replace
    # this with real role and permission information.
    roles: List[str] = []
    return render_template('rbac_demo.html', user=user, roles=roles)


@bp.route("/admin/roles")
def admin_roles():
    user = _get_current_user()
    if user is None:
        return redirect(url_for('main.login'))
    # 🔒 Simple guard: only superadmins may view this page.
    # Replace with has_perm("manage_roles") once Challenge 1 is done.
    if not getattr(user, "is_primary_admin", False):
        return redirect(url_for("main.rbac_demo"))

    roles = Role.query.order_by(Role.name).all() if hasattr(Role, "name") else []
    return render_template("admin_roles.html", roles=roles)


@bp.route('/gcode/upload', methods=['GET', 'POST'])
def gcode_upload():
    """Upload a G‑Code file and return parsed statistics.

    GET requests render the upload form.  POST requests accept a file
    upload, save it to the configured uploads directory and call the
    parser stub in :mod:`app.services`.  The result is returned as
    JSON.  Errors return a 400 response with an error message.
    """
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == '':
            return jsonify({'error': 'No file provided'}), 400
        filename = secure_filename(file.filename)
        # Determine destination path relative to project root
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, filename)
        file.save(save_path)
        # Call the parser stub and return whatever it returns as JSON
        result = services.gcode_parser(save_path)
        return jsonify(result)
    return render_template('gcode_upload.html')


@bp.route('/thumbs/upload', methods=['POST'])
def thumbs_upload():
    """Upload a 3D model file and create a thumbnail entry.

    This route saves the uploaded file to the uploads directory,
    calls the thumbnail rendering stub and then creates an :class:`Item`
    record with the filename and the returned thumbnail path (if any).
    Finally it redirects to the items list.  The redirect status code
    is 302 which is accepted by the self‑check script.
    """
    file = request.files.get('file')
    if file is None or file.filename == '':
        return jsonify({'error': 'No file provided'}), 400
    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)
    # Generate a thumbnail.  The stub returns None by default.
    thumb_relative_path = services.thumbnail_render(save_path)
    # Create an Item record with the filename and meta information
    item_meta = {}
    if thumb_relative_path:
        item_meta['thumb'] = thumb_relative_path
    item = Item(filename=filename, meta=item_meta)
    db.session.add(item)
    db.session.commit()
    # Redirect to the items list.  A 302 Found is sufficient here.
    return redirect(url_for('main.items'))


@bp.route('/items')
def items():
    """Render a table of all uploaded items."""
    all_items = Item.query.all()
    return render_template('items_list.html', items=all_items)