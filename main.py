import os
import random
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import db, Donor, Donation

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/', methods=['GET', 'POST'])
def all():
    donations = Donation.select()

    # generate a list to be populated into drop down list, allowing for filter by donors
    donor_list = ['ALL']
    for donation in donations:
        if donation.donor.name not in donor_list:
            donor_list.append(donation.donor.name)

    # if post, return a filtered view. if get, return default view.
    if request.method == 'POST':
        if request.form['filter_by_donor'] != 'ALL':
            filtered_donors = []

            for donation in donations:
                if donation.donor.name == request.form['filter_by_donor']:
                    filtered_donors.append(donation)
        else:
            filtered_donors = donations

        return render_template('donations.jinja2', donations=filtered_donors, donor_list=donor_list, select_value=request.form['filter_by_donor'])
    elif request.method == 'GET':
        return render_template('donations.jinja2', donations=donations, donor_list=donor_list)

@app.route('/add_donation/', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        donor = request.form['name']
        amount = request.form['amount']

        donations = Donation.select()

        for donation in donations:
            if donor in donation.donor.name:
                print('donor has already donated, this would break so im exiting')
                return

        temp = Donor(name=donor)
        temp.save()

        Donation(donor=temp, value=amount).save()

        return render_template('add_donation.jinja2')
    else:
        return render_template('add_donation.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

