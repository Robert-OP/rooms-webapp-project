

class Student(ndb.Model):
	student = ndb.StringProperty()

	def register(name):
		# add name in db and assign a student id and return id
		return '<p>Welcome %s, </p>' % student_id

	def login(id):


		if id_in_db:
			# route to checkin checkout room
			return '<p>Welcome %s, </p>'
		else:
			return '<p>Invalid ID, please register.</p>'

	def checkin(id):
		# get (clicked) room ID and name, checkin it
		# if user id already checkin in another room, auto-checkout
		return '<p>Check-in room %s successful.</p>' % room_name

	def checkout(id):
		# get room ID and name where the id is checkin and checkout of it
		return '<p>Check-out in room %s successful.</p>' % room_name