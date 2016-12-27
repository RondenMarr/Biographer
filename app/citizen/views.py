from flask import abort, render_template
from flask_login import current_user, login_required

from . import citizen


@citizen.route('/')
def citizenpage():
    """
    Render the citizen page template on the / route
    """
    return render_template('citizen/index.html', title="Welcome")


@citizen.route('/citizen')
@login_required
def dashboard():
    """
    Render the dashboard template on the /citizen route
    """
    return render_template('citizen/dashboard.html', title="Dashboard")


@citizen.route('/admin/citizen')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('citizen/admin_dashboard.html', title="Dashboard")
