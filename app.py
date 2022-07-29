from flask import Flask,request, render_template
import pandas as pd
from flask_cors import cross_origin
import pickle
import bz2

app=Flask(__name__)

pickle_file=bz2.BZ2File('house_price.pkl','rb')
model=pickle.load(pickle_file)

@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def predict():
    if request.method == 'POST':
        posted_by=request.form['posted_by']
        if posted_by == 'Owner':
            Owner=1
            Dealer=0
            Builder=0
        elif posted_by =='Dealer':
            Dealer=1
            Owner=0
            Builder=0
        elif posted_by == 'Builder':
            Builder=1
            Owner=0
            Dealer=0
        under_construction=request.form['UNDER_CONSTRUCTION']
        rera=int(request.form['RERA'])
        bhk=int(request.form['BHK'])
        bhkrk=request.form['BHKRK']
        if bhkrk == 'BHK':
            BHK= 1
            RK= 0
        elif bhkrk =='RK':
            BHK=0
            RK=1
        square_ft=float(request.form['SQUARE_FT'])
        ready_to_move=request.form['READY_TO_MOVE']
        if ready_to_move == 'Yes':
            Yes= 1
            No= 0
        elif ready_to_move =='No':
            No=1
            Yes=0
        RESALE=request.form['RESALE']
        longitude=request.form['LONGITUDE']
        latitude=request.form['LATITUDE']
        prediction=model.predict([[
            under_construction,
            rera,
            bhk,
            square_ft,
            ready_to_move,
            RESALE,
            longitude,
            latitude,
            Dealer,
            Owner,
            Builder,
            BHK,
            RK
        ]])

        output=round(prediction[0],2)

        return render_template('index.html',prediction_price=output,longitude=longitude,latitude=latitude,posted_by=posted_by,under_construction=under_construction,
                               rera=rera,bhk=bhk,bhkrk=bhkrk,square_ft=square_ft,ready_to_move=ready_to_move,RESALE=RESALE)
    return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)
