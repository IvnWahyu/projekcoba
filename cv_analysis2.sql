-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 27 Apr 2025 pada 16.46
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cv_analysis`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `analysis_results`
--

CREATE TABLE `analysis_results` (
  `id` int(11) NOT NULL,
  `cv_id` int(11) NOT NULL,
  `criteria_id` int(11) NOT NULL,
  `analysis_result` text NOT NULL,
  `total_score` decimal(5,2) NOT NULL,
  `eligibility` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `cvs`
--

CREATE TABLE `cvs` (
  `id` int(11) NOT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `extracted_text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `cvs`
--

INSERT INTO `cvs` (`id`, `filename`, `extracted_text`) VALUES
(1, 'CV_Cia_Thing.pdf', 'https://github.com/CiaThing\nCia Thing +6287782425144\nciathing488@gmail.com\nhttps://www.linkedin.com/in/cia-thing-824b482b9/\nData Science\nSaya adalah mahasiswa semester 6 di program studi Informatika dengan antusiasme tinggi dalam bidang\ndata science dan machine learning. Saya memiliki keinginan kuat untuk mempelajari hal-hal baru dan\nmengaplikasikan ilmu yang saya peroleh untuk memecahkan masalah nyata. Kombinasi dari keinginan\nbelajar, rasa ingin tahu, dan keterampilan teknis dalam machine learning memungkinkan saya untuk\nmengembangkan solusi inovatif dan efektif. Saya berkomitmen untuk terus mengembangkan pengetahuan\ndan keterampilan saya di bidang ini, serta berkontribusi dalam proyek-proyek yang berdampak positif.\nWork Experience\nMagang Entry Data Universitas Pembangunan Jaya\nKampus\nMenyalin data-data dari berbagai program studi di Universitas Pembangunan Jaya dengan\n2024-sekarang Excel.\nMenyalin data seperti CPL, CPMK, SCPMK, mata kuliah dari semester 1 sampai semester 8 dari\nberbagai program studi.\nMenginput data-data dari excel ke dalam sistem.\nMenginput data-data RPS, materi pembelajaran, pustaka pembelajaran pada setiap mata\nkuliah ke dalam sistem.\nEducation\nMahasiswa Informatika Universitas Pembangunan Jaya 2021-sekarang\nSMA jurusan Science SMAK 6 BPK PENABUR Jakarta 2018-2021\natau MIPA\nOrganization Experience\nAnggota KPPS TPS 239 Cengkareng Timur\nMembuat rincian pengeluaran dengan excel.\nJan 2024 - Feb 2024\nMempelajari dan menggunakan aplikasi SIREKAP.\nMenginput data seperti form jumlah suara ke aplikasi SIREKAP.\nRelevant Skills\nHard Skills Tools Soft Skills\nData Mining Python Critical Thinking\nVisualisasi data Javascript\nProblem Solving\nNormalisasi data MySQL\nCommunicative\nAnalisis data Tableau\nMachine Learning ( fokus metode regresi )\nStatistik\nCertificate\nData Analyst Mini Course - RevoU\nJun 2023 - Jul 2023'),
(5, 'Test.pdf', 'Juara PHP\nJuara Javascript\nBahasa Inggris\nBahasa Jepang\nToefl\nJLPT\nPHP\nJavascript'),
(7, 'Test_2.pdf', 'Juara PHP\nJuara Javascript\nBahasa Jepang\nToefl\nPHP\nJavascript'),
(10, 'CV-Ivan_Wahyu_Putratama.pdf', 'Ivan Wahyu Putratama\nivanwahyu2813@gmail.com | 085781029976\nSaya adalah mahasiswa semester 6 jurusan Informatika yang bersemangat untuk terus mengembangkan\nkemampuan saya. Saya telah memperoleh pengalaman dalam desain UI/UX dan pengembangan website. Saya\nmemiliki kemampuan adaptasi yang baik, dan mampu bekerja dalam tim. Saya sangat tertarik pada teknologi\ndan desain, serta selalu mencari kesempatan untuk mempelajari hal-hal baru di bidang ini.\nEducation\nSMAN 10 Kota Depok\nIPA • 2018 - 2021\nUniversitas Pembangunan Jaya\nInformatika • 2021 - Sekarang\nOrganization Experience\nForkanite • Universitas Pembangunan Jaya\n2024 | Anggota Divisi Publikasi, Dokumentasi dan Desain (PDD)\nSkills\nSo\0ware Pemrograman Bahasa Pemrograman Lainnya\nVisual Studio Code HTML Figma\nPycharm PHP Microsoft Word\nGoogle Colab Javascript Microsoft Excel\nPython\nCourses\nBelajar Dasar Pemrograman Web • Dicoding\n2023\nMencakup dasar-dasar HTML dan CSS, pengenalan dan pendalaman HTML dan CSS, serta teknik\nlayout responsif dengan Flexbox. Total 41 jam pembelajaran yang mencakup ujian akhir dan proyek\nakhir pembuatan halaman website.\nIntroduction to Networks • Cisco\n2023\nMencakup kon\0gurasi switch dan router untuk memberikan akses ke sumber daya jaringan lokal\ndan remote, pengalamatan IPv4 dan IPv6, serta troubleshooting jaringan kecil. Juga mencakup\npraktik terbaik keamanan jaringan dan mendukung operasi Ethernet di jaringan switch.');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kriteria_penilaian`
--

CREATE TABLE `kriteria_penilaian` (
  `id` int(11) NOT NULL,
  `posisi` varchar(255) DEFAULT NULL,
  `pendidikan_minimum` varchar(100) DEFAULT NULL,
  `pengalaman_minimum` int(11) DEFAULT NULL,
  `keterampilan` varchar(255) DEFAULT NULL,
  `bahasa` varchar(255) DEFAULT NULL,
  `sertifikasi` text DEFAULT NULL,
  `penghargaan_prestasi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kriteria_penilaian`
--

INSERT INTO `kriteria_penilaian` (`id`, `posisi`, `pendidikan_minimum`, `pengalaman_minimum`, `keterampilan`, `bahasa`, `sertifikasi`, `penghargaan_prestasi`) VALUES
(2, 'lkdsnf', 'sma', 3, 'werwe, gfhfdg', '5647, tyru7r5', 'retfgdyjt, 456yhjt,jm, uykyu567', 'uyjt67, ytu78o, 432514, 809yuikjyt'),
(3, 'BackEnd Programmer', 's1', 3, 'PHP, Javascript, C', 'Bahasa Inggris, Bahasa Jepang', 'Toefl, JLPT', 'Juara PHP, Juara Javascript');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `last_login` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `is_admin`, `created_at`, `last_login`) VALUES
(1, 'ivan', 'pbkdf2:sha256:600000$CAEmm9uwwrw0xnBM$962974dd252bb7d237f469affe3205d55204f0a2b0f0a519fd364b369a6ba446', 0, '2025-01-13 16:21:36', '2025-01-28 19:14:43'),
(2, 'admin', 'pbkdf2:sha256:600000$AMxTATqsrYxPuKOO$7fe54047aad083701f10dbb2fd86e9e81956a6fdd0586d32c5c522a19a758144', 1, '2025-01-13 11:16:25', '2025-01-31 13:19:33'),
(3, 'budi', 'pbkdf2:sha256:600000$sQnGCEfaZ0ky0W4a$8df06a1c006d1f178cd597a37cb37e65a108aef89bc8666e902bdbc8bee46a7b', 0, '2025-01-22 16:59:48', '2025-01-24 14:16:19');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `analysis_results`
--
ALTER TABLE `analysis_results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cv_id` (`cv_id`),
  ADD KEY `criteria_id` (`criteria_id`);

--
-- Indeks untuk tabel `cvs`
--
ALTER TABLE `cvs`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `kriteria_penilaian`
--
ALTER TABLE `kriteria_penilaian`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `analysis_results`
--
ALTER TABLE `analysis_results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `cvs`
--
ALTER TABLE `cvs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `kriteria_penilaian`
--
ALTER TABLE `kriteria_penilaian`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `analysis_results`
--
ALTER TABLE `analysis_results`
  ADD CONSTRAINT `analysis_results_ibfk_1` FOREIGN KEY (`cv_id`) REFERENCES `cvs` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `analysis_results_ibfk_2` FOREIGN KEY (`criteria_id`) REFERENCES `kriteria_penilaian` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
