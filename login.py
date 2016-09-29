from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def loginpage():
    return render_template('home.html')


@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    try:
        user = request.form['user']
        password = request.form['pass']
    except:
        return render_template('hax.html')
    if user == 'admin' and password == 'alpine':
        return render_template('success.html')
    else:
        return render_template('failure.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
