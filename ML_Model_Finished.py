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
  dicti={'Apple': 0, 'Banana': 1, 'Blackgram': 2, 'Chickpea': 3, 'Coconut': 4, 'Coffee': 5, 'Cotton': 6, 'Grapes': 7, 'Jute': 8, 'Kidneybeans': 9, 'Lentil': 10, 'Maize': 11, 'Mango': 12,
       'Mothbeans': 13, 'Mungbean': 14, 'Muskmelon': 15, 'Orange': 16, 'Papaya': 17, 'Pigeonpeas': 18, 'Pomegranate': 19, 'Rice': 20, 'Watermelon': 21}
  for key in dicti.keys():
    if dicti[key]==value:
      return key
  return "Error"

xtest=scaler.transform([[90,42,43,20.879,82,6.5,202.9355,1]])




