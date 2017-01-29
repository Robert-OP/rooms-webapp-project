
from bottle import Bottle, debug, get, BaseRequest, run, template, request, response
from google.appengine.ext import ndb
import urllib, json
from json import dumps

debug(True)
app = Bottle()

@app.route('/')
def index():
    return template('index.html')

@app.route('/login', method='POST')
def do_login():
    # get ID number from the page and see if it is in database
    id_no = request.forms.get('id_number')
    print id_no
    admin_id = '0'
    db_id = '11'
    db_username = 'Robert'
    # OBS: what comes from the form is string
    if id_no == db_id:
        # route to checkin in rooms available
        return '<p> Welcome %s. </p>' % db_username
    elif id_no == admin_id:
        # route to give priviledges to add rooms to the database
        # todo: make query to the database and see if ID number is in 
        return template('admin.html') 
    else:
        return '<p>The ID %s is not registered, please register.</p>' % id_no

class Student(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

@app.route('/register', method='POST')
def do_register():
    # get username from the page and assign an ID and insert in database
    username = request.forms.get('username')
    student = Student(name = username)
    key = student.put()
    # todo: make query to the database and see what is the last ID number
    return 'Hello %s, this is your ID: %s' % (student, str(key.id()))

@app.get('/entity/<id>')
def list_campus(id):
    return template('entity.html')

@app.get('/room/<id>')
def list_campus(id):
    return template('room.html')

class Room(ndb.Model):
    # model an individual room with name, capacity, date
    name = ndb.StringProperty()
    occupancy = 0 
    capacity = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

@app.post('/add/<room>/<capacity>')
def add_room(room, capacity):
    r = Room(name = room, capacity = capacity)
    key = r.put()
    return 'Room %s added with key %s' % (r, str(key.id()))

@app.route('/showrooms')
def show_rooms():
    out = ''
    rooms = Room.query()
    for r in rooms:
        out += 'ID: ' + str(r.key.id()) + ' Name: ' + r.name + ' Capacity: ' + str(r.capacity) + ' Date: ' + str(r.date) + '<br>'
    return out

@app.route('/students')
def show_rooms():
    out = ''
    students = Student.query()
    for s in students:
        out += 'ID: ' + str(s.key.id()) + ' Name: ' + s.name + ' Date: ' + str(s.date) + '<br>'
    return out

@app.get('/spaces/<id>')
def req(id):
    campus_url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/' + id
    response = urllib.urlopen(campus_url)
    response.content_type = 'application/json'
    return response.read()

@app.get('/spaces')
def req1():
    campus_url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
    response = urllib.urlopen(campus_url)
    response.content_type = 'application/json'
    return response.read()


# Define a handler for 404 errors.
@app.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'