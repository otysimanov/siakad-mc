from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from backend.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('auth.login'))
    return wrapper

@auth.route('/register', methods=['POST','GET'])
def register():
    #jika method == post
    if request.method == 'POST':
        # tangkap data form
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'username': request.form['username'],
            'email': request.form['email']
        }
        # cek apakah password dan password_1 itu sama
        if request.form['password'] != request.form['password_1']:
            flash('Password Tidak Sama Silahkan Ulang', 'danger')
            return redirect(url_for('auth.register'))
        # set enskripsi password
        data['password'] = generate_password_hash(request.form['password'], 'sha256')
        # cek apakah username sudah ada 
        users = db.collection('users').document(data['username']).get().to_dict()
        if users:
            flash('Username Sudah Terdaftar', 'danger')
            return redirect(url_for('auth.login'))
        # simpan ke dalam database
        # kembali ke halaman index
        else:
            db.collection('users').document(data['username']).set(data, merge=True)
            flash('Berhasil Menambahkan User', 'success')
            return redirect(url_for('index'))
        
    return render_template('register.html')

@auth.route('/login', methods = ["POST", "GET"])
def login():
     # cek dlu request.method
    if request.method == 'POST':
        # tangkap data
        data = {
            'username': request.form['username'],
            'password' : request.form['password']
        }
        # cek user
        user = db.collection('users').document(data['username']).get().to_dict()
        if user:            
            # cek password
            if check_password_hash(user['password'], data['password']):
                # menggunakan session
                session['user'] = user
                flash('Berhasil Login', 'success')
                return redirect(url_for('index'))
            else:
                flash('Username/Password Anda Salah', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Username/Password Anda Salah', 'danger')
            return redirect(url_for('auth.login'))
        
    if 'user' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Berhasil Logout', 'success')
    return redirect(url_for('auth.login'))
