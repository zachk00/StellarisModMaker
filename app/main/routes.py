from flask import render_template
from flask_login import login_required
from . import main
from app.models import Mod, ModType
from flask_login import login_required, current_user

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    mod_types = ModType.query.all()
    user_mods = Mod.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user_mods=user_mods, mod_types=mod_types)

@main.route('/mod_editor/<mod_type>')
@login_required
def mod_editor(mod_type):
    mod_type = ModType.query.filter_by(name=mod_type).first_or_404()
    return render_template('mod_editor.html', mod_type=mod_type)

@main.route('/mod_editor/<int:mod_id>')
@login_required
def edit_mod(mod_id):
    mod = Mod.query.get_or_404(mod_id)
    return render_template('mod_editor.html', mod=mod, mod_type=mod.mod_type)