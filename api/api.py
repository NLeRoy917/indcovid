'''
Copyright (c) 2020 indcovid.com
@author: Nathan LeRoy
@contact: NLeRoy917@gmail.com

indcovid.com main api to interface the MySQL database and the UI
'''

import sys
import os
import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
sys.path.append('../')

from dotenv import load_dotenv
load_dotenv()

MYSQL_URL = os.environ['MYSQL_URL']
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASS = os.environ['MYSQL_PASS']

# import custom classes
try:
    from ..lib.mysqlclient import MySQL
    from ..lib.datafetcher import DataFetcher
except:
    from lib.mysqlclient import MySQL
    from lib.datafetcher import DataFetcher


# import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def fetch_latest_data():
    dir = './tmp/'
    print('Fetching latest data into {} ... '.format(dir), flush=True)
    fetcher = DataFetcher.DataFetcher()
    fetcher.get_latest_data()

# background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_latest_data, trigger="interval", seconds=21600)
scheduler.start()

# Testing route/main route
@app.route('/')
def api_base():
    return_package={
        'message': "indcovid public api",
        'contact': 'nleroy917@gmail.com',
        'version': 1
    }
    return jsonify(return_package)

@app.route('/data/isdh/full', methods=['GET'])
def get_isdh_dull():
    res = requests.get('https://www.coronavirus.in.gov/map/covid-19-indiana-universal-report-current-public.json')
    return res.json()


@app.route('/data/indiana/county-hospitals', methods=['GET'])
def get_county_hospitals():
    """
    Get county hospital inpatient v outpatient statistics
    """
    mysql = MySQL.MySQL(MYSQL_URL, MYSQL_USER, MYSQL_PASS)
    data = mysql.get_county_hospitals()
    return_package = {
        'data': data
    }
    del mysql
    return jsonify(return_package)

@app.route('/data/indiana/education-geographic', methods=['GET'])
def get_education_geographic():
    """
    Get education statistics by geographic region in Indiana
    """
    mysql = MySQL.MySQL(MYSQL_URL, MYSQL_USER, MYSQL_PASS)
    data = mysql.get_education_geographic()
    return_package = {
        'data': data
    }
    del mysql
    return jsonify(return_package)

@app.route('/data/indiana/expenditure', methods=['GET'])
def get_expenditure():
    """
    Get all expenditure data - WARNING! THIS IS VERY NON PERFORMANT RIGHT NOW!
    """
    mysql = MySQL.MySQL(MYSQL_URL, MYSQL_USER, MYSQL_PASS)
    data = mysql.get_expenditure()
    return_package = {
        'data': data
    }
    del mysql
    return jsonify(return_package)

@app.route('/data/indiana/demographics', methods=['GET'])
def get_demographics():
    """
    Get the most recent demographic data for Indiana
    """
    mysql = MySQL.MySQL(MYSQL_URL, MYSQL_USER, MYSQL_PASS)
    data_raw = mysql.get_demographics()
    demographics_race = []
    demographics_ethnicities = []
    ethnicities = ['Hispanic', 'Not Hispanic or Latino']

    for row in data_raw:
        if row[0] not in ethnicities:
            demographics_race.append({
                'Race': row[0],
                'Percent': row[1],
                'Count': row[2],
                'ID': row[3]
            })
        else:
            demographics_ethnicities.append(
                {
                'Ethnicity': row[0],
                'Percent': row[1],
                'Count': row[2],
                'ID': row[3]  
                }
            )

    demographics_race_sorted = sorted(demographics_race, key=lambda k: k['Race']) 
    race_percentages = [obj['Percent'] for obj in demographics_race_sorted]
    race_labels = [obj['Race'] for obj in demographics_race_sorted]

    demographics_ethnicities_sorted = sorted(demographics_ethnicities, key=lambda k: k['Ethnicity']) 
    ethnicities_percentages = [obj['Percent'] for obj in demographics_ethnicities_sorted]
    ethnicities_labels = [obj['Ethnicity'] for obj in demographics_ethnicities_sorted]

    return_package = {
        'race_data': demographics_race,
        'race_percentages': race_percentages,
        'race_labels': race_labels,
        'ethnicity_data': demographics_ethnicities,
        'ethnicity_percentages': ethnicities_percentages,
        'ethnicity_labels': ethnicities_labels
    }
    del mysql
    return jsonify(return_package)

@app.route('/data/indiana/median-house-income', methods=['GET'])
def get_median_house_income():
    """
    Get the median household income statisistic for Indiana. It is organized by county and year.
    """
    mysql = MySQL.MySQL(MYSQL_URL, MYSQL_USER, MYSQL_PASS)
    data = mysql.get_median_income()
    return_package = {
        'data': data
    }
    del mysql
    return jsonify(return_package)

