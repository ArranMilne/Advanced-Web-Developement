from flask import Flask
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

@app.route('/home')
def home():
    return "Home"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

