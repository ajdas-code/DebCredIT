"""
############################3333
class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {'tasks': [marshal(task, task_fields) for task in tasks]}


#=====
request.cookies.get('username')  # get single cookie
request.cookies  # get all as dict

==============

# Generate Secret Key
#python -c 'import os; print(os.urandom(16))'

######
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "example.com"}})
======
CORS(app, origins="http://127.0.0.1:8080", allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)

# -----------------
"""
"""
You could pass the messages as explicit URL parameter (appropriately encoded), or store the messages into session (cookie) variable before redirecting and then get the variable before rendering the template
or
as query param to PUBLIC URL
/app/4903294/my-great-car?email=coolguy%40gmail.com to

/public/4903294/my-great-car?email=coolguy%40gmail.com
---->>>> return redirect(url_for('app.vehicle', vid=vid, year_make_model=year_make_model, **request.args))

"""
"""
def do_baz():
    messages = json.dumps({"main":"Condition failed on page baz"})
    session['messages'] = messages
    return redirect(url_for('.do_foo', messages=messages))

@app.route('/foo')
def do_foo():
    messages = request.args['messages']  # counterpart for url_for()
    messages = session['messages']       # counterpart for session
    return render_template("foo.html", messages=json.loads(messages))
    

####VCurry function
def change(b, c, d):
    def a(x):
        return b(c(d(x)))
    return a
# Currying in Python - Many to Single Argument
 def change(a):
    def w(b):
        def x(c):
            def y(d):
                def z(e):
                    print(a, b, c, d, e)
                return z
            return y
        return x
    return w
   
change(10)(20)(30)(40)(50)
"""