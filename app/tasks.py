from flask import redirect, url_for, flash
from app import app, celery, db, models

@celery.task()
def remove_room(roomname):
	room = models.Room.query.filter_by(roomname=roomname)
	room.approved_users = []
	models.Room.query.filter_by(id=roomId).delete()
	db.session.commit()

	return 'Room ' + roomname + ' deleted.'