@app.route('/data/indiana/medicaid-funding-source', methods=['GET'])
def get_medicaid_funding_source():
    """
    Get the most common medicaid funding soruces for all medicaid claims
    """
    mysql = MySQL.MySQL(MYSQL_URL, MYSQL_USER, MYSQL_PASS)
    data = mysql.get_medicaid_funding()
    return_package = {
        'data': data
    }
    del mysql
    return jsonify(return_package)

@app.route('/data/indiana/medicaid-race', methods=['GET'])
def get_medicaid_demographics():
    """
    Get the medicaid demographics data
    """
    mysql = MySQL.MySQL(MYSQL_URL, MYSQL_USER, MYSQL_PASS)
    data = mysql.get_medicaid_race()
    return_package = {
        'data': data
    }
    del mysql
    return jsonify(return_package)

@app.route('/data/covid/demographics', methods=['GET'])
def get_case_demographics():
    """
    Get the covid-19 case demographics for Indiana
    """
    fetcher = DataFetcher.DataFetcher()
    demographics_race = fetcher.read_case_demographics_race()
    demographics_ethnicity = fetcher.read_case_demographics_ethnicity()
    race_labels = []
    ethnicity_labels = []

    for obj in demographics_race:
        # case to change "Black or African American to Black"
        if obj['Race'] == 'Black or African American':
            race_labels.append('Black')
        elif obj['Race'] == 'Unknown':
            race_labels.append('Unknown/Not Reported')
        elif obj['Race'] == 'Other Race':
            race_labels.append('Other/Mixed race')
        else:
            race_labels.append(obj['Race'])

    COVID_TEST_RACE = [obj['COVID_TEST'] for obj in demographics_race]
    COVID_COUNT_RACE = [obj['COVID_COUNT'] for obj in demographics_race]
    COVID_DEATHS_RACE = [obj['COVID_DEATHS'] for obj in demographics_race]
    COVID_TEST_PCT_RACE = [obj['COVID_TEST_PCT'] for obj in demographics_race]
    COVID_COUNT_PCT_RACE = [obj['COVID_COUNT_PCT'] for obj in demographics_race]
    COVID_DEATHS_PCT_RACE = [obj['COVID_DEATHS_PCT'] for obj in demographics_race]
    COVID_DEATH_RATE_RACE = [obj['COVID_DEATHS']/obj['COVID_COUNT']*100 for obj in demographics_race]

    ethnicity_labels = [
        'Hispanic or Latinx',
        'Non-Hispanic or Latinx',
        'Unknown/Not Reported'
    ]

    COVID_TEST_ETHNICITY = [obj['COVID_TEST'] for obj in demographics_ethnicity]
    COVID_COUNT_ETHNICITY = [obj['COVID_COUNT'] for obj in demographics_ethnicity]
    COVID_DEATHS_ETHNICITY = [obj['COVID_DEATHS'] for obj in demographics_ethnicity]
    COVID_TEST_PCT_ETHNICITY = [obj['COVID_TEST_PCT'] for obj in demographics_ethnicity]
    COVID_COUNT_PCT_ETHNICITY = [obj['COVID_COUNT_PCT'] for obj in demographics_ethnicity]
    COVID_DEATHS_PCT_ETHNICITY = [obj['COVID_DEATHS_PCT'] for obj in demographics_ethnicity]
    COVID_DEATH_RATE_ETHNICITY = [obj['COVID_DEATHS']/obj['COVID_COUNT']*100 for obj in demographics_ethnicity]


    return_package = {
        'race_data': demographics_race,
        'ethnicity_data': demographics_ethnicity,
        'COVID_TEST_RACE': COVID_TEST_RACE,
        'COVID_COUNT_RACE': COVID_COUNT_RACE,
        'COVID_DEATHS_RACE': COVID_DEATHS_RACE,
        'COVID_TEST_PCT_RACE': COVID_TEST_PCT_RACE,
        'COVID_COUNT_PCT_RACE': COVID_COUNT_PCT_RACE,
        'COVID_DEATHS_PCT_RACE': COVID_DEATHS_PCT_RACE,
        'COVID_DEATH_RATE_RACE': COVID_DEATH_RATE_RACE,
        'COVID_TEST_ETHNICITY': COVID_TEST_ETHNICITY,
        'COVID_COUNT_ETHNICITY': COVID_COUNT_ETHNICITY,
        'COVID_DEATHS_ETHNICITY': COVID_DEATHS_ETHNICITY,
        'COVID_TEST_PCT_ETHNICITY': COVID_TEST_PCT_ETHNICITY,
        'COVID_COUNT_PCT_ETHNICITY': COVID_COUNT_PCT_ETHNICITY,
        'COVID_DEATHS_PCT_ETHNICITY': COVID_DEATHS_PCT_ETHNICITY,
        'COVID_DEATH_RATE_ETHNICITY': COVID_DEATH_RATE_ETHNICITY,
        'race_labels': race_labels,
        'ethnicity_labels': ethnicity_labels
    }
    del fetcher
    return jsonify(return_package)

