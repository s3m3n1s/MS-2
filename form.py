"""
Предоставляет классы форм
"""


from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FileField


class MainForm(FlaskForm):
    """
    Создает форму с тремя полями для коэффициентов и кнопкой отправки
    """
    order = IntegerField('Наивысшая степень')
    file = FileField("Прикрепите файлик с координатами точек")
    x1 = IntegerField('Икс от которого график строить')
    x2 = IntegerField('Икс до которого график строить')
    submit = SubmitField('Посчитать')

