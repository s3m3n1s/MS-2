import datetime
import io
import numpy as np

from flask import render_template, request, Flask, Response, url_for, redirect
from werkzeug.utils import secure_filename
from solver import solve

from form import MainForm
from flask_bootstrap import Bootstrap

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.secret_key = "kek"
Bootstrap(app)


@app.route('/', methods=['POST', 'GET'])
def get_vars():
    """Возрашает отрисованный интерфейс"""
    form = MainForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        if not filename:
            filename = str(datetime.datetime.now())
        form.file.data.save('uploads/' + filename)
        sol = solve(filename, int(request.form["order"]))
        data = "y = "
        if type(sol) is str:
            return render_template('data.html', formula=sol, image='/grust.png', result="Результат убил!")
        for num, i in enumerate(sol):
            if i >= 0 and num != 0:
                data += " +"
            data += f" {i:.2f} * x^{num}"

        image = '/plot.png?X={}&x1={}&x2={}'.format(
            data.replace('y = ', '').replace(" ", "").replace("^", "**").replace("+", "P"), request.form['x1'], request.form['x2'])
        return render_template('data.html', formula=data, image=image, result="Результат!")
    return render_template('form.html', form=form)


@app.route('/plot.png')
def plot_png_X():
    """Возвращает картинку"""
    x = request.args.get('X')
    x1 = int(request.args.get('x1'))
    x2 = int(request.args.get('x2'))

    fig = create_figure(x, x1, x2)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/grust.png')
def grust():
    """Возвращает грустную картинку"""
    with open('res/img.png', 'rb') as img:
        return Response(img.read(), mimetype='image/png')


def create_figure(X, x1, x2):
    """Создаёт картинку (график)"""
    fig = Figure()
    x = np.arange(x1, x2, 0.01)
    y = eval(X.replace('P', "+"))
    print(X)
    axis = fig.add_subplot(1, 1, 1)
    axis.grid(True, which='both')
    axis.plot(x, y)
    return fig


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
