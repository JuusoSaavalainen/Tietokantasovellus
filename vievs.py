from app import app
from flask import render_template, request, redirect
import accounts
import topics

@app.route("/")
def index():
    return render_template('index.html', titles=reversed(topics.get_all_topic_titles_desc()))

@app.route("/newtopic", methods=["get","post"])
def newtopic():
    if request.method == 'GET':
        return render_template('newtopic.html')

    if request.method == 'POST':
        accounts.check_csrf()
        
        topic_name = request.form['Topicname']
        if ' ' in topic_name[0]:
            return render_template('error.html', message='Name of the topic cant start with empty space')
        first_comm = request.form['comments']
        #virheen käsittely tähän
        topic_id = topics.add_topic(topic_name, first_comm, accounts.user_id()) 
        return redirect("/topic/"+str(topic_id))

@app.route("/logout")
def logout():
    accounts.logout()
    return render_template('succes.html', message='logged out!')

@app.route("/likess", methods=["get","post"])
def likes():
    if request.method == 'POST':
        accounts.check_csrf()
        liker_id = request.form['comm_id']
        t_id = request.form['topic_idr']
        tpc_id = request.form['topic_id']
        topics.add_likes(liker_id,t_id)
        return redirect("/topic/"+str(tpc_id))

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message='500')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='404')


@app.route("/topic/<int:topic_id>", methods=["get","post"])
def show_topic(topic_id):
    if request.method == 'GET':
        listlikes = []
        info = topics.get_topic_info(topic_id)
        all_comments = topics.get_topic_comments(topic_id)
        for i in all_comments:
            listlikes.append(topics.get_likes(i[2]))
        return render_template('topic.html', id=topic_id, title=info[0], creator=info[1], comments=all_comments, likes=listlikes)

    if request.method == 'POST':
        accounts.check_csrf()
        topic_id = request.form["topic_id"]
        #virhe käsittely tähän
        comm = request.form['comments']
        #virheen käsittely tähän
        topics.add_comment(comm, topic_id, accounts.user_id()) 
        return redirect("/topic/"+str(topic_id))


@app.route("/login", methods=["get","post"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        usern = request.form['Username'].lower()
        passw = request.form['Password']

        if not accounts.login(usern, passw):
            return render_template('error.html', message='Invalid credentials please try again')
        return render_template('succes.html', message='logged in!')

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        usern = request.form["username"].lower()
        passw1 = request.form["password1"]
        passw2 = request.form["password2"]
        if accounts.register(usern, passw1) == False:
            return render_template("error.html", message='Username was already taken')
        return render_template('succes.html', message='registered, i logged you in!')
