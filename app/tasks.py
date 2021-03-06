from flask import redirect, url_for, flash
from app import app, celery, db, models

@celery.task()
def remove_room(roomname):
	room = models.Room.query.filter_by(roomname=roomname).all()
	room[0].approved_users = []

	users = models.User.query.filter(models.User.approved_rooms.any(roomname=roomname)).all()
	for user in users:
		user.approved_rooms = list(user.approved_rooms).remove(room)

	models.Room.query.filter_by(roomname=roomname).delete()
	db.session.commit()

	return 'Room ' + roomname + ' deleted.'

@celery.task()
def update_available_rooms():
    app.config['AVAILABLE_ROOMS'] = models.Room.query.all()
    return 'Available room list updated'

