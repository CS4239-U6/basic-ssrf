from flask import Flask, render_template

app = Flask(__name__)


class User:
    uid = 1

    def __init__(self, username, password, website):
        self.id = User.uid
        User.uid += 1
        self.username = username
        self.password = password
        self.website = website


users = [
    User('Junhua', 'i4mv3ryc00l', 'http://github.com/jh123x'),
    User('Hanming', 'i_push_10k_code_per_day', 'http://github.com/zhuhanming'),
    User('Kelvin', 'password1234', 'http://github.com/kelvinnharris'),
    User('Jaedon', 'password1234', 'http://github.com/jaedonkey'),
    User('Johanna', 'password1234', 'http://github.com/joannasara')
]


@app.route('/')
def index():
    return render_template('index.html', users=users)


if __name__ == '__main__':
    app.run(port=5001)
