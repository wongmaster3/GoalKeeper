===========
Goal Keeper
===========

Features
========

This platform helps keep track of the goals you have. You can make an account, add goals, monitor goals,
update goals, and interact with other users. There are also newsfeed and forum features where you can 
check out what others say about different topics in technology, heatlh, fitness, and so much more. Another
key feature on the platform is the ability to add friends to help keep each other accountable for finishing
goals. There is so much to do on this platform, so enjoy it!

Install and Run
===============

To install and run the program with Docker::

    docker-compose up --build -d

Then go to http://localhost:5000/

If you want to see the application on the web, the application is located at http://35.174.165.19:5000/

Code Structure and Design
=========================

File Structure
--------------

The main source code is located in the web/goalkeeper folder. We put all of our html and python 
files in the folder. Each subdirectory, represents a component of the application. For example, 
we have an 'accounts' folder which will handle authentication (login and registering) and a 
'friends' folder which will handle adding friends, and profiles of friends.

We used flask's blueprints to help us connect the frontend templates to the backend. 

A typical file structure of a component of the the application would look like this::
    
    component_name
        |
        |--__init__.py
        |--forms.py
        |--routes.py

The init.py file is usually empty since it is just there so that we can reference the 
module from other files. The forms.py file contains the WTForms classes that are used for
that specific component's forms if there is any. The routes.py is going to be where you 
create your blueprint object and then create routes which link your html pages to that 
certain route. Depending on the type of request, the functionality is handled in any of the 
route functions in routes.py.

Modifying the Schema to the Database
------------------------------------

If you need to change the schema of the database, you will need to modify the models.py file 
in web/goalkeeper/models. We use Python's SQLAlchemy to help generate tables and do 
queries in the functions. If you need a refresher on what SQLAlchemy is and what it does, 
then the following link can help: https://www.sqlalchemy.org/

Creating New Components
-----------------------

To create new component of the application, we need to create the 3 files mentioned above, and 
then we typically have to put the following code at the top of the routes.py file::

    <blueprint_name> = Blueprint("<blueprint_name>", __name__, url_prefix="/<blueprint_name>")
    
Every time you want to create a new blueprint, you will need to add it to the init.py file of Develop. 
You will need to add::

     app.register_blueprint(<blueprint_name>)

From there on, the blueprint is set up already. Now you can add your own routes in the routes.py
file like the sample below::

    @<blueprint_name>.route('/home', methods=['GET'])
    def <function_name>():
        --Code goes here--

The routes connect the code to the templates which is in the section below. 

Creating New Templates
----------------------

The templates are what the browser will display. Our code uses jinja2 to render templates. 
All of the templates will go in the folder web/goalkeeper/templates. Most of the templates
extend the base.html which contains the navigation bar and other javascript libraries. 
If your component wants to have the navbar at the top, then you can follow the format 
below::

    {% extends "base.html" %}
    {% block content %}
        --HTML Code goes here (whatever you want your page to look like)--
    {% endblock %}

Whatever you want your page to look like, you need to put it in the 'block content tag'.
If you do not want the navbar, then you can create an entirely new page with basic HTML. 

Adding Forms to Template
------------------------

If you need to add a form to a template, you can put the code in the forms.py file within your
component folder. The project uses the wtforms module from python. You can check out more 
about the module here: https://wtforms.readthedocs.io/en/stable/ . If you want to put a form 
on a template, the following code could be base code::

    <form action="{{ <form route> }}" method="post">
        <div class="form-group">
            <label for="formGroupExampleInput">Form Label:</label>
            {{ Form Label Input }}
            <div class="form-group row mt-3">
                <div class="col-sm-10">
                  <button type="submit" class="btn btn-primary">Submit Button</button>
                </div>
            </div>
            {{ form.csrf_token }}
        </div>
    </form>

Adding to NavBar
----------------

If you need to add something to the navbar, you will need to go to the file /web/goalkeeper/templates/base.html.
and add the following code under the nav tag::

    <li class="nav-item">
        <a class="nav-link" href="{{ url_for('<Route to what it will display>') }}">NavBar element name!</a>
    </li>
    
Hypothetical Extension
======================

Our application is a very basic goal tracker with some social aspects to it. One extension of the application 
could be adding more newsfeed features where it could display some articles about goal tracking and topics that 
suit the user. 

Another extension of our project could be creating a chat service on the platfrom. Users could be able to 
find their friends and other users on the platform and start chatting them. 

We could also expand on the calendar to include more frontend functionality to serve as a
visual reminder of goals that users have created and completed. It'd be nice to
have a more reactive and dynamic UI for the calendar and the notifications. 