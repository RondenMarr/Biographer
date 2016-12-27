from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import UserAssignForm,CitizenForm
from .. import db
from ..models import  User, Citizen


def check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


@admin.route('/citizens')
@login_required
def list_citizens():
    check_admin()
    """
    List all citizens
    """
    citizens = Citizen.query.all()
    return render_template('admin/citizens/citizens.html',
                           citizens=citizens, title='Citizens')


@admin.route('/citizens/add', methods=['GET', 'POST'])
@login_required
def add_citizen():
    """
    Add a citizen to the database
    """
    check_admin()

    add_citizen = True

    form = CitizenForm()
    if form.validate_on_submit():
        citizen = Citizen(name=form.name.data,
                    description=form.description.data)

        try:
            # add citizen to the database
            db.session.add(citizen)
            db.session.commit()
            flash('You have successfully added a new citizen.')
        except:
            # in case citizen name already exists
            flash('Error: citizen name already exists.')

        # redirect to the citizens page
        return redirect(url_for('admin.list_citizens'))

    # load citizen template
    return render_template('admin/citizens/citizen.html', add_citizen=add_citizen,
                           form=form, title='Add Citizen')


@admin.route('/citizens/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_citizen(id):
    """
    Edit a citizen
    """
    check_admin()

    add_citizen = False

    citizen = Citizen.query.get_or_404(id)
    form = CitizenForm(obj=citizen)
    if form.validate_on_submit():
        citizen.name = form.name.data
        citizen.description = form.description.data
        db.session.add(citizen)
        db.session.commit()
        flash('You have successfully edited the citizen.')

        # redirect to the citizens page
        return redirect(url_for('admin.list_citizens'))

    form.description.data = citizen.description
    form.name.data = citizen.name
    return render_template('admin/citizens/citizen.html', add_citizen=add_citizen,
                           form=form, title="Edit Citizen")


@admin.route('/citizens/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_citizen(id):
    """
    Delete a citizen from the database
    """
    check_admin()

    citizen = Citizen.query.get_or_404(id)
    db.session.delete(citizen)
    db.session.commit()
    flash('You have successfully deleted the citizen.')

    # redirect to the citizens page
    return redirect(url_for('admin.list_citizens'))

    return render_template(title="Delete Citizen")

# User Views

@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


