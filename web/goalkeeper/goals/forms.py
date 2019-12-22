from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms.validators import DataRequired

class GoalForm(FlaskForm):
    title = StringField('Goal Name', validators=[DataRequired()])
    description = StringField('Goal Description', validators=[DataRequired()])
    due_date = StringField('Goal Due Date')
    tags = StringField('Tags')
    private_goal = BooleanField('Private')
