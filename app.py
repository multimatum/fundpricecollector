import os
from flask import Flask, render_template, request, jsonify
#from firebase_admin import credentials, firestore, initialize_app
from firebase import firebase
# import json
from datetime import date
#from twilio.rest import Client

#import config
#client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN) 
#client = Client(ACCOUNT_SID, AUTH_TOKEN) 

app = Flask(__name__)
firebase = firebase.FirebaseApplication('https://fundpricescraperncb.firebaseio.com/') # copy this from Firebase >> Database >> link next to the chain icon

# cred = credentials.Certificate('height-collector-firebase-adminsdk-4mjmy-8b0f39331c.json')
# default_app = initialize_app(cred)
# db = firestore.client()
# todo_ref = db.collection('todos')

def send_message(): 
    result = firebase.get('/Data', name='') # name = '' gets all the data
    
    id_last = sorted(result.keys())[-1]
    date_last = result[id_last]['Date']
    price_last = result[id_last]['Price']

    id_last_2 = sorted(result.keys())[-2]
    date_last_2 = result[id_last_2]['Date']
    price_last_2 = result[id_last_2]['Price']

    change_pct = (float(price_last) - float(price_last_2)) / float(price_last_2)
    
    if change_pct >= 0:
        pct_sign = '+'
    else:
        pct_sign = ''

    message_1 = '南商中國源動力基金'
    message_2 = '{0} 價格: {1}'.format(date_last_2, price_last_2)
    message_3 = '{0} 價格: {1}'.format(date_last, price_last)
    message_4 = '變動: {0}{1:.2%}'.format(pct_sign, change_pct)
                                                              
    # message = client.messages.create( 
    #                             from_='whatsapp:+14155238886',  
    #                             body= message_body,      
    #                             to='whatsapp:+85262166578' 
    #                         ) 
    # message = client.messages.create( 
    #                             from_='whatsapp:+14155238886',  
    #                             body= message_body,      
    #                             to='whatsapp:+85294362320' 
    #                         ) 
    
    # print(message.sid)
    return [message_1, message_2, message_3, message_4]

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        date_string = date.today().strftime('%Y-%m-%d')
        price = request.form['price_name']
        data = {
            'Date': date_string,
            'Price': price
        }
        result = firebase.post('/Data', data) # fundpricescraperncb comes from Firebase >> Database >> top of the tree

        # SEND WHATSAPP MESSAGE
        message = send_message()
        
        return render_template('success.html', message_1=message[0], message_2=message[1], message_3=message[2], message_4=message[3])
    else:
       pass

# @app.route("/listdata")
# def listdata():
#     result = firebase.get('/height-collector/Data', name='') # name = '' gets all the data
#     # result = {
#     #     'Name': 'Testing'
#     # }
#     print(result)
#     result2 = 'hello'
#     return render_template('listdata.html', context=result)

# @app.route("/updatedata")
# def updatedata():
#     result = firebase.get('/height-collector/Data', name='')
#     id = str(sorted(result.keys())[0])
#     email = result[id]['Email']
#     height = 314
#     firebase.put('/height-collector/Data/' + id, 'Height', height)
#     return render_template('updatedata.html', email=email, height=height)

# @app.route("/deletedata")
# def deletedata():
#     result = firebase.get('/height-collector/Data', name='')
#     id = sorted(result.keys())[-1]
#     email = result[id]['Email']
#     firebase.delete('/height-collector/Data/', id)
#     return render_template('deletedata.html', email=email)

if __name__ == '__main__':
    app.debug = True
    app.run()