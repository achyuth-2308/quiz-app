from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.models import Subject, Chapter, Quiz
from controllers.forms import SubjectForm, ChapterForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def dashboard():
    subjects = Subject.query.all()
    return render_template('dashboard.html', subjects=subjects)

@admin_bp.route('/admin/add_sub', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('add_sub.html')

@admin_bp.route('/admin/subject_edit/<int:subject_id>', methods=['GET', 'POST'])
def subject_editject(subject_id):
    subject = Subject.query.get(subject_id)
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template('subject_edit.html', subject=subject)

@admin_bp.route('/admin/delete_sub/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/subjects/<int:subject_id>/chapters', methods=['GET', 'POST'])
def subject_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = subject.chapters.all()
    return render_template('subject_chapters.html', subject=subject, chapters=chapters)

@admin_bp.route('/admin/subjects/<int:subject_id>/chapters/new', methods=['GET', 'POST'])
def new_subject_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = ChapterForm()
    if form.validate_on_submit():
        chapter = Chapter(name=form.name.data, subject=subject)
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter created successfully!', 'success')
        return redirect(url_for('subject_chapters', subject_id=subject_id))
    return render_template('new_subject_chapter.html', form=form, subject=subject)

@admin_bp.route('/admin/subjects/<int:subject_id>/chapters/<int:chapter_id>/edit', methods=['GET', 'POST'])
def subject_editject_chapter(subject_id, chapter_id):
    subject = Subject.query.get_or_404(subject_id)
    chapter = Chapter.query.get_or_404(chapter_id)
    form = ChapterForm()
    if form.validate_on_submit():
        chapter.name = form.name.data
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('subject_chapters', subject_id=subject_id))
    form.name.data = chapter.name
    return render_template('subject_editject_chapter.html', form=form, subject=subject, chapter=chapter)

@admin_bp.route('/admin/subjects/<int:subject_id>/chapters/<int:chapter_id>/delete', methods=['POST'])
def delete_subject_chapter(subject_id, chapter_id):
    subject = Subject.query.get_or_404(subject_id)
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully!', 'success')
    return redirect(url_for('subject_chapters', subject_id=subject_id))