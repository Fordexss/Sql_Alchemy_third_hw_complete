from sqlalchemy import select
from flask import render_template, request, redirect, url_for
from flask.blueprints import Blueprint
from sqlalchemy.orm import selectinload
from app.database import Session
from app.models import Lesson, Group

bp = Blueprint("lesson", __name__)


@bp.route('/', methods=["GET", "POST"])
def lesson_add():
    if request.method == "POST":
        with Session() as session:
            title = request.form.get("title")
            group_ids = [int(group_id) for group_id in request.form.getlist("groups")]

            items_groups = session.query(Group).filter(Group.id.in_(group_ids)).all()

            new_lesson = Lesson(title=title)
            new_lesson.groups = items_groups

            session.add(new_lesson)
            session.commit()

            return redirect(url_for('lesson.lesson_add'))

    with Session() as session:
        lessons = session.query(Lesson).options(selectinload(Lesson.groups)).all()
        groups = session.query(Group).all()

    return render_template("lesson/managment.html", lessons=lessons, groups=groups)


@bp.route('/<int:id>', methods=["GET"])
def lesson_get(id):
    with Session() as session:
        query = select(Lesson).where(Lesson.id == id).options(selectinload(Lesson.groups))
        lesson = session.execute(query).scalar()

    return render_template("main.html", content=lesson)
