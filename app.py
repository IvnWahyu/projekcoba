from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os
import pdfplumber
import re
import dateparser
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Tentukan folder tempat menyimpan file yang diunggah
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Gunakan folder 'uploads' di direktori kerja saat ini
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Maksimal ukuran file 5 MB

# Kunci rahasia untuk flash messages
app.secret_key = 'your_secret_key'

# Konfigurasi database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cv_analysis2'
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

        if user and check_password_hash(user['password'], password):
            # Update waktu login terakhir
            cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
            conn.commit()
            conn.close()

            # Set sesi login
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash('Login berhasil!', 'success')
            return redirect(url_for('index'))
        else:
            conn.close()
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


# Halaman Dashboard
@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Hitung jumlah CV yang diunggah
    cursor.execute("SELECT COUNT(*) AS total_cvs FROM CVs")
    total_cvs = cursor.fetchone()['total_cvs']
    
    # Hitung jumlah pengguna jika admin login
    total_users = None
    user_data = None
    if session.get('is_admin'):
        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        total_users = cursor.fetchone()['total_users']
    else:
        # Ambil data pengguna untuk pengguna biasa
        cursor.execute("SELECT created_at, last_login FROM users WHERE id = %s", (session['user_id'],))
        user_data = cursor.fetchone()

    conn.close()
    
    return render_template('index.html', total_cvs=total_cvs, total_users=total_users, user_data=user_data)


# Halaman Pengaturan Kriteria
@app.route('/criteria', methods=['GET', 'POST'])
@login_required
def criteria():
    if request.method == 'POST':
        # Mengambil data dari form
        position = request.form['position']
        education = request.form['education']
        experience = request.form['experience']
        skills = ', '.join(request.form.getlist('skills[]'))  # Menangani keterampilan
        languages = ', '.join(request.form.getlist('languages[]'))  # Menangani bahasa
        certifications = ', '.join(request.form.getlist('certifications[]'))  # Menangani sertifikasi
        achievements = ', '.join(request.form.getlist('achievements[]')) if request.form.getlist('achievements[]') else None  # Menangani penghargaan

        # Menyimpan data ke database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Kriteria_Penilaian (posisi, pendidikan_minimum, pengalaman_minimum, keterampilan, bahasa, sertifikasi, penghargaan_prestasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (position, education, experience, skills, languages, certifications, achievements))
        conn.commit()
        conn.close()

        flash('Kriteria berhasil disimpan!', 'success')
        return redirect('/criteria')

    return render_template('criteria.html')

# Halaman Unggah CV
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Cek apakah file diunggah
        if 'cv' not in request.files:
            flash('Tidak ada file yang diunggah', 'error')
            return redirect(request.url)
        
        file = request.files['cv']
        
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Ekstraksi teks dari PDF
            try:
                extracted_text = extract_text_from_pdf(filepath)
                # Simpan CV ke database setelah ekstraksi
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO CVs (filename, extracted_text) VALUES (%s, %s)", 
                               (filename, extracted_text))
                conn.commit()
                conn.close()
                flash('CV berhasil diunggah dan teks diekstraksi!', 'success')
                return render_template('upload.html', extracted_text=extracted_text)
            except Exception as e:
                flash(f'Terjadi kesalahan saat mengekstrak teks: {str(e)}', 'error')
                return redirect(request.url)

    return render_template('upload.html')

# Fungsi untuk mengekstrak teks dari PDF
def extract_text_from_pdf(filepath):
    with pdfplumber.open(filepath) as pdf:
        text = ''
        for page in pdf.pages:  # Loop melalui semua halaman
            text += page.extract_text()  # Tambahkan teks dari setiap halaman
    return text

# Halaman Daftar CV yang Telah Diunggah
@app.route('/cv_list')
@admin_required
def cv_list():
    # Ambil semua CV dari database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename FROM CVs")  # Ambil ID dan nama file dari CV yang diunggah
    cvs = cursor.fetchall()
    conn.close()

    return render_template('cv_list.html', cvs=cvs)

