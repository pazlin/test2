from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("comune-di-piacenza-nomi-iscritti-per-nascita.csv")

@app.get("/names")
def get_names(
    nome: Optional[str] = None,
    cittadinanza: Optional[str] = None,
    sesso: Optional[str] = None,
    anno_min: Optional[int] = None,
    anno_max: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc"
):
    data = df.copy()
    if nome:
        data = data[data['Nome'].str.contains(nome, case=False, na=False)]
    if cittadinanza:
        data = data[data['Cittadinanza'].str.lower() == cittadinanza.lower()]
    if sesso:
        data = data[data['Sesso'].str.lower() == sesso.lower()]
    if anno_min:
        data = data[data['Anno Nascita'] >= anno_min]
    if anno_max:
        data = data[data['Anno Nascita'] <= anno_max]
    if sort_by:
        data = data.sort_values(by=sort_by, ascending=(sort_order=="asc"))
    return data.to_dict(orient="records")

@app.get("/aggregate")
def aggregate(
    by: str = Query(..., description="Field to aggregate by, e.g. 'Nome', 'Cittadinanza', 'Sesso', 'Anno Nascita'"),
    cittadinanza: Optional[str] = None,
    sesso: Optional[str] = None,
    anno_min: Optional[int] = None,
    anno_max: Optional[int] = None
):
    data = df.copy()
    if cittadinanza:
        data = data[data['Cittadinanza'].str.lower() == cittadinanza.lower()]
    if sesso:
        data = data[data['Sesso'].str.lower() == sesso.lower()]
    if anno_min:
        data = data[data['Anno Nascita'] >= anno_min]
    if anno_max:
        data = data[data['Anno Nascita'] <= anno_max]
    agg = data.groupby(by)['Occorrenze'].sum().reset_index()
    agg = agg.sort_values(by='Occorrenze', ascending=False)
    return agg.to_dict(orient="records")
