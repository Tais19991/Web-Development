from flask import Flask, render_template
import requests
import os
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import SubmitField, SelectField
from datetime import date, timedelta, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MARKET_APP_KEY')
app.config['MARKETSTACK_API_URL'] = os.environ.get('MARKETSTACK_URL')
app.config['MARKETSTACK_ACCESS_KEY'] = os.environ.get("MARKETSTACK_API_KEY")
bootstrap = Bootstrap5(app)

company_dict = {"APPLE Inc": "AAPL",
                "3M Company": "MMM",
                "MICROSOFT CORP": "MSFT",
                "Amazon.com Inc": "AMZN",
                "Tesla Inc": "TSLA"}


class ChooseDataForm(FlaskForm):
    company = SelectField("Choose company",
                          choices=[key for key, value in company_dict.items()],
                          option_widget=None,
                          validate_choice=True)
    period = SelectField("Choose period (days)",
                         choices=[7, 10, 20, 30],
                         option_widget=None,
                         validate_choice=True)
    submit = SubmitField("Find Market Data")


def get_market_data(symbols, date_from):
    """Helper function to retrieve and process market data from the API."""
    url = app.config['MARKETSTACK_API_URL']
    access_key = app.config['MARKETSTACK_ACCESS_KEY']

    querystring = {
        "access_key": access_key,
        "symbols": symbols,
        "date_from": date_from,
        "date_to": str(date.today())
    }

    try:
        response = requests.get(url, params=querystring)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json().get('data', [])

        if not data:
            return [], None  # Return empty data if nothing found

        chart_data = {
            'labels': [datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d') for item in data][
                      ::-1],
            'closing_prices': [item['close'] for item in data][::-1],
            'opening_prices': [item['open'] for item in data][::-1]
        }
        return data, chart_data

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return [], None


@app.route("/", methods=["GET", "POST"])
def home():
    form = ChooseDataForm()
    company = "APPLE Inc"
    symbols = "AAPL"
    date_from = date.today() - timedelta(days=7)

    if form.validate_on_submit():
        company = form.company.data
        symbols = company_dict[company]
        date_from = date.today() - timedelta(days=int(form.period.data))

    # Get the market data using the helper function
    data, chart_data = get_market_data(symbols, str(date_from))

    # Handle case where no data is returned
    if not data:
        return render_template("error.html", message="No data available", form=form)

    return render_template("index.html", all_data=data, chart_data=chart_data, form=form, company=company,
                           symbols=symbols)


if __name__ == '__main__':
    app.run(debug=True)
