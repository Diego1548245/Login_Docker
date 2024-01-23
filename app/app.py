from flask import Flask, render_template, request, flash

import mysql.connector

app = Flask(__name__)
app.secret_key = 'Datos Inválidos'
config = {
    'host':'localhost',
    'user':'root',
    'password':'',
    'db':'LoginDB'
}

cnx=mysql.connector.connect(**config)

@app.route('/')
def index():
    return render_template('index.html')


# SECCIÓN REGISTRO

@app.route('/signup', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        Nombres = request.form['Nombres']
        Apellidos = request.form['Apellidos']
        Correo = request.form['Correo']
        Passwordd = request.form['Passwordd']

        cursor = cnx.cursor(dictionary=True)
        query = ("insert into Usuario (Nombres, Apellidos, Correo, Passwordd) values (%s, %s, %s, %s)")
        data = (Nombres, Apellidos, Correo, Passwordd)
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
        return render_template('signup_check.html')
    
    return render_template('signup.html')


# SECCIÓN INICIAR SESIÓN

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        Correo = request.form['Correo']
        Passwordd = request.form['Passwordd']

        cursor = cnx.cursor(dictionary=True)
        query = "select Correo, Passwordd from Usuario where Correo = %s and Passwordd = %s"
        cursor.execute(query, (Correo, Passwordd))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario and usuario['Passwordd'] == Passwordd:
            return render_template('login_check.html')
        
        else : flash('Datos inválidos')
        
    return render_template('login.html')


# SECCIÓN RECUPERAR CONTRASEÑA

@app.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        Correo = request.form['Correo']

        cursor = cnx.cursor(dictionary=True)
        query = 'select Correo from Usuario where Correo = %s'
        cursor.execute(query, (Correo,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario : return render_template('forgot_check.html')
        
        else : flash('Datos inválidos')

    return render_template('forgot_password.html')


# SECCIÓN CAMBIAR CONTRASEÑA

@app.route('/change_password', methods = ['GET', 'POST'])
def change_password():
    if request.method == 'POST' :
        Correo = request.form['Correo']
        Passwordd = request.form['Passwordd']
        new_Passwordd = request.form['new_Passwordd']

        cursor = cnx.cursor(dictionary=True)
        query_select = 'select id from Usuario where Correo = %s and Passwordd = %s'
        cursor.execute(query_select, (Correo, Passwordd))
        usuario = cursor.fetchone()

        if usuario :
            query_update = 'UPDATE Usuario SET Passwordd = %s WHERE id = %s'
            cursor.execute(query_update, (new_Passwordd, usuario['id']))
            cnx.commit
            cursor.close()
            return render_template('change_check.html')

        else : flash('Datos inválidos')

    return render_template('change_password.html')

if __name__ == '__main__' :
    app.run(debug=True, port=5000)