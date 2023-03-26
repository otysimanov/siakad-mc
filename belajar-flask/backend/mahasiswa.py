from flask import Blueprint, render_template, url_for, redirect, flash, session, jsonify, request
from backend.db import db, storage
from backend.auth import login_required

mahasiswa = Blueprint('mahasiswa', __name__)

@mahasiswa.route('/mahasiswa', methods =['POST','GET'])
@login_required
def daftar_mahasiswa():
    if request.method == 'POST':
        #simpan dictonary

        # return jsonify(request.files)
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'nim' : request.form['nim'],
            'jurusan' : request.form['jurusan'],
            'is_active' : True
        }

        if 'gambar' in request.files and request.files['gambar']:
            image = request.files['gambar']
            # buatkan kondisi
            allowed_extensions = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"profil/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in allowed_extensions:
                storage.child(lokasi).put(image)
                data['profil'] = storage.child(lokasi).get_url(None)
            else:
                flash('Foto Tidak di Perbolehkan', 'danger')
                return redirect(url_for('.daftar_mahasiswa'))
            
        db.collection('mahasiswa').document().set(data)
        flash('Berhasil Menambahkan Mahasiswa','success')
        return redirect(url_for('mahasiswa.daftar_mahasiswa'))
    
    #panggil database
    docs = db.collection('mahasiswa').stream()
    mhs = []
    for doc in docs:
        user = doc.to_dict()
        user['id'] = doc.id
        mhs.append(user)

    jurs = db.collection('jurusan').stream()
    data = []
    for jur in jurs:
        usr = jur.to_dict()
        usr['id'] = jur.id
        data.append(usr)

    return render_template('mahasiswa.html', students = mhs, jurusan=data)


@mahasiswa.route('/mahasiswa/lihat/<uid>')
@login_required
def lihat_mahasiswa(uid):
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('lihat_mahasiswa.html', data = mahasiswa)

@mahasiswa.route('/mahasiswa/delete', methods= ['POST'])
@login_required
def delete_mahasiswa():
    uid = request.form['uid']
    db.collection('mahasiswa').document(uid).delete()
    flash('Berhasil Hapus Mahasiswa', 'danger')
    return redirect(url_for('.daftar_mahasiswa'))

@mahasiswa.route('/mahasiswa/edit/<uid>', methods=['GET','POST'])
@login_required
def edit_mhs(uid):
    if request.method == 'POST':
        #simpan dictonary
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'nim' : request.form['nim'],
            'jurusan' : request.form['jurusan']
        }
        #simpan database
        db.collection('mahasiswa').document(uid).set(data, merge=True)
        flash('Berhasil Edit Mahasiswa','success')
        return redirect(url_for('.daftar_mahasiswa'))
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('edit_mhs.html', data = mahasiswa)
