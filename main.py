import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation

app = Flask(__name__)
app.secret_key = b'\x1d\xa5\xb0`2\x83\x98G\xc3Aa\x17=\nHO\xbd$\xb92\n\xa7S\x03'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add_donation/', methods=['GET', 'POST'])
def add_donation():
    # donations = Donation.select()

    if request.method == 'POST':
        donor = request.form['name']
        amount = request.form['amount']
        
        print('logging: Received a post method from {} for {}'.format(
            donor,
            amount
        ))

        Donation(donor, amount).save()

        return all()
    else:
        return render_template('add_donation.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

