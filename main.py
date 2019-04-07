import os
import random
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import db, Donor, Donation

app = Flask(__name__)

def check_donor(donor_name):
    '''
    Checks to see if donor_name is an existing donor, if so, returns the donor object

    :param donor_name:
    :return:
    '''
    current_donors = Donor

    for donors in current_donors:
        if donor_name.lower() == donors.name.lower():
            return donors
    return

def generate_donor_list():
    donations = Donation.select()

    donor_list = ['ALL']
    for donation in donations:
        if donation.donor.name not in donor_list:
            donor_list.append(donation.donor.name)

    return donor_list

def add_donation(donor_name, donor_amount):
    current_donor = check_donor(donor_name)

    if current_donor:
        Donation(donor=current_donor, value=donor_amount).save()
    else:
        temp = Donor(name=donor_name)
        temp.save()
        Donation(donor=temp, value=donor_amount).save()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/', methods=['GET', 'POST'])
def all():
    donations = Donation.select()

    # generate a list to be populated into drop down list, allowing for filter by donors
    donor_list = generate_donor_list()

    # if POST, determine whether a Name or ALL was selected, and filter results
    if request.method == 'POST':
        if request.form['filter_by_donor'] != 'ALL':
            filtered_donors = []

            for donation in donations:
                if donation.donor.name == request.form['filter_by_donor']:
                    filtered_donors.append(donation)
        else:
            filtered_donors = donations

        return render_template('donations.jinja2', donations=filtered_donors, donor_list=donor_list)

    # return default view of all donations on GET
    elif request.method == 'GET':
        return render_template('donations.jinja2', donations=donations, donor_list=donor_list)

@app.route('/add_donation/', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        donor = request.form['name']
        amount = request.form['amount']

        # add_donation form was submitted, and both fields were populated.
        if donor and amount:
            # accepts a comma delimited listed for multiple donation input
            if "," in amount:
                for donation in amount.split(","):
                    add_donation(donor, amount)

            # single donation
            else:
                add_donation(donor, amount)

        return render_template('donations.jinja2', donations=Donation.select(), donor_list=generate_donor_list())
    else:
        return render_template('add_donation.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