@app.route('/data/covid/cdc-demographics-cases', methods=['GET'])
def get_case_demographics_2():
    """
    """
    uri = 'https://data.cdc.gov/resource/k8wy-p9cg.json?fipsstate=18'
    res = requests.get(uri)
    data = res.json()
    return_package = {
        'data': data
    }
    return jsonify(return_package)

@app.route('/data/covid/cdc-demographics-death-deprecated', methods=['GET'])
def get_case_demographics_3():
    """
    """
    uri = 'https://data.cdc.gov/resource/ks3g-spdg.json?state=Indiana'
    res = requests.get(uri)
    data = res.json()
    races = [
        'White', 'Black', 'American Indian', 'Pacific Islander', 'Asian',  'More than one race', 'Unknown/Not Reported', 'Hispanic'
    ]
    ages = [
         "Under 1 year", "1-4 years", "5-14 years", "15-24 years", "25-34 years", "35-44 years", "45-54 years", "55-64 years", "65-74 years", "75-84 years", "85 years and over"
        ]
    White = []
    Black = []
    AmericanIndian = []
    Asian = []
    PacificIslander = []
    MoreThanOne = []
    Hispanic = []
    Unknown = []
    race_age_data = {
      "Under 1 year": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "1-4 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
    "5-14 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "15-24 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "25-34 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "35-44 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "45-54 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "55-64 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "65-74 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "75-84 years": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      },
      "85 years and over": {
          'Non-Hispanic White': 0,
          'Non-Hispanic Black': 0,
          'Non-Hispanic American Indian or Alaska Native': 0,
          'Non-Hispanic Native Hawaiian or Other Pacific Islander': 0,
          'Non-Hispanic Asian or Pacific Islander': 0,
          'Non-Hispanic More than one race': 0,
          'Hispanic': 0,
          'Unknown': 0
      }
    }
    # organize the data
    for obj in data:
        if 'total_deaths' in obj:
            if obj['age_group_new'] in race_age_data:
                race_age_data[obj['age_group_new']][obj['race_and_hispanic_origin']] += int(obj['total_deaths'])
            else:
                pass
        else:
            pass

    for age_group in race_age_data:
          White.append(race_age_data[age_group]['Non-Hispanic White'])
          Black.append(race_age_data[age_group]['Non-Hispanic Black'])
          AmericanIndian.append(race_age_data[age_group]['Non-Hispanic American Indian or Alaska Native'])
          Asian.append(race_age_data[age_group]['Non-Hispanic Asian or Pacific Islander'])
          PacificIslander.append(race_age_data[age_group]['Non-Hispanic Native Hawaiian or Other Pacific Islander'])
          MoreThanOne.append(race_age_data[age_group]['Non-Hispanic More than one race'])
          Hispanic.append(race_age_data[age_group]['Hispanic'])
          Unknown.append(race_age_data[age_group]['Unknown'])

    return_package = {
        'data_raw': data,
        'data_organized': race_age_data,
        'ages': ages,
        'race_age_data': {
            'White': White,
            'Black': Black,
            'AmericanIndian': AmericanIndian,
            'Asian': Asian,
            'PacificIslander': PacificIslander,
            'MoreThanOne': MoreThanOne,
            'Hispanic': Hispanic,
            'Unknown': Unknown
        }
    }
    return jsonify(return_package)


@app.route('/data/covid/access-to-care', methods=['GET'])
def access_to_care():
    """
    Endpoint to get the health-care access data from the CDC. Data-URL: https://data.cdc.gov/resource/xb3p-q62w
    """
    uri = "https://data.cdc.gov/resource/xb3p-q62w.json?state=Indiana"
    res = requests.get(uri)
    data = res.json()
    weeks = []
    week_dates = []
    delayed = []
    did_not_get = []
    both = []
    for obj in data:
        if obj['time_period'] not in weeks:
            weeks.append(obj['time_period'])
        if obj["indicator"] == "Delayed Medical Care, Last 4 Weeks":
            delayed.append(obj['value'])
        elif obj["indicator"] == "Did Not Get Needed Care, Last 4 Weeks":
            did_not_get.append(obj['value'])
        elif obj["indicator"] == "Delayed or Did Not Get Care, Last 4 Weeks":
            both.append(obj['value'])

    return_package = {
        'data': data,
        'weeks': weeks,
        'delayed': delayed,
        'did_not_get': did_not_get,
        'both': both
    }
    return jsonify(return_package)

