import os
import random
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import db, Donor, Donation

app = Flask(__name__)
app.secret_key = b'\x1d\xa5\xb0`2\x83\x98G\xc3Aa\x17=\nHO\xbd$\xb92\n\xa7S\x03'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/', methods=['GET', 'POST'])
def all():
    print('running all')
    donations = Donation.select()

    donor_list = ['ALL']

    # generate a list for the donor filter
    for donation in donations:
        if donation.donor.name not in donor_list:
            donor_list.append(donation.donor.name)

    if request.method == 'POST':
        filtered_donors = []
        print("we got a filter request by:", request.form['filter_by_donor'])
        for donation in donations:
            if donation.donor.name == request.form['filter_by_donor']:
                filtered_donors.append(donation)

        # filtered_donors = [donor for donor in donations if donor.donation.name == request.form['filter_by_donor']]

        return render_template('donations.jinja2', donations=filtered_donors, donor_list=donor_list)
    else:
        return render_template('donations.jinja2', donations=donations, donor_list=donor_list)

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

        temp = Donor(name=donor)
        temp.save()

        Donation(donor=temp, value=amount).save()

        return render_template('donations.jinja2')
    else:
        return render_template('add_donation.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

