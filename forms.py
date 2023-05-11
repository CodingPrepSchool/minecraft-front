from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, HiddenField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    post_id = HiddenField()
    post = TextAreaField("Whats new?", validators = [DataRequired()])
    submit = SubmitField("Upload")