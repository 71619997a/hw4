from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def loginpage():
    return render_template('home.html')


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    try:
        user = request.form['user']
        password = request.form['pass']
        trickery = False
    except:
        user = 0
        password = 0
        trickery = True
    login_good = user == 'admin' and password == 'alpine'
    return render_template('auth-response.html', trickery=trickery, login_good=login_good)

if __name__ == '__main__':
    app.debug = True
    app.run()
