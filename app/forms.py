from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class JoinForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=3, max=12), DataRequired()])
    lobby = StringField(label="Lobby code", validators=[Length(min=6, max=6), DataRequired()])
    submit = SubmitField(label='Play')


class PlayForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=3, max=12), DataRequired()])
    roundLength = SelectField(label="Round length", choices=["1 minute", "2 minutes", "3 minutes"], default="2 minutes")
    submit = SubmitField(label='Play')