# Halaman Daftar Kriteria Penilaian
@app.route('/criteria_list')
@admin_required
def criteria_list():
    # Ambil semua kriteria penilaian
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, posisi FROM Kriteria_Penilaian")  # Ambil semua posisi dari kriteria
    criteria_positions = cursor.fetchall()
    conn.close()

    return render_template('criteria_list.html', criteria_positions=criteria_positions)

# Halaman Analisis CV
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

    analysis_results = []
    analysis_scores_list = []
    selected_criteria_list = []
    cv_text = None

    if request.method == 'POST':
        cv_id = request.form.get('cv_id')
        criteria_id = request.form.get('criteria_id')

        if cv_id:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CVs WHERE id = %s", (cv_id,))
            cv = cursor.fetchone()
            conn.close()

            if not cv:
                flash('CV tidak ditemukan', 'error')
                return redirect(url_for('analysis'))

            cv_text = cv[2]  # Teks ekstraksi CV

            if criteria_id == "all":
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Kriteria_Penilaian")
                all_criteria = cursor.fetchall()
                conn.close()

                for criteria in all_criteria:
                    analysis_result = analyze_text(cv_text, criteria)
                    analysis_scores = analyze_scores(cv_text, criteria)
                    analysis_results.append(analysis_result)
                    analysis_scores_list.append(analysis_scores)
                    selected_criteria_list.append(criteria)
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Kriteria_Penilaian WHERE id = %s", (criteria_id,))
                criteria = cursor.fetchone()
                conn.close()

                if not criteria:
                    flash('Kriteria tidak ditemukan', 'error')
                    return redirect(url_for('analysis'))

                analysis_result = analyze_text(cv_text, criteria)
                analysis_scores = analyze_scores(cv_text, criteria)
                analysis_results.append(analysis_result)
                analysis_scores_list.append(analysis_scores)
                selected_criteria_list.append(criteria)

            # Kirim konteks bersama fungsi zip ke template
            return render_template(
                'analyze_cv.html', 
                cv=cv, 
                analysis_results=analysis_results,
                analysis_scores_list=analysis_scores_list,
                selected_criteria_list=selected_criteria_list,
                zip=zip  # Tambahkan zip di sini
            )

    return render_template('analysis.html', cvs=cvs, criteria_positions=criteria_positions)


# Fungsi untuk menganalisis teks dan memberikan skor berdasarkan kriteria
def analyze_text(extracted_text, criteria):
    # Analisis sederhana: menghitung jumlah kata dalam teks ekstraksi
    word_count = len(extracted_text.split())
    return f"Jumlah kata dalam teks: {word_count} kata"

def extract_experience_duration(extracted_text):
    # Regex untuk mengekstrak durasi pengalaman kerja
    date_pattern = r"(\d{1,2}\s*(tahun|thn|bulan|bln))|(\d{1,2}/\d{4}\s*-\s*\d{1,2}/\d{4})"
    matches = re.findall(date_pattern, extracted_text)
    
    total_duration_years = 0

    for match in matches:
        if match[0]:  # Format durasi langsung (misalnya, "2 tahun 6 bulan")
            duration = match[0]
            if "tahun" in duration or "thn" in duration:
                years = int(re.search(r'\d+', duration).group())
                total_duration_years += years
            elif "bulan" in duration or "bln" in duration:
                months = int(re.search(r'\d+', duration).group())
                total_duration_years += months / 12
        elif match[2]:  # Format MM/YYYY - MM/YYYY (misalnya, "10/2023 - 05/2024")
            start_date_str, end_date_str = match[2].split('-')
            start_date = dateparser.parse(start_date_str.strip(), date_formats=['%m/%Y'])
            end_date = dateparser.parse(end_date_str.strip(), date_formats=['%m/%Y'])
            if start_date and end_date:
                duration_days = (end_date - start_date).days
                total_duration_years += duration_days / 365

    return round(total_duration_years, 2)
# Fungsi untuk menganalisis skor berdasarkan kriteria

