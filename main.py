from fastapi import FastAPI
from typing import Union
import warnings
warnings.filterwarnings('ignore')

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
from disease import suicide,diseases


app = FastAPI()
app.include_router(suicide.suicide_query_router)
app.include_router(diseases.parkinsons_query_router)

origins = [
    "https://querybox.wdc1a.ciocloud.nonprod.intranet.ibm.com",
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:4200/",
    "https://querybox.wdc1a.ciocloud.nonprod.intranet.ibm.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Yes")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item():
    return {"item_id": "item id"}
