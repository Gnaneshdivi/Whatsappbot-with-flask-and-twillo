from itertools import count
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from twilio.rest import Client
app = Flask(__name__)
account_sid = 'AC9516b6b588fc138e043601bcad3ac65e'
auth_token = '87eb0762b98c9a86794eabc4dbee9d2a'
client = Client(account_sid, auth_token)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/login")
def login():
    return "got it "    

file= pd.read_excel(r'data.xlsx')

@app.route("/sms", methods=['POST'])
def sms_reply():
    resp = MessagingResponse()
    item=[]
    sp=[]
    mrp=[]

    msg= request.form.get('Body').lower()
    if(msg=='get all'):
        resp.message("Here is the file for complete Data : https://drive.google.com/file/d/1Qa3qG5EObt75h7ibMJB_kn4qw5gkaWby/view?usp=sharing")
        return str(resp)

    else:    

        for i in range(file.shape[0]):  
            if(all(ele in str(file.at[i,'Item Descriptionfor Printing']).lower().split() for ele in msg.split(' '))):
                item.append(file.at[i,'Item Descriptionfor Printing'])
                sp.append(file.at[i,'Std Pkg'])
                mrp.append(file.at[i,'MRP'])
    data = {'ITEM':  item,
        'STD PKG': sp,
        'MRP':mrp
        }
    if(item!=[]):  
        if(len(item)<50)  :
            df = pd.DataFrame (data, columns = ['ITEM','STD PKG','MRP'])
            resp.message("The Results For Your Search Along with Standard Packing and MRP") 
            resp.message(str(df))
        else:
            resp.message("PLease Specify the " +msg+" product, as the range of products are very broad")
    else:
        resp.message("Item Not Found PLease search again")     

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)