def analyze_scores(extracted_text, criteria):
    education_score = 0
    experience_score = 0
    skills_score = 0
    language_score = 0
    certificate_score = 0
    award_score = 0

    # Skor Pendidikan
    if criteria[1] in extracted_text:
        education_score = 20

    # Skor Pengalaman
    experience_duration = extract_experience_duration(extracted_text)
    required_experience = int(criteria[3])  # Kriteria pengalaman minimum (dalam tahun)
    if experience_duration >= required_experience:
        experience_score = 20
    else:
        experience_score = (experience_duration / required_experience) * 20

    # Skor Keterampilan
    skills_keywords = []
    if isinstance(criteria[4], str):
        skills_keywords = [skill.strip().lower() for skill in criteria[4].split(",")]

    matched_skills = 0
    for skill in skills_keywords:
        if skill in extracted_text.lower():
            matched_skills += 1

    if skills_keywords:
        skills_score = (matched_skills / len(skills_keywords)) * 30
    else:
        skills_score = 0

    # Skor Bahasa
    languages_keywords = []
    if isinstance(criteria[5], str):
        languages_keywords = [lang.strip().lower() for lang in criteria[5].split(",")]

    matched_languages = 0
    for language in languages_keywords:
        if language in extracted_text.lower():
            matched_languages += 1

    if languages_keywords:
        language_score = (matched_languages / len(languages_keywords)) * 20
    else:
        language_score = 0

    # Skor Sertifikasi
    certificates_keywords = []
    if isinstance(criteria[6], str):
        certificates_keywords = [cert.strip().lower() for cert in criteria[6].split(",")]

    matched_certificates = 0
    for certificate in certificates_keywords:
        if certificate in extracted_text.lower():
            matched_certificates += 1

    if certificates_keywords:
        certificate_score = (matched_certificates / len(certificates_keywords)) * 25
    else:
        certificate_score = 0

    # Skor Penghargaan
    awards_keywords = []
    if isinstance(criteria[7], str):
        awards_keywords = [award.strip().lower() for award in criteria[7].split(",")]

    matched_awards = 0
    for award in awards_keywords:
        if award in extracted_text.lower():
            matched_awards += 1

    if awards_keywords:
        award_score = (matched_awards / len(awards_keywords)) * 10
    else:
        award_score = 0

    # Total skor
    total_score = ((education_score + experience_score + skills_score + language_score + certificate_score + award_score) / 105) * 100
    total_score = round(total_score, 2)

    return {
        'education_score': education_score,
        'experience_score': experience_score,
        'experience_duration': experience_duration,  # Tambahkan durasi pengalaman
        'skills_score': round(skills_score, 2),
        'language_score': round(language_score, 2),
        'certificate_score': round(certificate_score, 2),
        'award_score': round(award_score, 2),
        'total_score': total_score
    }

    
@app.route('/analyze_cv/<int:cv_id>', methods=['GET'])
def analyze_cv(cv_id):
    # Ambil data CV berdasarkan id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CVs WHERE id = %s", (cv_id,))
    cv = cursor.fetchone()

    if not cv:
        flash('CV tidak ditemukan', 'error')
        return redirect(url_for('cv_list'))  # Pastikan ini mengarah ke halaman daftar CV

    # Ambil kriteria penilaian terbaru
    cursor.execute("SELECT * FROM Kriteria_Penilaian ORDER BY id DESC LIMIT 1")
    criteria = cursor.fetchone()

    if not criteria:
        flash('Kriteria penilaian belum diatur', 'error')
        return redirect(url_for('criteria'))  # Pastikan ini mengarah ke halaman pengaturan kriteria

    # Lakukan analisis terhadap teks ekstraksi CV
    analysis_result = analyze_text(cv[2], criteria)  # cv[2] berisi teks ekstraksi CV
    analysis_scores = analyze_scores(cv[2], criteria)

    conn.close()

    return render_template('analyze_cv.html', cv=cv, analysis_result=analysis_result, analysis_scores=analysis_scores)

@app.route('/view_extracted_text/<int:cv_id>', methods=['GET'])
def view_extracted_text(cv_id):
    # Ambil data CV berdasarkan id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename, extracted_text FROM CVs WHERE id = %s", (cv_id,))
    cv = cursor.fetchone()

    if not cv:
        flash('CV tidak ditemukan', 'error')
        return redirect(url_for('cv_list'))  # Kembali ke daftar CV jika CV tidak ditemukan

    conn.close()
    return render_template('view_extracted_text.html', cv=cv)


