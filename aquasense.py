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

def conversion_horas(tup):
    dic = {}
    for x, y in tup:
        dic.setdefault(y.strftime("%H:%M:%S"), x)
    return dic

def conversion_dias(tup):
    dic = {}
    for x, y in tup:
        dic.setdefault(y.strftime("%Y-%m-%d"), x)
    return dic

def _datos(cur):
    cur.execute(
        'SELECT fecha_hora, agua_flujo FROM datos_dia WHERE id = (SELECT MAX(id) FROM datos_dia)')
    datos_tiempo_real = cur.fetchall()
    json_data = json.dumps(
        {'fecha': datos_tiempo_real[0][0].strftime("%d/%m/%Y %H:%M:%S"), 'numero1': datos_tiempo_real[0][1]})

    yield f"data:{json_data}\n\n"

@app.route('/')
def index():
    return render_template('index.html', inicio="active")


@app.route('/graficas')
def graficas():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT  agua_flujo, fecha_hora FROM datos_dia")
    valores = cur.fetchall()
    flujo_dia = conversion_horas(valores)
    
    cur.execute(
        "SELECT  maximo_flujo, fecha FROM datos_semana")
    valores = cur.fetchall()
    flujo_semana = conversion_dias(valores)
    
    cur.execute(
        "SELECT maximo_flujo FROM datos_semana WHERE week(fecha)=week(now())")
    valores = cur.fetchall()

    flujo_semana_actual = [valores[x][0] for x in range(len(valores))]
    
    return render_template('graficas.html', graficas="active",
                           flujo_dia=flujo_dia, flujo_semana=flujo_semana,
                           flujo_semana_actual=flujo_semana_actual)


@app.route('/tablas')
def tablas():
    cur = mysql.get_db().cursor()
    cur.execute(
        "SELECT * FROM datos_semana")
    valores = cur.fetchall()
    print(valores)
    return render_template('tablas.html', tablas="active", valores=valores)

@app.route('/flujo_tiempo_real')
def flujo_tiempo_real():
    cur = mysql.get_db().cursor()
    
    enviar = _datos(cur)
    
    return Response(stream_with_context(enviar), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)
