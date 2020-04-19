# importing required modules
from flask import Flask, render_template, request
from model import Model
import random
from db import Db

# creating flask app
app = Flask(__name__)

# creating model object
m = Model()

# sentiment emoji list
happy = ['\U0001F603', '\U0001F607', '\U0001F60D', '\U0001F929', '\U0001F60E']
neutral = ['\U0001F62C', '\U0001F644', '\U0001F610', '\U0001F642', '\U0001F643', '\U0001F971']
negative = ['\U0001F910', '\U0001F928', '\U0001F614', '\U0001F97A']


# home page
@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template('index.html')


# result page
@app.route("/result", methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # data from front end
        feedback = request.form['review']
        domain = request.form['domain']

        m.input(feedback, domain)  # input to model

        feedback_sentiment = m.overall_polarity()  # result of the feedback entered by the user
        feedback_output = m.output()  # sentence_token wise result

        # database object
        db = Db(feedback, domain, feedback_sentiment)
        db.Insert()

        previous_list = db.Display()

        overall_pos = 0
        overall_neu = 0
        overall_neg = 0
        for review in previous_list:
            polarity = review['Polarity']
            overall_neg += polarity['neg']
            overall_neu += polarity['neu']
            overall_pos += polarity['pos']

        overall_neg /= len(previous_list)
        overall_neu /= len(previous_list)
        overall_pos /= len(previous_list)


        db.Insert()

        # generating emoji
        if feedback_sentiment['pos'] and feedback_sentiment['neg']:
            emoji = random.choice(neutral)
        elif feedback_sentiment['pos']:
            emoji = random.choice(happy)
        elif feedback_sentiment['neg']:
            emoji = random.choice(negative)
        else:
            emoji = random.choice(neutral)

    return render_template(
        'output.html',
        overall_result=feedback_sentiment,
        result=feedback_output,
        feedback=feedback,
        emoji=emoji,
        text_pos=feedback_sentiment['pos'],
        text_neu=feedback_sentiment['neu'],
        text_neg=feedback_sentiment['neg'],
        # aspect_current=[[('camera', 'photo'), 100, 200, 300], [('battery', 'charge'), 100, 200, 300]]
        overall_neg=overall_neg,
        overall_neu=overall_neu,
        overall_pos=overall_pos
    )


app.run(debug=True)  # running flask app
