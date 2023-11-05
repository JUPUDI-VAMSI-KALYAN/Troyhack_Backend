from fastapi import APIRouter
from schemas.suicide_schema import suicide_queriesEntity
from pydantic import BaseModel
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import neattext.functions as nfx
from tqdm import tqdm



model = pickle.load(open("./disease/suicide_pickle.pickle",mode='rb'))
tokenizer = pickle.load(open("./disease/suicide_tokenizer.pickle",mode='rb'))


suicide_query_router  = APIRouter(
    prefix="/mental-health",
    tags=['Mental Health']
)   


class SuicideQuery(BaseModel):
    user_text : str 


def clean_text(text):
    text_length=[]
    cleaned_text=[]
    for sent in tqdm(text):
        sent=sent.lower()
        sent=nfx.remove_special_characters(sent)
        sent=nfx.remove_stopwords(sent)
        text_length.append(len(sent.split()))
        cleaned_text.append(sent)
    return cleaned_text,text_length


#test_preprocessing
def pre_processor(text):
    text = clean_text([text])[0]
    print(text)
    text_seq=tokenizer.texts_to_sequences(text)
    print(text_seq)
    text_pad=pad_sequences(text_seq,maxlen=40)
    print(text_pad)
    predict = model.predict(text_pad)
    print(predict)
    return predict


@suicide_query_router.post("/suicide_query")
async def recommended_queries(user_text : SuicideQuery):
    print(user_text)
    pred = pre_processor(str(user_text))
    print(pred[0][0])
    if pred>0.5:
        return {"message": "Suicide","prob":str(pred[0][0])}
    else:
        return {"message" : "Non Suicide","prob":str(pred[0][0])}
    

########################### Parkinsons Disease #############################