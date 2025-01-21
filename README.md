Untuk database

CREATE TABLE `cvs` (
  `id` int(11) NOT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `extracted_text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE `kriteria_penilaian` (
  `id` int(11) NOT NULL,
  `posisi` varchar(255) DEFAULT NULL,
  `pendidikan_minimum` varchar(100) DEFAULT NULL,
  `pengalaman_minimum` int(11) DEFAULT NULL,
  `keterampilan` text DEFAULT NULL,
  `bahasa` varchar(255) DEFAULT NULL,
  `sertifikasi` text DEFAULT NULL,
  `penghargaan_prestasi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
