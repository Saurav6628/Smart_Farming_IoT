from flask import Flask,request,render_template,redirect,url_for, jsonify
from numpy import random

import gspread
from keras.models import load_model
import pickle
model=load_model("ML_Model")
scaler_filename = "scaler.sav"
scaler=pickle.load(open(scaler_filename, 'rb'))

def crop_model(values):
  val=scaler.transform([values])
  pred=model.predict([val])
  return getKey(pred.argmax())
  
# Creating a function to fetch key using the value
def getKey(value):
  dicti={'Apple': 0, 'Banana': 1, 'Blackgram': 2, 'Chickpea': 3, 'Coconut': 4, 'Coffee': 5, 'Cotton': 6, 'Grapes': 7, 'Jute': 8, 'Kidneybeans': 9, 'Lentil': 10, 'Maize': 11, 'Mango': 12,'Mothbeans': 13, 'Mungbean': 14, 'Muskmelon': 15, 'Orange': 16, 'Papaya': 17, 'Pigeonpeas': 18, 'Pomegranate': 19, 'Rice': 20, 'Watermelon': 21}
  for key in dicti.keys():
    if dicti[key]==value:
      return key
  return "Error"

se=gspread.service_account(filename='data-collection.json')
sh=se.open("DHT11_Monitoring")
wks=sh.worksheet('Sheet1')

def read_value(worksheet):
        values=worksheet.get_all_values()
        col=f"H"+str(len(values))
        print(col)
        worksheet.update(col,"Data Read")
        return values[-1][0:7]

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def login():
    name=''
    password=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        name=request.form.get('username')
        password=request.form.get('password')
        if name=="MajorProject" and password=="LavaJava":
            return redirect(url_for("dashboard"))
    return render_template("LogIn.html",name=name,password=password)

@app.route("/dashboard")
def dashboard():
    l=[]
    return render_template("Dashboard.html", data = l)


@app.route('/update_data')
def update_data():
    data=read_value(wks)
    n,p,k=random.randint(0,140),random.randint(5,145),random.randint(5,205)
    ph=random.randint(3,9)
    rainfall=random.randint(20,298)
    crop_yield= round(random.uniform(0.0001,100.0001),4)
    # print(data[0][0:2])
    month=int("03")
    if month<=10 and month>=4:
        season="Kharif"

        
        season_num=1
    else:
        season="Rabi"
        season_num=2
    lt=[n, p, k, ph, rainfall, season]
    newData=[float(i) for i in data[2:len(data)-1]]
    for i in lt:
        newData.append(i)
    xtest=[n,p,k,newData[0],newData[1],ph,rainfall,season_num]
    pred=crop_model(xtest)
    newData.append(pred)
    newData.append(int(data[6]))
    newData.append(crop_yield)
    print(newData)
    l = newData
    return jsonify(newData)

if __name__ == '__main__':
    app.run(debug=True)

app.run()





