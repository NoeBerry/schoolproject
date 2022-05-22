from flask import Blueprint, render_template, request, flash, jsonify,redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, hotovo=False)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.home'))


    return render_template("home.html", user=current_user)

@views.route("/update/<note_id>")
def update(note_id):
    note = Note.query.filter_by(id=note_id).first()
    note.hotovo = not note.hotovo
    db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route("/completed")
def completed():
    complete = Note.query.filter_by(hotovo=True, user_id=current_user.id).all()

    return render_template("completed.html", complete=complete)

@views.route("/incompleted")
def incompleted():
    incomplete = Note.query.filter_by(hotovo=False, user_id=current_user.id).all()

    return render_template("incompleted.html", incomplete=incomplete)