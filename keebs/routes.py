from keebs import app, SearchForm, db
from keebs.forms import KeyboardForm, AddCartForm
from keebs.helper import to_img64, update_cart, purge_cart, get_cart
from keebs.models import Keyboard
from flask import render_template, flash, request

def render(template, **kwargs):
    query = db.session.query(Keyboard.brand).distinct()
    brands = [b.brand for b in query.all()]

    search_form = SearchForm()
    if search_form.validate_on_submit():
        items = Keyboard.query.filter(Keyboard.name.contains(search_form.input.data)).all()
        return render_template("items.jinja", search_form=search_form, brands=brands, items=items)
    else:
        return render_template(template, search_form=search_form, brands=brands, **kwargs)

@app.route("/")
def index():
    return render("index.jinja")

@app.route("/about")
def about():
    purge_cart()
    return render("about.jinja")

@app.route("/gallery")
def gallery():
    return render("gallery.jinja", items=Keyboard.query.all())

@app.route("/inventory", methods=["GET", "POST"])
@app.route("/inventory/<brand>", methods=["GET", "POST"])
def inventory(brand=None):
    if brand:
        return render("items.jinja", items=Keyboard.query.filter_by(brand=brand).all())
    return render("items.jinja", items=Keyboard.query.all())

@app.route("/item/<int:item_id>", methods=["GET", "POST"])
def item(item_id):
    cart_form = AddCartForm()
    item = Keyboard.query.get_or_404(item_id)

    # If we are posting to this route and the cart form is valid, push item into the session cart
    if request.method == "POST" and cart_form.validate_on_submit():
        update_cart(item, cart_form.quantity.data)
    return render("item.jinja", item=item, cart_form=cart_form)

@app.route("/insert", methods=["GET", "POST"])
def insert():
    form = KeyboardForm()
    if form.validate_on_submit():
        img64_small = to_img64(request.files["image"], 200)
        img64_large = to_img64(request.files["image"], 600)
        kb = Keyboard(img_small=img64_small, img_large=img64_large)
        form.populate_obj(kb)
        db.session.add(kb)
        db.session.commit()
        flash(f"Submitted {form.name.data}!")
    return render("insert.jinja", form=form)

@app.route("/cart")
def cart():
    return render("cart.jinja", items=get_cart())

@app.route("/update/<int:item_id>", methods=["GET", "POST"])
def update(item_id):
    item = Keyboard.query.get_or_404(item_id)
    form = KeyboardForm()
    if request.method == "GET":
        form.process(obj=item)
    elif request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(item)
            if form.image.data:
                item.img_small = to_img64(request.files["image"], 200)
                item.img_large = to_img64(request.files["image"], 600)
            db.session.add(item)
            db.session.commit()
            print("return inv")
            return inventory()
    return render("update.jinja", title="Update", item=item, form=form)