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


@app.route('/', methods=['GET'])
def index():
    """
    По ТЗ не понятно, какого формата входная строка,
    могут ли там быть лишние пробелы в выражении (например: math.sqrt(    4) + 2),
    поэтому строку выражения получаю из всего url.
    Если мы знаем, что лишних пробелов нет во входной строке,
    то строку-выражение можно получить из request.args.
    """
    print(request.query_string)
    url = request.url
    url = url.replace('%2B', '+')
    url = url.replace('%20', ' ')
    url = url.replace('%2F', '/')

    index_expression = url.find('expr=')
    expression = url[index_expression + 5:len(url)]

    form = ExpressionForm()

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
