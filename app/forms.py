from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, PasswordField, SelectField, StringField, TextAreaField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError

from app.models import STATUSES


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password (8+ characters)", validators=[DataRequired(), Length(min=8, max=128)])
    confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", "Passwords must match.")])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class ApplicationForm(FlaskForm):
    company = StringField("Company", validators=[DataRequired(), Length(max=120)])
    role = StringField("Role", validators=[DataRequired(), Length(max=120)])
    status = SelectField("Status", choices=[(s, s) for s in STATUSES])
    date_applied = DateField("Date applied", validators=[Optional()])
    salary_min = IntegerField("Salary min ($)", validators=[Optional(), NumberRange(min=0)])
    salary_max = IntegerField("Salary max ($)", validators=[Optional(), NumberRange(min=0)])
    job_url = StringField("Job posting URL", validators=[Optional(), URL(), Length(max=500)])
    next_followup = DateField("Next follow-up", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Length(max=5000)])

    def validate_salary_max(self, field):
        if field.data is not None and self.salary_min.data is not None and field.data < self.salary_min.data:
            raise ValidationError("Max salary can't be lower than min salary.")