@app.route('/data/covid/mental-health', methods=['GET'])
def get_mental_health_data():
    """
    """
    uri = 'https://data.cdc.gov/resource/8pt5-q6wp.json?state=Indiana'
    res = requests.get(uri)
    data = res.json()
    
    weeks = []
    depression_values = []
    anxiety_values = []
    depression_anxiety_values = []

    for obj in data:
        if obj['time_period'] not in weeks:
            weeks.append(obj['time_period'])

        if obj['indicator'] == 'Symptoms of Depressive Disorder':
            depression_values.append(obj['value'])
        elif obj['indicator'] == 'Symptoms of Anxiety Disorder':
            anxiety_values.append(obj['value'])
        elif obj['indicator'] == 'Symptoms of Anxiety Disorder or Depressive Disorder':
            depression_anxiety_values.append(obj['value'])

    return_package = {
        'data': data,
        'weeks': weeks,
        'depression': depression_values,
        'anxiety': anxiety_values,
        'depression_anxiety': depression_anxiety_values
    }
    return jsonify(return_package)

@app.route('/data/covid/vaccines', methods=['GET'])
def vaccine_data():
    """
    Endpoint to get the curent data for vaccine distribution
    and rollout.
    """
    PFIZER_URL = 'https://data.cdc.gov/resource/saz5-9hgg.json?jurisdiction=Indiana'
    MODERNA_URL = 'https://data.cdc.gov/resource/b7pe-5nws.json?jurisdiction=Indiana'
    KEY_PHRASE = 'doses_allocated_week_'

    res_p = requests.get(PFIZER_URL).json()
    res_m = requests.get(MODERNA_URL).json()
    
    dates = []
    p_first_doses = []
    p_second_doses = []
    p_total_doses = []
    p_first_cumulative = 0
    p_second_cumulative = 0
    p_total_cumulative = 0
    m_first_doses = []
    m_second_doses = []
    m_total_doses = []
    m_first_cumulative = 0
    m_second_cumulative = 0
    m_total_cumulative = 0
    both_total_doses = []
    
    for row in res_p:
        dates.append(row['week_of_allocations'])
        p_first_doses.append(int(row['_1st_dose_allocations']))
        p_second_doses.append(int(row['_2nd_dose_allocations']))
        p_total_doses.append(int(row['_1st_dose_allocations']) + int(row['_2nd_dose_allocations']))
        p_first_cumulative += int(row['_1st_dose_allocations'])
        p_second_cumulative += int(row['_2nd_dose_allocations'])
        p_total_cumulative += int(row['_1st_dose_allocations']) + int(row['_2nd_dose_allocations'])
    
    for row in res_m:
        dates.append(row['week_of_allocations'])
        m_first_doses.append(int(row['_1st_dose_allocations']))
        m_second_doses.append(int(row['_2nd_dose_allocations']))
        m_total_doses.append(int(row['_1st_dose_allocations']) + int(row['_2nd_dose_allocations']))
        m_first_cumulative += int(row['_1st_dose_allocations'])
        m_second_cumulative += int(row['_2nd_dose_allocations'])
        m_total_cumulative += int(row['_1st_dose_allocations']) + int(row['_2nd_dose_allocations'])
    
    for p, m in zip(p_total_doses, m_total_doses):
        both_total_doses.append(p + m)
    
    return_package = {
        "dates": dates,
        "pfizer_first_doses": p_first_doses,
        "pfizer_second_doses": p_second_doses,
        "pfizer_total_doses": p_total_doses,
        "pfizer_first_cumulative": p_first_cumulative,
        "pfizer_second_cumulative": p_second_cumulative,
        "pfizer_total_cumulative": p_total_cumulative,
        "moderna_first_doses": m_first_doses,
        "moderna_second_doses": m_second_doses,
        "moderna_total_doses": m_total_doses,
        "moderna_first_cumulative": m_first_cumulative,
        "moderna_second_cumulative": m_second_cumulative,
        "m_total_cumulative": m_total_cumulative,
        "both_total_doses": both_total_doses,
        "first_doses_to_date": [
            p_first_cumulative,
            m_first_cumulative,
            p_first_cumulative + m_first_cumulative
        ],
        "second_doses_to_date": [
            p_second_cumulative,
            m_second_cumulative,
            p_second_cumulative + m_second_cumulative
            
        ]
    }
    
    return jsonify(return_package)
    

if __name__ =='__main__':
    app.run()

