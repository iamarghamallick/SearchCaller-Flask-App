from dotenv import dotenv_values
from flask import Flask, render_template, request
import asyncio
import os
from truecallerpy import search_phonenumber

config = dotenv_values(".env")

app = Flask(__name__)


def search_phone_number(ph_no, country_code):
    phone_number = ph_no
    country_code = country_code
    installation_id = os.getenv("INSTALLATION_ID")

    response = asyncio.run(search_phonenumber(phone_number, country_code, installation_id))
    # print(response)
    return response


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ph_no = str(request.form.get('ph'))
        data = search_phone_number(ph_no, "IN")

        try:
            name = data['data']['data'][0]['name']
        except:
            name = "Not Available"
        try:
            mobile = data['data']['data'][0]['phones'][0]['e164Format']
        except:
            mobile = "Not Available"
        try:
            national_format = data["data"]["data"][0]["phones"][0]["nationalFormat"]
        except:
            national_format = "Not Available"
        try:
            countryCode = data['data']['data'][0]['phones'][0]['countryCode']
        except:
            countryCode = "Not Available"
        try:
            carrier = data['data']['data'][0]['phones'][0]['carrier']
        except:
            carrier = "Not Available"
        try:
            city = data["data"]['data'][0]["addresses"][0]["city"]
        except:
            city = "Not Available"
        try:
            email = data["data"]["data"][0]["internetAddresses"][0]["id"]
        except:
            email = "Not Available"

        try:
            spam_score = data['data']['data'][0]['phones'][0]['spamScore']
            spam_type = data['data']['data'][0]['phones'][0]['spamType']
            status = "danger"
        except:
            spam_score = 0
            spam_type = ""
            status = "success"

        return render_template('search.html', name=name, mobile=mobile, national_format=national_format,
                               countryCode=countryCode, carrier=carrier,
                               city=city, email=email, status=status)

    return render_template('index.html')


@app.route('/search/<string:ph>')
def search_json(ph):
    return search_phone_number(ph, "IN")


if __name__ == "__main__":
    app.run()
