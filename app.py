from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fromsoftData.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weapons = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    playstyle = db.Column(db.String(100), nullable=False)
    # created_at = db.Column(db.Datetime, default=datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        movie1=request.form.get('form1FirstInput')
        movie2=request.form.get('form1SecondInput')
        movie3=request.form.get('form1ThirdInput','test')

        return render_template('success/page1Success.html',fmovie1=movie1,fmovie2=movie2,fmovie3=movie3)
    return render_template('page1.html')
    

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        game = request.form.get('game', '').strip()
        year = request.form.get('release', '').strip()
        star1 = request.form.get('rating1star', '').strip()
        star2 = request.form.get('rating2star', '').strip()
        star3 = request.form.get('rating3star', '').strip()
        star4 = request.form.get('rating4star', '').strip()
        star5 = request.form.get('rating5star', '').strip()
        fstar = 0
        if(star5):
            fstar = 5
        elif(star4):
            fstar = 4
        elif(star3):
            fstar = 3
        elif(star2):
            fstar = 2
        elif(star1):
            fstar = 1
        else:
            fstar = 0
        return render_template('success/page2Success.html', gameName=game, gameYear=year, stars=fstar)
    return render_template('page2.html')

@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        weapon = request.form.get('weapon', '').strip()
        amount = request.form.getlist('fromAmount')
        number = len(amount)
        playstyle = request.form.get('playstyle','').strip()

        try:
            new_profile = Profile(
                name = name,
                weapons = weapon,
                amount = str(amount),
                number = number,
                playstyle = playstyle
            )
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "You done messed up."
            return render_template('page3.html', error=error)
        


        return render_template('success/page3Success.html',name=name, weapon=weapon, fromAmount=amount, fromNumber=number, playstyle=playstyle)
    return render_template('page3.html')

@app.route('/admin/data')
def admin_data():
    profiles = Profile.query.all()
    return render_template('admin_data.html', profiles=profiles)