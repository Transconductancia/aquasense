from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html', inicio="active")


@app.route('/graficas')
def graficas():
    return render_template('graficas.html', graficas="active")


@app.route('/tablas')
def tablas():
    return render_template('tablas.html', tablas="active")


if __name__ == "__main__":
    app.run(debug=True)
