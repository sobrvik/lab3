from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Головна сторінка
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Сторінка для додавання користувача
@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        new_user = User(name=name, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
            return 'There was an issue adding the user'

@app.before_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

