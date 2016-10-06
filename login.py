from flask import Flask, render_template, request, session, redirect, url_for
from hashlib import sha256
app = Flask(__name__)
app.secret_key = 'wigjhuv;osfdodsfogvsn b.  ZUiv  '

@app.route('/')
def loginpage():
    return render_template('home.html', logged='login' in session)


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    try:
        user = request.form['user']
        password = request.form['pass']
    except:
        return render_template(
            'auth-response.html', trickery=1, log=0, pw=0, new=0)
    hashuser = sha256(user).hexdigest()
    hashpass = sha256(password).hexdigest()
    logins = load_logins()
    if request.form['action'] == 'Login':
        badpass = True
        badlog = True
        try:
            real_pass = logins[hashuser]
            badlog = False
            badpass = real_pass != hashpass
        except KeyError:
            badlog = True
        return render_template(
            'auth-response.html', trickery=0, log=not badlog,
            pw=not badpass, new=0)
    elif request.form['action'] == 'Register':
        log = True
        if hashuser in logins:
            log = False
        else:
            register(hashuser, hashpass)
        return render_template(
            'auth-response.html', trickery=0, log=log,
            pw=True, new=1)
    else:
        return render_template(
            'auth-response.html', trickery=1, log=0, pw=0, new=0)


def load_logins():
    with open('data/passwords.csv', 'r') as f:
        lines = f.readlines()
    logins = [(i.strip() for i in line.split(',')) for line in lines]
    return dict(logins)


def register(u, p):
    with open('data/passwords.csv', 'a') as f:
        f.write(u + ',' + p + '\n')


if __name__ == '__main__':
    app.debug = True
    app.run()
