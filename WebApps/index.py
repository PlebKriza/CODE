from flask import Flask, request, render_template #can use html but you have to call render_template
import os
import sqlite3 as sql

app = Flask(__name__) #Double "_"

template_folder = os.path.join(os.path.dirname(__file__),"templates/")
#               = a + b
#             a = os.path.dirname(os.path.dirname(__file__)
#             a = "D:\WEBAPP"
#             b = "template/"


#template_folder + "D:\WEBAPP + "template/"
# ...
app.static_folder = "static"
app.static_url_path = "/static"

#data base
database = os.path.join(os.path.dirname(__file__),"database/ibit.db")


#when you create a route you have to make a function (cannot use the same function)
@app.route('/', methods=["GET"]) #"/" index #GET user access from our web
def home():
    return render_template("index.html")

@app.route('/signin', methods=["GET"]) 
def signin():
    return render_template("sign-in.html")

@app.route('/post-signin',methods=["POST"])
def post_signin():
    username = request.form.get ("username")
    password = request.form.get ("password")

    conn = sql.connect(database)
    cur = conn.cursor() 
    sql_select = """
                SELECT email, password, fullname
                FROM username 
                WHERE email=?
                """ 
    # will give more arsenal to hackers if a lot of condition

    val = (username,)
    cur.execute(sql_select,val)
    data = cur.fetchone()
    conn.close()
    # print(data)

    if password == data[1]:
        return user()      #render_template('username.html', data=data)
    else:
        return signin()

@app.route('/user',methods=["GET"])
def user():
    conn = sql.connect(database)
    cur = conn.cursor() 
    sql_user = """
                SELECT email, password, fullname
                FROM username 
                """ 

    cur.execute(sql_user)
    data = cur.fetchall()
    conn.close()
    return render_template('username.html', user=data)

    # return "username = " + data[0] + " ,password = " + data[1]    # return "username =" + username + ", password = " + password

@app.route('/delete/<email>', methods=['GET'])
def delete(email):
    conn= sql.connect(database)
    cur = conn.cursor()
    sql_delete = """
    DELETE FROM username
    WHERE email=?
    """

    val = (email,)
    cur.execute(sql_delete, val)
    conn.commit()
    conn.close()
    return user()

@app.route('/signup', methods=["GET"]) 
def signup():
    return render_template("signup.html")
 #   return "Welcome to homepage, Kriza Claire (ㆆ_ㆆ)" 

@app.route('/post-signup', methods=["POST"])
def post_signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    psw_repeat = request.form.get("psw-repeat")

    conn = sql.connect(database)
    cur = conn.cursor() #cannot use sql without cursor
    sql_insert = """
    INSERT INTO username (fullname,email, password, authorize)
    VALUES(?,?,?,?)
    """ 
    #""" can include multiple lines"
    #order not important

    val = (username,email,password,1)
    cur.execute(sql_insert,val)
    conn.commit()
    conn.close()

    return username + ", " + email + ", " + password 

@app.route('/register', methods=["GET"])
def register():
    name = request.args['name']
    email = request.args['email']
    return "<h1>Your name is " + name + ", Your Email is " + email + "</hi>" 
#http://localhost:5000/register?name=Kriza&email=Kriza@gmail.com

@app.route('/cal', methods=["GET"])
def cal():
    item = request.args['item']
    number = int(request.args['number'])
    price = float(request.args['price'])
    msg = "You have to pay "
    msg += str(number*price)
    return "You buy <h1>" + item + "</h1>" + msg
#http://localhost:5000/cal?item=Adidas&number=2&price=25.5

@app.route('/edit/<email>', methods=["GET"])
def edit(email):
    conn = sql.connect(database)
    cur = conn.cursor() 
    sql_select = """
                SELECT fullname, email, password
                FROM username 
                WHERE email=?
                """ 
    val = (email,)
    cur.execute(sql_select, val)
    data = cur.fetchone()
    conn.close()
    return render_template('edit_user.html', user=data)

@app.route('/post-edit', methods=["POST"])
def post_edit():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    repassword = request.form.get('repassword')
    
    conn = sql.connect(database)
    cur = conn.cursor() 
    sql_update = """
                UPDATE USERNAME 
                SET FULLNAME=?
                WHERE EMAIL=?
            """

    val = (fullname, email)
    cur.execute(sql_update, val)
    conn.commit
    conn.close()
    return user()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
