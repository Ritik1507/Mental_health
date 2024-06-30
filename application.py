import string
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sklearn
import pickle
from nltk.corpus import stopwords
import keras
import re
from keras.utils import pad_sequences
import nltk
import logging

nltk.download('stopwords')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_tokenizer(filepath):
    try:
        with open(filepath, 'rb') as file:
            token_load = pickle.load(file)
        print("Token loaded successfully!")
        return token_load
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except OSError as e:
        print(f"Error loading token: {e}")  # Likely file system error
    except Exception as e:  # Catch other unexpected exceptions
        print(f"Unexpected error: {e}")
    return None

def load_model(filepath):
    try:
        model = keras.models.load_model(filepath)
        print("Model loaded successfully!")
        return model
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except OSError as e:
        print(f"Error loading model: {e}")  # Likely file system error
    except Exception as e:  # Catch other unexpected exceptions
        print(f"Unexpected error: {e}")
    return None


token_load= load_tokenizer('C:\\Users\\ritik\\OneDrive\\Documents\\projects\\Mental_health\\models\\tokenizer.pickle')
model = load_model("C:\\Users\\ritik\\OneDrive\\Documents\\projects\\Mental_health\\models\\model.h5")


stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words('english'))


class InputData(BaseModel):
    feature: str


@app.get('/')
def index():
    return {'message': 'Hello, World'}


@app.post("/predict")
def predict_banknote(text: InputData):
    print(text)
    text = text.feature.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    seq = token_load.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=300)
    pred = model.predict(padded)

    print("pred", pred)
    if pred < 0.5:
        print("Normal")
    else:
        print("Need expert attention")
    return {"prediction": pred.tolist()}


if __name__ == '_main_':
    uvicorn.run(app, host='127.0.0.1', port=8000)