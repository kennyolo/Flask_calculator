from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEY'

bootstrap = Bootstrap(app)
moment = Moment(app)


class ExpressionForm(FlaskForm):
    expression = StringField('Enter expression')
    calculate = SubmitField('Calculate')
    result = StringField('Result')


class Calculater:

    def __init__(self, calculated_expression):
        self.calculated_expression = calculated_expression
        self.result = None

    def run(self):
        """
            Проверяет выражение на отсутсвие знака умножения между скобками.
            При необходимости добавляет знак умножения для корректной аботы eval().
        """
        self.calculated_expression = self.calculated_expression.replace(' ', '')
        multiplication_index = self.calculated_expression.find(')(')
        while multiplication_index != -1:
            len_expression = len(self.calculated_expression)
            self.calculated_expression = self.calculated_expression[0:multiplication_index + 1] + \
                                         '*' + \
                                         self.calculated_expression[multiplication_index + 1: len_expression + 1]
            multiplication_index = self.calculated_expression.find(')(')

        self.result = eval(self.calculated_expression)


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    expression = None
    form = ExpressionForm()
    if form.validate_on_submit():
        expression = form.expression.data
        calculater = Calculater(expression)
        try:
            calculater.run()
            form.result.data = calculater.result
        except ZeroDivisionError:
            form.result.data = 'Division by zero'
        except Exception:
            form.result.data = 'Invalid Input'
    return render_template('index.html', form=form, name=expression)


if __name__ == '__main__':
    app.run(debug=True)

    print(str)
