from flask import Flask, render_template, url_for, request, redirect
from flask import json
from flask.helpers import url_for
import json
import csv

''''
Quickstart in
https://flask.palletsprojects.com/en/1.1.x/quickstart/

NOTE:
from a virtualenv I can export the requirements using:
$ pip freeze > requirements.txt

'''

app = Flask(__name__)

'''
To start the server:
    $env:FLASK_APP = "server.py"
    flask run

Note: for dev/debug mode use:
$env:FLASK_ENV = "development"

This way any time you change the file you can just reload the page instead of
restarting the server

NOTE: Flask check for the html file in a folder called './templates' by default
NOTE: For CSS files you need to place them in a './static' folder

Adding an icon (favicon):
to the html:
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">

{{ }} -> expression -> jinja

To host on a server use Pythonanywhere

'''


# Root of the page: '/'
#-> http://127.0.0.1:5000/

@app.route('/')
def my_home():

    return render_template('./index.html')

#Dynamically accept the page name:
@app.route('/<string:page_name>')
def custom_page(page_name):
    if page_name == 'thankyou.html':
        # Use request.args to get the url_from argument email
        # in submit_form
        email=request.args['email']
        print(f"in here {page_name} {email}")
        return render_template(page_name, email=email)

    return render_template(page_name)

#use the flask request method to access data from the form
# Let's also give a thank you message once the form has been submitted
# To do so I just copy the contact.html and create a new file
# called thankyou.html (substitute the form with a message)
# USe the "redirect" from flask
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            # convert the request response to a dict
            data = request.form.to_dict()
            # Save to a json file
            to_json(data)
            # Save to a csv file
            to_csv(data)

            return redirect(url_for('custom_page', page_name='thankyou.html', email=data['email'] ))
        except:
            return 'Could not save to db'
    else:
        return "Not allowed"

# Save the form data to a json file
def to_json(data):
    with open('database.json', mode='a') as db:
        json.dump(data, db, indent=4, separators=(',', ':'))

# Save the form data to a csv file
def to_csv(data):
    email, subject, message = data.values()
    with open('database.csv', mode='a', newline='') as db:
        writer = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([email, subject, message])


# @app.route('/index.html')
# def home():

#     return render_template('./index.html')


# @app.route('/about.html')
# def about():

#     return render_template('./about.html')

# @app.route('/components.html')
# def components():

#     return render_template('./components.html')

# @app.route('/contact.html')
# def contact():

#     return render_template('./contact.html')

# @app.route('/work.html')
# def work():
#     return render_template('./work.html')

# @app.route('/works.html')
# def works():

#     return render_template('./works.html')

# #If you want to pass a variable:
# @app.route('/<username>')
# def hello(username='username'):
#     # convert the variable in the template:
#     return render_template('./index.html', username=username)

# #If you want to pass 2 variables -> one has to be an int:
# @app.route('/<username>/<int:post_id>')
# def hello_numbered(username='username', post_id=None):

#     return render_template('./index.html', username=username, \
#                            post_id=post_id)

# # Another route: '/blog'
# #-> http://127.0.0.1:5000/blog
# @app.route('/blog')
# def blog():
#     return 'This is my blog'

# @app.route('/about.html')
# def about():
#     return render_template('./about.html')

