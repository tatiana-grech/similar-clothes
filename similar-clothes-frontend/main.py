import requests
import streamlit as st
from PIL import Image
import json

def get_img_ids():
    with open('/data/vectors.json') as jsonFile:
        vectors = json.load(jsonFile)
        jsonFile.close()
    return list(vectors.keys())

def get_list_of_images(images_indexes):
    images = []
    for img_index in images_indexes:
        img_id = st.session_state.img_ids[img_index]
        image = Image.open('/data/clothing-dataset/images/'+img_id+'.jpg')
        images.append(image)
    return images

if "counter" not in st.session_state:
    st.session_state.counter = 0
    st.session_state.img_ids = get_img_ids()

def increment():
    st.session_state.counter += 5

st.title("Get similar clothes")
st.button("Show other items", on_click=increment)
st.text('Select one item')
images = get_list_of_images(range(st.session_state.counter, st.session_state.counter+5))
img_indices = [x for x in range(st.session_state.counter+1, st.session_state.counter+6)]
pick_img = st.sidebar.radio("Which item do you like?", img_indices)
st.image(images,caption=img_indices, width=120)

if pick_img:
    img_index = pick_img-1
    st.text('Selected item')
    st.image(images[pick_img-1-st.session_state.counter], width=120)
    res = requests.post(f"http://backend:8080/{img_index}")
    neighbours_images = get_list_of_images(res.json()['neighbours'])
    st.text('Similar items')
    st.image(neighbours_images, width=120)
