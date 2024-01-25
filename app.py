from flask import Flask, request, json
import mysql.connector
from datetime import datetime

import datetime
app = Flask(__name__)


db_config = {
    'user': 'Saurav',
    'password': 'Gaurav@2001',
    'host': '127.0.0.1',
    'database': 'blacklight',
    'raise_on_warnings': True
}

def fetch_data_from_db():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM leaderboard"  # Replace 'leaderboard' with your actual table name if different
    cursor.execute(query)

    data = cursor.fetchall()
	 # Convert datetime objects to strings
    for entry in data:
        entry['timestamp'] = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

    cursor.close()
    connection.close()

    return data



# Fetching all data from the database
allData = fetch_data_from_db()
@app.route('/')
def hello_world():
    return """
    <h1>Welcome to the Flask API Server</h1>
    <p>To use this server, please use the following API endpoints:</p>
    <ul>
        <li><b>Find User Score:</b> Use the endpoint <code>/user-rank/&lt;uid&gt;</code>. Replace &lt;uid&gt; with the user's ID.<br>Example http://127.0.0.1:5000/user-rank/5370D18E</br></li>
        <li><b>Current Week Leaderboard:</b> Access the top 200 users of the current week at <code>/current-week-leaderboard</code>.<br>Example http://127.0.0.1:5000/current-week-leaderboard</br></li>
        <li><b>Last Week Leaderboard:</b> For the top 200 users from the last week for a specific country, use <code>/last-week-leaderboard/&lt;country&gt;</code>. Replace &lt;country&gt; with the desired country code.<br>Example http://127.0.0.1:5000/last-week-leaderboard/IN</br> </li>
    </ul>
    """



@app.route('/user-rank/<uid>')
def user_rank(uid):
	for entry in allData:
		if entry['uid'] == uid:
			return str(entry['score'])
	return 'User not found'


def getCurrentWeek(userdata):
	timestamp=datetime.datetime.strptime(userdata['timestamp'], '%Y-%m-%d %H:%M:%S')
	currDate=datetime.datetime.now()
	diff = (currDate-timestamp).days
	return diff <= 7

@app.route('/current-week-leaderboard')
def current_week_leaderboard():

	currentWeekEntries=list(filter(getCurrentWeek, allData))

	sortByScore=sorted(currentWeekEntries, key=lambda k: k['score'], reverse=True)

	topTwoHundreds = sortByScore[:200]
	return json.dumps(topTwoHundreds, indent=4)


def getLastWeek(userdata):
	timestamp=datetime.datetime.strptime(userdata['timestamp'], '%Y-%m-%d %H:%M:%S')
	currDate=datetime.datetime.now()
	diff = (currDate-timestamp).days
	return diff > 7 and diff <= 14

@app.route('/last-week-leaderboard/<country>')
def last_week_leaderboard(country):

	currentWeekEntries=list(filter(getLastWeek, allData))

	countryData=list(filter(lambda k: k['country']==country, currentWeekEntries))

	sortByScore=sorted(countryData, key=lambda k: k['score'], reverse=True)

	topTwoHundreds = sortByScore[:200]
	return json.dumps(topTwoHundreds, indent=4)

if __name__ == '__main__':
	app.run()


