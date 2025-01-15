from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os
import pdfplumber
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Konfigurasi
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Maksimal ukuran file 5 MB
app.secret_key = 'your_secret_key'

# Konfigurasi database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cv_analysis'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Middleware
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Harap login terlebih dahulu.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def admin_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Halaman ini hanya dapat diakses oleh admin.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash('Login berhasil!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah.', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'on'

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)",
                           (username, hashed_password, is_admin))
            conn.commit()
            flash('Pendaftaran berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username sudah terdaftar.', 'error')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout berhasil.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM CVs")
    total_cvs = cursor.fetchone()[0]
    conn.close()
    return render_template('index.html', total_cvs=total_cvs)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'cv' not in request.files or request.files['cv'].filename == '':
            flash('Tidak ada file yang diunggah.', 'error')
            return redirect(request.url)
        
        file = request.files['cv']
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                extracted_text = extract_text_from_pdf(filepath)
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO CVs (filename, extracted_text) VALUES (%s, %s)", 
                               (filename, extracted_text))
                conn.commit()
                conn.close()
                flash('CV berhasil diunggah dan teks diekstraksi!', 'success')
            except Exception as e:
                flash(f'Terjadi kesalahan: {str(e)}', 'error')
        else:
            flash('Hanya file PDF yang diperbolehkan.', 'error')
    return render_template('upload.html')

@app.route('/criteria', methods=['GET', 'POST'])
@admin_required
def criteria():
    if request.method == 'POST':
        position = request.form['position']
        education = request.form['education']
        experience = request.form['experience']
        skills = ', '.join(request.form.getlist('skills[]'))
        languages = ', '.join(request.form.getlist('languages[]'))
        certifications = ', '.join(request.form.getlist('certifications[]'))
        achievements = ', '.join(request.form.getlist('achievements[]')) if request.form.getlist('achievements[]') else None

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Kriteria_Penilaian (posisi, pendidikan_minimum, pengalaman_minimum, keterampilan, bahasa, sertifikasi, penghargaan_prestasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (position, education, experience, skills, languages, certifications, achievements))
        conn.commit()
        conn.close()

        flash('Kriteria berhasil disimpan!', 'success')
    return render_template('criteria.html')

@app.route('/cv_list')
@admin_required
def cv_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename FROM CVs")
    cvs = cursor.fetchall()
    conn.close()
    return render_template('cv_list.html', cvs=cvs)

@app.route('/criteria_list')
@admin_required
def criteria_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, posisi FROM Kriteria_Penilaian")
    criteria_positions = cursor.fetchall()
    conn.close()
    return render_template('criteria_list.html', criteria_positions=criteria_positions)

@app.route('/analysis', methods=['GET', 'POST'])
@admin_required
def analysis():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename FROM CVs")
    cvs = cursor.fetchall()
    cursor.execute("SELECT id, posisi FROM Kriteria_Penilaian")
    criteria_positions = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        # Implementasi analisis (sama seperti sebelumnya)
        pass

    return render_template('analysis.html', cvs=cvs, criteria_positions=criteria_positions)

def extract_text_from_pdf(filepath):
    with pdfplumber.open(filepath) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
    return text

if __name__ == '__main__':
    app.run(debug=True)
