from flask import Flask, render_template, url_for, Response, stream_with_context
from flask.wrappers import Response
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL
from decouple import config
import json
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = config('HOST')
app.config['MYSQL_DATABASE_USER'] = config('USER_DB')
app.config['MYSQL_DATABASE_PASSWORD'] = config('PASSWORD_DB')
app.config['MYSQL_DATABASE_DB'] = config('NAME_DB')
mysql.init_app(app)


def _datos(cur):
    try:
        cur.execute(
            'SELECT fecha_hora, agua_flujo FROM datos_dia WHERE id = (SELECT MAX(id) FROM datos_dia)')
        datos_tiempo_real = cur.fetchall()
        json_data = json.dumps(
            {'fecha': datos_tiempo_real[0][0].strftime("%d/%m/%Y %H:%M:%S"), 'numero1': datos_tiempo_real[0][1]})
    except:
        json_data = json.dumps(
            {'fecha':  datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'numero1': 0})
    yield f"data:{json_data}\n\n"

@app.route('/')
def index():
    return render_template('index.html', inicio="active")


@app.route('/graficas')
def graficas():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT  agua_flujo, fecha_hora FROM datos_dia")
    flujo_dia = cur.fetchall()

    cur.execute(
        "SELECT  maximo_flujo, fecha FROM datos_semana")
    flujo_semana = cur.fetchall()
    
    cur.execute(
        "SELECT maximo_flujo FROM datos_semana WHERE week(fecha)=week(now())")
    flujo_semana_actual = cur.fetchall()
    print(flujo_semana_actual)
    
    
    return render_template('graficas.html', graficas="active",
                           flujo_dia=flujo_dia, flujo_semana=flujo_semana,
                           flujo_semana_actual=flujo_semana_actual)


@app.route('/tablas')
def tablas():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT * FROM datos_semana")
    valores = cur.fetchall()
    return render_template('tablas.html', tablas="active", valores=valores)

@app.route('/flujo_tiempo_real')
def flujo_tiempo_real():
    cur = mysql.get_db().cursor()
    
    enviar = _datos(cur)
    
    return Response(stream_with_context(enviar), mimetype='text/event-stream')

@app.route('/predicciones')
def predicciones():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT * FROM datos_prediction")
    valores = cur.fetchall()

    return render_template('predicciones.html', predicciones="active", valores=valores)


if __name__ == "__main__":
    app.run(debug=True)
