from interactive_maps import make_vaccination_map, make_income_map, make_party_map
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, render_template_string, request
from flask_cors import CORS

import pymysql.cursors

app = Flask(__name__)
CORS(app)

db = pymysql.connect(host='stats-db.cc4nxcpkcpin.us-west-1.rds.amazonaws.com',
                     user='admin',
                     password='Nezzy559',
                     database='stats_db',
                     cursorclass=pymysql.cursors.DictCursor)

# Swagger UI
app.register_blueprint(get_swaggerui_blueprint(
    "",
    '/static/swagger.json',
    config={'app_name': "Stats Final REST API"},
))


@app.route("/swagger")
def getSwaggerJson():
    try:
        json = open('static/swagger.json', 'r').read()
        return render_template_string(json)
    except:
        return {}


@app.route("/api")
def getParameterOrAllCounties():
    try:
        fips_code = request.args.get('fips_code')
        state = request.args.get('state')
        county = request.args.get('county')
        if fips_code:
            return getCountyUsingFipsCode(fips_code)
        elif state and county:
            return getCountyUsingStateCounty(state, county)
        elif state:
            return getAllStateCounties(state)
        else:
            return getAllCounties()
    except:
        return {}


@app.route('/api/<state>')
def getAllStateCounties(state):
    try:
        sql = """
        SELECT
            e.State,
            p.County,
            e.FIPS_Code,
            e.Income,
            e.Population,
            v.Fully_Vaccinated,
            v.Boosters,
            p.Winner,
            p.Total_Votes,
            ROUND((GREATEST(p.Democrat, p.Republican, p.Other) / p.Total_Votes) * 100, 1) AS Winner_Percentage
        FROM
            economics e
            INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
            INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code
        WHERE
            p.State = %s
        ORDER BY p.County;
        """
        result = {}
        state = state.lower()
        with db.cursor() as cursor:
            cursor.execute(sql, (state))
            result = cursor.fetchall()
        return result
    except:
        return {}


@app.route('/api/<state>/<county>')
def getCountyUsingStateCounty(state, county):
    try:
        sql = """
        SELECT
            e.State,
            p.County,
            e.FIPS_Code,
            e.Income,
            e.Population,
            v.Fully_Vaccinated,
            v.Boosters,
            p.Winner,
            p.Total_Votes,
            ROUND((GREATEST(p.Democrat, p.Republican, p.Other) / p.Total_Votes) * 100, 1) AS Winner_Percentage
        FROM
            economics e
            INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
            INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code
        WHERE
            p.State = %s
            AND p.County = %s;
        """
        result = {}
        state = state.lower()
        county = county.lower()
        if "county" not in county and "parish" not in county:
            county = county + " parish" if state == "louisiana" else county + " county"
        with db.cursor() as cursor:
            cursor.execute(sql, (state, county))
            result = cursor.fetchall()
        return result
    except:
        return {}


@app.route("/map/income")
def getIncomeMap():
    try:
        map = make_income_map()
        return render_template_string(
            """{{ iframe|safe }}""",
            iframe=map.get_root()._repr_html_(),
        )
    except:
        return {}


@app.route("/map/vaccination")
def getVaccinationMap():
    try:
        map = make_vaccination_map()
        return render_template_string(
            """
            {{ iframe|safe }}
            """,
            iframe=map.get_root()._repr_html_(),
        )
    except:
        return {}


@app.route("/map/party")
def getPartyMap():
    try:
        map = make_party_map()
        return render_template_string(
            """
            {{ iframe|safe }}
            """,
            iframe=map.get_root()._repr_html_(),
        )
    except:
        return {}


def getAllCounties():
    try:
        sql = """
        SELECT
            e.State,
            p.County,
            e.FIPS_Code,
            e.Income,
            e.Population,
            v.Fully_Vaccinated,
            v.Boosters,
            p.Winner,
            p.Total_Votes,
            ROUND((GREATEST(p.Democrat, p.Republican, p.Other) / p.Total_Votes) * 100, 1) AS Winner_Percentage
        FROM
            economics e
            INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
            INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code
        ORDER BY e.State, e.County;
        """
        result = {}
        with db.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    except:
        return {}


def getCountyUsingFipsCode(fips_code):
    try:
        sql = """
        SELECT
            e.State,
            p.County,
            e.FIPS_Code,
            e.Income,
            e.Population,
            v.Fully_Vaccinated,
            v.Boosters,
            p.Winner,
            p.Total_Votes,
            ROUND((GREATEST(p.Democrat, p.Republican, p.Other) / p.Total_Votes) * 100, 1) AS Winner_Percentage
        FROM
            economics e
            INNER JOIN politics p ON e.FIPS_Code = p.FIPS_Code
            INNER JOIN vaccines v ON e.FIPS_Code = v.FIPS_Code
        WHERE
            e.FIPS_Code = %s;
        """
        result = {}
        with db.cursor() as cursor:
            cursor.execute(sql, (fips_code))
            result = cursor.fetchall()
        return result
    except:
        return {}
