from wtforms import Form, validators
from wtforms.fields import StringField
from wtforms.validators import ValidationError, NumberRange

class CreatePolicy(Form):
    default_src = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Default src"})
    script_src = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Script src"})
    script_src_elem = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Script src elem"})
    script_src_attr = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Script src attr"})
    img_src = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Img src"})
    style_src = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Style src"})
    style_src_elem = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Style src elem"})
    style_src_attr = StringField([validators.Length(min=1, max=250)], render_kw={"placeholder": "Style src attr"})