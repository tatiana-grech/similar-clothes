import uvicorn
from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.post("/{img_index}")
def get_neighbours(img_index: int):
    img_response = requests.get('http://host.docker.internal:6333/collections/clothes_collection/points/'+str(img_index))
    search_obj = {
        "filter": {
        },
        "params": {
            "hnsw_ef": 128
        },
        "vector": img_response.json()['result']['vector'],
        "top": 4
    }
    search_response = requests.post('http://host.docker.internal:6333/collections/clothes_collection/points/search', json=search_obj)
    neighbours = []
    for item in search_response.json()['result']:
        if (len(neighbours) < 3) & (item['id'] != img_index):
            neighbours.append(item['id'])
    return {"neighbours": neighbours}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
