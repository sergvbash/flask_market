import os
from flask import Flask
from flask import redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, FloatField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db = SQLAlchemy(app)
SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x0f\t\xfdS\x9aH\x00\x89\x94\xd4\x07\x9a\xed\xd4\xe2\x1a'
app.config['SECRET_KEY'] = SECRET_KEY

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    instock = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Item %r>' %self.title

class ItemForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description')
    price = FloatField('Price')
    instock = IntegerField('In stock')
    submit = SubmitField('Add Item')


db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    items = Item.query.all()
    ch = 'off'
    if request.method == 'POST':
        ch = request.form.getlist('filteronstock')[0]
        print(ch)
        if ch == 'on':
            items = Item.query.filter(Item.instock>0).all()
    return render_template('index.html', items=items, ch=ch)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/additem', methods=['GET', 'POST'])
def additem():
    form = ItemForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            price = round(form.price.data, 2)
            instock = form.instock.data
            newitem = Item(title=title, description=description, price=price, instock=instock)
            try:
                db.session.add(newitem)
                db.session.commit()
                return redirect(url_for('index'))
            except:
                return 'Error with DB'
    return render_template('additem.html', form = form)

@app.route('/buy/<int:id>')
def buy(id):
    return id


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
