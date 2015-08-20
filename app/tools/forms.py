from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField, TextField, HiddenField
from ..models import Quality

class MoveForm(Form):
    append_fen = HiddenField()
    append_san = HiddenField()
    quality = SelectField('Quality', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(MoveForm, self).__init__(*args, **kwargs)
        self.quality.choices = [(quality.id, quality.name)
                             for quality in Quality.query.all()]
