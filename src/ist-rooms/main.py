
from bottle import Bottle, debug, get, BaseRequest, run, template, request, response
from google.appengine.ext import ndb
import urllib, json
from json import dumps

debug(True)
app = Bottle()

@app.route('/')
def index():
    return template('index.html')

@app.post('/login/student')
def do_login():
    # what comes from the form is string
    id_no = request.forms.get('id_number')
    # get ID number from the page and see if it is in database
    # fetch one entry of student with that specific ID
    user = Student.get_by_id(int(id_no))
    if user != None:
        # route to give priviledges to add rooms to the database
        # todo: make query to the database and see if ID number is in 
        return template('student.html') 
    else:
        # return in case ID is not registered
        return '''<p>The ID %s is not registered, please register.</p>
                <form action="/" method="get">
                    <input type="submit" value="Home">
                </form>''' % id_no

@app.post('/login/admin')
def do_login():
    return template('admin.html')

class Student(ndb.Model):
    name = ndb.StringProperty()
    checkin = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

@app.route('/register', method='POST')
def do_register():
    # get username from the page and assign an ID and insert in database
    username = request.forms.get('username')
    student = Student(name=username, checkin=0)
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
    occupancy = ndb.IntegerProperty()
    capacity = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

@app.post('/add/<room>/<capacity>')
def add_room(room, capacity):
    r = Room(name=room, occupancy=0, capacity=capacity)
    key = r.put()
    return 'Room %s added with key %s' % (r, str(key.id()))

@app.route('/showrooms')
def show_rooms():
    out = ''
    rooms = Room.query()
    for r in rooms:
        out += ' Name: ' + r.name + ' |Occupancy: ' + str(r.occupancy) + ' |Total Capacity: ' + r.capacity + ' |ID: ' + str(r.key.id()) + ' |Date: ' + str(r.date) + '<br>'
    return out

@app.route('/students')
def show_rooms():
    out = ''
    students = Student.query()
    for s in students:
        out += 'ID: ' + str(s.key.id()) + ' |Name: ' + s.name + ' | Enrol Date: ' + str(s.date) + '<br>'
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

@app.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'