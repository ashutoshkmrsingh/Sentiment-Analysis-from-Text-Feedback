# importing required modules
from flask import Flask, render_template, request
from model import Model
import random
from db import Db
import aspect_mobile as ap

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
        mobile = request.form['domain']

        m.input(feedback, mobile)  # input to model

        feedback_sentiment = m.overall_polarity()  # result of the feedback entered by the user
        feedback_output = m.output()  # sentence_token wise result

        # database object
        db = Db(feedback, mobile, feedback_sentiment)
        db.Insert(mobile)

        previous_list = db.Display(mobile) # return previous enetered data

        # detecting aspects
        aspects = ap.aspect_cal(feedback)

        # d = {}
        # for key, val in aspect.items():
        #     d[key[0]] = val

        # db.Insert_Aspect(d)


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


        # db.Delete()

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
        overall_pos=overall_pos,
        aspect_score = aspects,
        camera_pos=aspects[('camera', 'photography')][0] * 100,
        camera_neu=aspects[('camera', 'photography')][1] * 100,
        camera_neg=aspects[('camera', 'photography')][2] * 100,
        battery_pos=aspects['battery'][0] * 100,
        battery_neu=aspects['battery'][0] * 100,
        battery_neg=aspects['battery'][0] * 100,
        display_pos=aspects[('display', 'screen', 'picture', 'look', 'design', 'UI', 'touch')][0] * 100,
        display_neu=aspects[('display', 'screen', 'picture', 'look', 'design', 'UI', 'touch')][1] * 100,
        display_neg=aspects[('display', 'screen', 'picture', 'look', 'design', 'UI', 'touch')][2] * 100,
        charge_neg=aspects[('charge', 'charging', 'power', 'discharing')][0] * 100,
        charge_neu=aspects[('charge', 'charging', 'power', 'discharing')][1] * 100,
        charge_pos=aspects[('charge', 'charging', 'power', 'discharing')][2] * 100,
        sound_neg=aspects[('sound', 'speaker', 'mic', 'microphone', 'music', 'voice')][0] * 100,
        sound_neu=aspects[('sound', 'speaker', 'mic', 'microphone', 'music', 'voice')][1] * 100,
        sound_pos=aspects[('sound', 'speaker', 'mic', 'microphone', 'music', 'voice')][2] * 100,
        processor_neg=aspects[('processor', 'storage', 'performance', 'heating', 'hanging ')][0] * 100,
        processor_neu=aspects[('processor', 'storage', 'performance', 'heating', 'hanging ')][1] * 100,
        processor_pos=aspects[('processor', 'storage', 'performance', 'heating', 'hanging ')][2] * 100,
        price_neg=aspects[('money', 'budget', 'price')][0] * 100,
        price_neu=aspects[('money', 'budget', 'price')][1] * 100,
        price_pos=aspects[('money', 'budget', 'price')][2] * 100,
        security_neg=aspects[('unlocking', 'finger print', 'sensor', 'unlock')][0] * 100,
        security_neu=aspects[('unlocking', 'finger print', 'sensor', 'unlock')][1] * 100,
        security_pos=aspects[('unlocking', 'finger print', 'sensor', 'unlock')][2] * 100
    )


app.run(debug=True)  # running flask app
