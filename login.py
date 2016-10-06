from flask import Flask, render_template, request, session, redirect, url_for
from hashlib import sha256
app = Flask(__name__)
app.secret_key = '''
a random string of characgh897y0a89sdyhfnia08d9 0a9-s8df7 aa
as8f09sda8 09a9090a09a908  b  90as8 0 09  88 8  8 9sdaasdasd
asdfasdfasoasdojiasoi  o o  oi 98asd 89asd 4 3
44 92340 wer 8908 sd70sdf9 n70sdf89 7fgsd
 2907wer80 09nsd78ngsdf90sdf8079sndf87sdf0g98sd  n 0n9sd8uaiyqo d
  as9780a sn0as9d8nd 7asfters :)
'''

@app.route('/')
def loginpage():
    if 'login' in session:
        return render_template(
            'home.html', logged=True, login=session['login'])
    else:
        return render_template(
            'home.html', logged=False, login=0)


@app.route('/logout')
def logout():
    if 'login' in session:
        session.pop('login')
    return redirect(url_for('loginpage'))


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    try:
        user = request.form['user']
        password = request.form['pass']
    except:
        return loginpage() + \
            render_template('addon.html', trickery=1, log=0, pw=0, new=0)
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
        if not badlog and not badpass:
            session['login'] = user
        return loginpage() + render_template(
            'addon.html', trickery=0, log=not badlog,
            pw=not badpass, new=0)
    elif request.form['action'] == 'Register':
        log = True
        if hashuser in logins:
            log = False
        else:
            register(hashuser, hashpass)
            session['login'] = user
        return loginpage() + render_template(
            'addon.html', trickery=0, log=log,
            pw=True, new=1)
    else:
        return loginpage() + render_template(
            'addon.html', trickery=1, log=0, pw=0, new=0)


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
