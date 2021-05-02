import base64
from PIL import Image
from io import BytesIO
from flask import session

from keebs.models import Keyboard

def to_img64(file, size):
    #Create image and resize to smaller size if over the threshold
    image = Image.open(file)
    if image.size[0] > size and image.size[1] > size:
        image.thumbnail((size, size), Image.ANTIALIAS)

    #Create memory buffer to store the image binary data
    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    #Convery bytes to base64
    img64 = base64.b64encode(buf.read())

    #Return bytes as base64 ascii
    return img64.decode("ascii")

def check_session(key, obj):
    #Make sure a key value pair exists in session for the passed key
    if key not in session:
        session[key] = obj

def update_cart(item, quantity):
    #Check if our cart key is in the session
    check_session("cart", {})

    #If exists, increment it, otherwise, assign it
    if str(item.id) in session["cart"]:
        session["cart"][str(item.id)] += 1
    else:
        session["cart"][str(item.id)] = quantity

    #Mark the session as modified so it updates for the user
    session.modified = True

def get_cart():
    check_session("cart", {})
    items = []
    for id in session["cart"]:
        items.append({"item": Keyboard.query.get_or_404(id), "quantity": session["cart"][id]})
    return items

def purge_cart():
    session["cart"] = {}
    session.modified = True