-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 15 Jan 2025 pada 10.35
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
(4, 'CV_Cia_Thing.pdf', 'https://github.com/CiaThing\nCia Thing +6287782425144\nciathing488@gmail.com\nhttps://www.linkedin.com/in/cia-thing-824b482b9/\nData Science\nSaya adalah mahasiswa semester 6 di program studi Informatika dengan antusiasme tinggi dalam bidang\ndata science dan machine learning. Saya memiliki keinginan kuat untuk mempelajari hal-hal baru dan\nmengaplikasikan ilmu yang saya peroleh untuk memecahkan masalah nyata. Kombinasi dari keinginan\nbelajar, rasa ingin tahu, dan keterampilan teknis dalam machine learning memungkinkan saya untuk\nmengembangkan solusi inovatif dan efektif. Saya berkomitmen untuk terus mengembangkan pengetahuan\ndan keterampilan saya di bidang ini, serta berkontribusi dalam proyek-proyek yang berdampak positif.\nWork Experience\nMagang Entry Data Universitas Pembangunan Jaya\nKampus\nMenyalin data-data dari berbagai program studi di Universitas Pembangunan Jaya dengan\n2024-sekarang Excel.\nMenyalin data seperti CPL, CPMK, SCPMK, mata kuliah dari semester 1 sampai semester 8 dari\nberbagai program studi.\nMenginput data-data dari excel ke dalam sistem.\nMenginput data-data RPS, materi pembelajaran, pustaka pembelajaran pada setiap mata\nkuliah ke dalam sistem.\nEducation\nMahasiswa Informatika Universitas Pembangunan Jaya 2021-sekarang\nSMA jurusan Science SMAK 6 BPK PENABUR Jakarta 2018-2021\natau MIPA\nOrganization Experience\nAnggota KPPS TPS 239 Cengkareng Timur\nMembuat rincian pengeluaran dengan excel.\nJan 2024 - Feb 2024\nMempelajari dan menggunakan aplikasi SIREKAP.\nMenginput data seperti form jumlah suara ke aplikasi SIREKAP.\nRelevant Skills\nHard Skills Tools Soft Skills\nData Mining Python Critical Thinking\nVisualisasi data Javascript\nProblem Solving\nNormalisasi data MySQL\nCommunicative\nAnalisis data Tableau\nMachine Learning ( fokus metode regresi )\nStatistik\nCertificate\nData Analyst Mini Course - RevoU\nJun 2023 - Jul 2023'),
(5, 'Test.pdf', 'Juara PHP\nJuara Javascript\nBahasa Inggris\nBahasa Jepang\nToefl\nJLPT\nPHP\nJavascript');

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
(1, 'oajnhfdo', 'sma', 3, 'aslkd', 'jndsak', 'fdes', 'fsd'),
(2, 'lkdsnf', 'sma', 3, 'werwe, gfhfdg', '5647, tyru7r5', 'retfgdyjt, 456yhjt,jm, uykyu567', 'uyjt67, ytu78o, 432514, 809yuikjyt'),
(3, 'BackEnd Programmer', 's1', 3, 'PHP, Javascript, C', 'Bahasa Inggris, Bahasa Jepang', 'Toefl, JLPT', 'Juara PHP, Juara Javascript');

--
-- Indexes for dumped tables
--

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
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `cvs`
--
ALTER TABLE `cvs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `kriteria_penilaian`
--
ALTER TABLE `kriteria_penilaian`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
