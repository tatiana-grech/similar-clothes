import requests
import json

with open('./data/vectors.json') as jsonFile:
    vectors = json.load(jsonFile)
    jsonFile.close()
    
collection_obj = {
    "create_collection": {
        "name": "clothes_collection",
        "distance": "Cosine",
        "vector_size": 768
    }
}
x = requests.post('http://localhost:6333/collections', json = collection_obj)

img_ids = list(vectors.keys())
for i in range(0,len(vectors)):
    point_obj = {
            "upsert_points": {
                "points": [
                    {
                        "id": i,
                        "payload": {},
                        "vector": vectors[img_ids[i]]
                    }
                ]
            }
        }
    x = requests.post('http://localhost:6333/collections/clothes_collection', json = point_obj)