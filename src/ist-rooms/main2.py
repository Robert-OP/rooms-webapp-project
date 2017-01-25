
from bottle import Bottle, debug, get, BaseRequest, run, template, request
from google.appengine.ext import ndb
import urllib, json

debug(True)
app = Bottle()

@app.route('/')
def index():
    return template('index.html')

@app.route('/login', method='POST')
def do_login():
    # get ID number from the page and see if it is in database
    id_no = request.forms.get('id_number')
    # OBS: what comes from the form is string
    # todo: make query to the database and see if ID number is in
    admin_id = '0'
    db_id = '11'
    db_username = 'Robert'
    if id_no == db_id:
    	# route to checkin in rooms available
    	return '<p>Welcome %s.</p>' % db_username
    elif id_no == admin_id:
    	# route to give priviledges to add rooms to the database
    	pass
    else:
    	return '<p>The ID %s is not registered, please register.</p>' % id_no

@app.route('/register', method='POST')
def do_register():
    # get username from the page and assign an ID and insert in database
    username = request.forms.get('username')
    # todo: make query to the database and see what is the last ID number
    id_no = 1
    output = '''<p> Hello %s, this is your ID: %d </p>
    <p> <form action="/" method = "get">
    		<input type="submit" value="Back to login">
    	</form> 
    </p>''' 
    return output % (username, id_no)
    # return '<p>Hello %s, this is your ID: %d</p>' % (username, id_no)

@app.get('/campus')
def list_campus():
    campus_url = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces'
    response = urllib.urlopen(campus_url)
    data = json.loads(response.read())
    campus_names = []
    for i in range(0, len(data)):
    	dic = data.pop()
    	campus_names.append(dic['name'])
    	# print campus_names
    # this should return to JavaScript it knows how to handle lists
    return "<p>Campuses: %s</p>" % campus_names

# Define a handler for 404 errors.
@app.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'