@app.route('/view_criteria/<int:criteria_id>', methods=['GET'])
def view_criteria(criteria_id):
    # Ambil data kriteria berdasarkan ID
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Kriteria_Penilaian WHERE id = %s", (criteria_id,))
    criteria = cursor.fetchone()

    if not criteria:
        flash('Kriteria tidak ditemukan', 'error')
        return redirect(url_for('criteria_list'))  # Kembali ke daftar kriteria jika kriteria tidak ditemukan

    conn.close()
    return render_template('view_criteria.html', criteria=criteria)

@app.route('/user_list')
@admin_required
def user_list():
    # Ambil semua pengguna dari database termasuk created_at dan last_login
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, is_admin, created_at, last_login FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('user_list.html', users=users)



@app.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    flash('Pengguna berhasil dihapus.', 'success')
    return redirect(url_for('user_list'))


@app.route('/user_detail/<int:user_id>')
@admin_required
def user_detail(user_id):
    # Ambil detail pengguna berdasarkan ID
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, is_admin, created_at, last_login FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        flash('Pengguna tidak ditemukan.', 'error')
        return redirect(url_for('user_list'))

    return render_template('user_detail.html', user=user)

@app.route('/delete_cv/<int:cv_id>', methods=['POST'])
@admin_required
def delete_cv(cv_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM CVs WHERE id = %s", (cv_id,))
        conn.commit()
        flash('CV berhasil dihapus.', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('cv_list'))

@app.route('/delete_criteria/<int:criteria_id>', methods=['POST'])
@admin_required
def delete_criteria(criteria_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Kriteria_Penilaian WHERE id = %s", (criteria_id,))
        conn.commit()
        flash('Kriteria berhasil dihapus.', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('criteria_list'))

@app.route('/save_analysis/<int:cv_id>/<int:criteria_id>', methods=['POST'])
@admin_required
def save_analysis(cv_id, criteria_id):
    # Ambil hasil analisis dari form
    analysis_result = request.form.get('analysis_result')
    total_score = float(request.form.get('total_score'))
    eligibility = total_score >= 70  # Set 'eligible' jika skor >= 70

    # Simpan ke database
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Analysis_Results (cv_id, criteria_id, analysis_result, total_score, eligibility)
            VALUES (%s, %s, %s, %s, %s)
        """, (cv_id, criteria_id, analysis_result, total_score, eligibility))
        conn.commit()
        flash('Hasil analisis berhasil disimpan.', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        conn.close()

    return redirect(url_for('analysis'))

@app.route('/analysis_results')
@admin_required
def analysis_results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ar.id, cv.filename, kp.posisi, ar.total_score, ar.eligibility, ar.created_at
        FROM Analysis_Results ar
        JOIN CVs cv ON ar.cv_id = cv.id
        JOIN Kriteria_Penilaian kp ON ar.criteria_id = kp.id
        ORDER BY ar.created_at DESC
    """)
    results = cursor.fetchall()
    conn.close()

    return render_template('analysis_results.html', results=results)

@app.route('/analysis_result_detail/<int:result_id>')
@admin_required
def analysis_result_detail(result_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ar.*, cv.filename, kp.posisi
        FROM Analysis_Results ar
        JOIN CVs cv ON ar.cv_id = cv.id
        JOIN Kriteria_Penilaian kp ON ar.criteria_id = kp.id
        WHERE ar.id = %s
    """, (result_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        flash('Hasil analisis tidak ditemukan.', 'error')
        return redirect(url_for('analysis_results'))

    return render_template('analysis_result_detail.html', result=result)

@app.route('/delete_analysis_result/<int:result_id>', methods=['POST'])
@admin_required
def delete_analysis_result(result_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Analysis_Results WHERE id = %s", (result_id,))
        conn.commit()
        flash('Hasil analisis berhasil dihapus.', 'success')
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('analysis_results'))



# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
