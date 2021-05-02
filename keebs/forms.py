from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.html5 import NumberInput

class KeyboardForm(FlaskForm):
    kw = {"title": "Keyboard Form", "id": "item-form"}
    brand = StringField("Brand", validators=[DataRequired(), Length(min=2, max=64)])
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=64)])
    model = StringField("Model", validators=[DataRequired(), Length(min=2, max=64)])
    switch = StringField("Switch", validators=[DataRequired(), Length(min=2, max=64)])
    desc = StringField("Description", validators=[DataRequired()])
    quantity = StringField("Quantity", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    image = FileField("Image", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    kw = {"id": "search-form", "ignore_labels": True}
    input = StringField("Search", validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField("Submit")

class AddCartForm(FlaskForm):
    kw = {"id": "cart-form"}
    quantity = IntegerField(widget=NumberInput(min=1), default=1)
    submit = SubmitField("Add To Cart")