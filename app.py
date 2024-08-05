from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_booking.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)

class BookingForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(min=2, max=150)])
    room_id = IntegerField('Room ID', validators=[DataRequired()])
    check_in_date = DateField('Check-in Date', validators=[DataRequired()])
    check_out_date = DateField('Check-out Date', validators=[DataRequired()])
    submit = SubmitField('Book Room')

db.create_all()

@app.route('/')
def home():
    rooms = Room.query.all()
    return render_template('index.html', rooms=rooms)

@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    form = BookingForm()
    if form.validate_on_submit():
        new_booking = Booking(
            customer_name=form.customer_name.data,
            room_id=form.room_id.data,
            check_in_date=form.check_in_date.data,
            check_out_date=form.check_out_date.data
        )
        room = Room.query.get(form.room_id.data)
        if room and room.status == 'available':
            room.status = 'booked'
            db.session.add(new_booking)
            db.session.commit()
            flash('Room booked successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Room is not available.', 'danger')
    return render_template('book_room.html', form=form)

@app.route('/bookings')
def bookings():
    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)
