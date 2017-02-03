
from bottle import Bottle, debug, get, BaseRequest, run, template, request, response
from google.appengine.ext import ndb
import urllib, json
from json import dumps

debug(True)
app = Bottle()

@app.route('/')
# main page of room booking web application
def index():
    return template('index.html')

# working with form input
# @app.post('/login/student')
# def do_login():
#     # what comes from the form is string
#     id_no = request.forms.get('id_number')
#     # get ID number from the page and see if it is in database
#     # fetch one entry of student with that specific ID
#     user = Student.get_by_id(int(id_no))
#     if user != None:
#         # route to give priviledges to add rooms to the database
#         # todo: make query to the database and see if ID number is in 
#         return template('student.html') 
#     else:
#         # return in case ID is not registered
#         return '''<p>The ID %s is not registered, please register.</p>
#                 <form action="/" method="get">
#                     <input type="submit" value="Home">
#                 </form>''' % id_no

@app.get('/student/<id>')
# gets input ID from user input with JS and performs login
def login_student(id):
    # get ID number from the page and see if it is in database
    # fetch one entry of student with that specific ID
    user = Student.get_by_id(int(id))
    # it returns None if there is no student with that ID registered
    if user != None:
        out = []
        rooms = Room.query()
        for r in rooms:
            room = {'id':r.key.id(), 'name':r.name, 'capacity':r.capacity, 'occupancy':r.occupancy}
            out.append(room)
        return template('student.html', data=json.dumps(out), user=user.name) 
    else:
        # return in case ID is not registered
        return '''<p>The ID %s is not registered, please register.</p>
                <form action="/" method="get">
                    <input type="submit" value="Home">
                </form>''' % id

@app.post('/student/<student_id>/<room_id>')
# for the logged in student ID, performs the checkin into the room desired
def checkin_room(student_id, room_id):
    student = Student.get_by_id(int(student_id))
    room = Room.get_by_id(int(room_id))
    
    if room.key.id() in student.room:
        # lroom = Room.get_by_id(int(student.room.keys()[0]))
        # student.room.pop(lroom.key.id())
        # student.checkin = False
        # student.put()
        return '<h4>Already logged in room %s</h4>' % room.name
    elif student.checkin:
        # checkout of last room (lroom)
        lroom = Room.get_by_id(int(student.room.keys()[0]))
        lroom.students.pop(student.key.id())
        lroom.occupancy -= 1
        lroom.put()
        # store in student new room
        student.room.pop(lroom.key.id()) 
        student.room[room.key.id()] = room.name
        # return '<h4>Already logged in room %s</h4>' % room.name
        # checkin - store student details in room
        room.students[student.key.id()] = student.name
        room.occupancy += 1
        student.put()
        room.put()
        return '<h4>Checkout %s & checkin %s</h4>' % (lroom.name, room.name)
    else:
        # store in student room details
        student.room[room.key.id()] = room.name
        student.checkin = True
        # checkin - store student details in room
        room.students[student.key.id()] = student.name
        room.occupancy += 1
        student.put()
        room.put()
        return '<h4>Checked in room: %s</h4>' % room.name
    # return room.students

@app.post('/login/admin')
# shows the admin page which afterwards gets info from fenix platform
def do_login():
    return template('admin.html')

class Student(ndb.Model):
# models an individual student with name and other properties
    name = ndb.StringProperty()
    checkin = ndb.BooleanProperty()
    room = ndb.PickleProperty(default={})
    date = ndb.DateTimeProperty(auto_now_add=True)

@app.route('/register', method='POST')
# registers users into datastore with their input name and retrieves an UNIQUE ID
def do_register():
    # get username from the page and add to datastore
    username = request.forms.get('username')
    student = Student(name=username, checkin=False)
    key = student.put()
    return '''<h3>Hello %s, this is your ID: %s</h3>
            <form action="/" method="get">
                <input type="submit" value="Home">
            </form>''' % (student.name, str(key.id()))

@app.get('/entity/<id>')
# shows from fenix platform the list of spaces (campuses/buildings/floors/rooms)
def list_campus(id):
    return template('entity.html')

@app.get('/room/<id>')
# shows the room with that specific ID, name, total capacity
def list_room(id):
    return template('room.html')

class Room(ndb.Model):
# model an individual room with name, capacity, occupancy, student dictionary, date
    name = ndb.StringProperty()
    occupancy = ndb.IntegerProperty(default=0)
    capacity = ndb.IntegerProperty()
    students = ndb.PickleProperty(default={})
    date = ndb.DateTimeProperty(auto_now_add=True)

@app.post('/add/<room>/<capacity>')
# add room with name and room total capacity in datastore
def add_room(room, capacity):
    r = Room(name=room, capacity=int(capacity))
    key = r.put()
    return 'Room: %s added with ID: %s' % (r.name, str(key.id()))

@app.route('/showrooms')
# shows all rooms added by admin in datastore + students checked in
def show_rooms():
    out = ''
    rooms = Room.query()
    for r in rooms:
        out += ' Name: ' + r.name + ' |Occupancy: ' + str(r.occupancy) + ' |Capacity: ' + str(r.capacity) + ' |ID: ' + str(r.key.id()) + ' |Date: ' + str(r.date) + '<br>' + str(dumps(r.students)) + '<br>'
    return out

@app.route('/students')
# shows all students registered in datastore and their details
def show_students():
    out = ''
    students = Student.query()
    for s in students:
        out += 'ID: ' + str(s.key.id()) + ' |Name: ' + s.name + ' |Checkin: ' + str(dumps(s.room)) + ' | Enrol Date: ' + str(s.date) + '<br>'
    return out

@app.get('/spaces/<id>')
# get (JSON) spaces (campus/building/floor/room) from fenix platform
def req(id):
    campus_url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/' + id
    response = urllib.urlopen(campus_url)
    response.content_type = 'application/json'
    return response.read()

@app.get('/spaces')
# get campuses (JSON) from fenix platform
def req1():
    campus_url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
    response = urllib.urlopen(campus_url)
    response.content_type = 'application/json'
    return response.read()

@app.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'