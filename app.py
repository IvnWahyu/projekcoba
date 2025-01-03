from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
import pdfplumber  # Impor untuk mengekstrak teks dari PDF
from werkzeug.utils import secure_filename  # Impor untuk menangani nama file yang aman

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
    'database': 'cv_analysis'
}

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Halaman Dashboard
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM CVs")  # Menghitung jumlah CV yang diunggah
    result = cursor.fetchone()
    total_cvs = result[0]
    conn.close()
    return render_template('index.html', total_cvs=total_cvs)

# Halaman Pengaturan Kriteria
@app.route('/criteria', methods=['GET', 'POST'])
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
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Halaman Daftar CV yang Telah Diunggah
@app.route('/cv_list')
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
def analysis():
    # Ambil semua CV dari database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename FROM CVs")  # Ambil ID dan nama file dari CV yang diunggah
    cvs = cursor.fetchall()

    # Ambil semua kriteria penilaian (posisi) dari database
    cursor.execute("SELECT id, posisi FROM Kriteria_Penilaian")  # Ambil semua posisi
    criteria_positions = cursor.fetchall()
    conn.close()

    # Jika ada pilihan CV dan kriteria, lakukan analisis
    analysis_result = None
    analysis_scores = None
    cv_text = None
    selected_criteria = None

    if request.method == 'POST':
        cv_id = request.form.get('cv_id')
        criteria_id = request.form.get('criteria_id')  # Ambil ID kriteria yang dipilih

        if cv_id and criteria_id:
            # Ambil CV dan kriteria yang dipilih
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CVs WHERE id = %s", (cv_id,))
            cv = cursor.fetchone()

            cursor.execute("SELECT * FROM Kriteria_Penilaian WHERE id = %s", (criteria_id,))
            criteria = cursor.fetchone()
            conn.close()

            if not cv or not criteria:
                flash('CV atau Kriteria tidak ditemukan', 'error')
                return redirect(url_for('analysis'))

            # Ambil hasil analisis berdasarkan CV dan kriteria yang dipilih
            analysis_result = analyze_text(cv[2], criteria)  # cv[2] berisi teks ekstraksi CV
            analysis_scores = analyze_scores(cv[2], criteria)
            cv_text = cv[2]  # Ambil teks ekstraksi CV
            selected_criteria = criteria  # Menyimpan kriteria yang dipilih

            return render_template('analyze_cv.html', cv=cv, analysis_result=analysis_result, 
                                   analysis_scores=analysis_scores, selected_criteria=selected_criteria)

    return render_template('analysis.html', cvs=cvs, criteria_positions=criteria_positions)

# Fungsi untuk menganalisis teks dan memberikan skor berdasarkan kriteria
def analyze_text(extracted_text, criteria):
    # Analisis sederhana: menghitung jumlah kata dalam teks ekstraksi
    word_count = len(extracted_text.split())
    return f"Jumlah kata dalam teks: {word_count} kata"

# Fungsi untuk menganalisis skor berdasarkan kriteria
def analyze_scores(extracted_text, criteria):
    # Logika analisis sederhana berdasarkan kriteria yang sudah disimpan
    education_score = 0
    experience_score = 0
    skills_score = 0
    language_score = 0

    # Skor Pendidikan
    if criteria[1] in extracted_text:  # criteria[1] berisi pendidikan yang dipilih (misalnya 'S1')
        education_score = 20  # Atur skor berdasarkan kecocokan

    # Skor Pengalaman
    if str(criteria[2]) in extracted_text:  # criteria[2] berisi pengalaman minimum (misalnya '3 tahun')
        experience_score = 20  # Skor jika ditemukan pengalaman yang sesuai

    # Skor Keterampilan (Menyesuaikan dengan keterampilan yang dipilih)
    skills_keywords = []
    if isinstance(criteria[3], str):  # Pastikan criteria[3] adalah string
        skills_keywords = criteria[3].split(",")  # Misalnya keterampilan yang dipilih adalah 'Python, Java'
    for skill in skills_keywords:
        if skill.strip().lower() in extracted_text.lower():
            skills_score += 5  # Beri skor per keterampilan yang cocok
    
    # Skor Bahasa
    languages = criteria[4].split(",")  # Misalnya 'Bahasa Inggris, Bahasa Jepang'
    for language in languages:
        if language.strip().lower() in extracted_text.lower():
            language_score += 5  # Beri skor per bahasa yang cocok

    # Total skor
    total_score = education_score + experience_score + skills_score + language_score

    return {
        'education_score': education_score,
        'experience_score': experience_score,
        'skills_score': skills_score,
        'language_score': language_score,
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


# Menjalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)

