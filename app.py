from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from backend.db import db 

from backend.auth import auth
from backend.mahasiswa import mahasiswa

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = '4p44p4'

app.register_blueprint(auth)  
app.register_blueprint(mahasiswa)  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dosen', methods = ['POST', 'GET'])
def dosen(): 
    if 'user' not in session:
        flash('Anda Harus login', 'danger')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        #simpan dictonary
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'nidn' : request.form['nidn'],
            'matakuliah' : request.form['dosen'],
            'is_active' : True
        }
        #simpan database
        db.collection('dosen').document().set(data)
        flash('Berhasil Menambahkan Dosen','success')
        return redirect(url_for('dosen'))
    
    #panggil database
    dos = db.collection('dosen').stream()
    dos_mk = []
    for dosen in dos:
        dosn = dosen.to_dict()
        dosn['id'] = dosen.id
        dos_mk.append(dosn)

    jurs = db.collection('jurusan').stream()
    data = []
    for jur in jurs:
        usr = jur.to_dict()
        usr['id'] = jur.id
        data.append(usr)
    return render_template('dosen.html', dosmat = dos_mk, jurusan = data)




#code menjalankan flask
if __name__ == '__main__':
    app.run(debug=True)
