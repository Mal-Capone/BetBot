# -----------IMPORTS----------#
import requests
from flask import Flask
from flask import render_template, request
from betbot import the_odds_api
import builder

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    html = render_template('index.html')
    return html

@app.route('/about')
def about():
    html = render_template('about.html')
    return html

@app.route('/results')
def results():
    o, r = builder.results_form()
    html = render_template('results.html', results='No Bets Checked', OUTCOMES=o, REGIONS=r)
    return html

@app.route('/get_results', methods=['GET', 'POST'])
def bets():
    data = request.form
    regions = str(data['ddRegions'])
    outcomes =  int(data['ddOutcomes'])
    response = the_odds_api.get_results(regions, outcomes)
    if builder.results(response):
        quota, used_req, this_cost = response['quota']
        total = int(quota) + int(used_req)
        o, r = builder.results_form(regions,outcomes)
        html = render_template("results.html", QUOTA=f'{quota} / {total}', COST=this_cost, REGIONS=r, OUTCOMES=o)
        return html

if __name__ == '__main__':
    try:
        app.run(debug=True,port=8080)
    except (KeyboardInterrupt, Exception) as e:
        print(f"Program Finished: {e}")
