from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, login_required
from models import db, User
from auth.auth import auth, bcrypt, login
import tensorflow as tf

app = Flask(__name__)
app.register_blueprint(auth, url_prefix="/auth")
db.init_app(app)
bcrypt.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#harus ada ini karena flask login pake session
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' #jika user belom login, kelempar ke view ini

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    data = [int(request.form.get('input'))]
    model = tf.keras.models.load_model('resources/model/first_model.h5')
    result = model.predict(data)
    return render_template('prediction.html', result = int(result[0][0]))

if __name__ == "__main__":
    app.run(debug=True)
