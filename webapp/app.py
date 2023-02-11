import datetime
import os
import csv
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

def save_mood_value(date, mood_value):
   with open('mood_scale.csv', 'a') as f:
      writer = csv.writer(f)
      writer.writerow([date, mood_value])

def get_mood_values():
   mood_values = []
   with open('mood_scale.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
         mood_values.append(int(row[1]))
   return mood_values

def get_mood_dates():
   mood_dates = []
   with open('mood_scale.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
         mood_dates.append(row[0])
   return mood_dates

def get_mood_timestamps():
   mood_timestamps = []
   with open('mood_scale.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
         mood_timestamps.append(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
   return mood_timestamps

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/mood_scale', methods=['POST'])
def mood_scale():
   mood_value = request.form['mood_value']
   date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   save_mood_value(date, mood_value)

   mood_values = get_mood_values()
   mood_timestamps = get_mood_timestamps()
   plt.clf()
   plt.plot(mood_timestamps, mood_values, color='blue')
   plt.title('Daily Mood Scale')
   plt.xlabel('Timestamp')
   plt.ylabel('Mood Value (1-10)')
   plt.xticks(rotation=45)
   plt.tight_layout()
   plt.savefig('static/mood_scale.png')
   os.remove('static/mood_scale.png')
   plt.savefig('static/mood_scale.png')

   return render_template('mood_scale.html')

if __name__ == '__main__':
   serve(app, host='0.0.0.0', port=5000)
