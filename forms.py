from wtforms import StringField, SubmitField, SelectField, BooleanField, RadioField
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm

class VenueForm(FlaskForm):
    venue_name = StringField('name', validators=[DataRequired()])
    venue_address = StringField('address', validators=[DataRequired()])
    venue_img_link = StringField('image link', validators=[URL()])
    venue_url = StringField('web address', validators=[DataRequired(), URL()])
    venue_indoor = SelectField('indoor or outdoor', validators=[DataRequired()],
                               choices=[("indoor", "Indoor"), ("outdoor", "Outdoor")])
    venue_owner = RadioField('venue ownership', validators=[DataRequired()],
                             choices=[("1", "1 - least cooperative"), ("2", "2"), ("3", "3"), ("4", "4"),
                                      ("5", "5 - most cooperative")])
    venue_refrigeration = BooleanField('venue has refrigeration')
    can_cook = BooleanField('cooking facilities?')
    back_entrance = BooleanField('service entrance?')
    service_area_size = RadioField('size of service area', validators=[DataRequired()],
                                   choices=[("small", "Small"), ("medium", "Decent"), ("large", "Opulent")])
    submit = SubmitField('Submit THANKS')
