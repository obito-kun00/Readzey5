-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 20, 2026 at 07:58 AM
-- Server version: 8.4.3
-- PHP Version: 8.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `readsmart`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int NOT NULL,
  `username` varchar(150) NOT NULL,
  `password` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'yash', 'pbkdf2:sha256:600000$dcNAmcbxBfPE2TSM$3c8fdde00e426e0f2228a6b3093ac2895a986ebc6cc32b8e83ed9806874f176c');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `price` float DEFAULT '0',
  `cover` varchar(255) DEFAULT NULL,
  `pdfs` varchar(255) DEFAULT NULL,
  `total_pages` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `price`, `cover`, `pdfs`, `total_pages`) VALUES
(2, 'shadows after midnight', 0, 'cover/Shadows After Midnight.jpg', 'pdfs/shadows after midnight.pdf', 11),
(3, 'The Shape of Her Silence', 0, 'cover/The Shape of Her Silence.jpg', 'pdfs/The Shape of Her Silence.pdf', 12),
(4, 'Exploring the Tapestry of Human Nature', 0, 'cover/Exploring the Tapestry of Human Nature.jpg', 'pdfs/Exploring the Tapestry of Human Nature.pdf', 11),
(5, 'Her Voice Was the Knife', 0, 'cover/Her-Voice-Was-the-Knife.jpg', 'pdfs/Her Voice Was the Knife.pdf', 6),
(6, 'Hypnosis and Love', 0, 'cover/Hypnosis and Love.jpg', 'pdfs/Hypnosis and Love.pdf', 15),
(7, 'Illusion and Simulation', 0, 'cover/Illusion and Simulation.jpg', 'pdfs/Illusion and Simulation.pdf', 8),
(8, 'The Heart of a Poet', 0, 'cover/The Heart of a Poe.jpg', 'pdfs/The Heart of a Poet.pdf', 6),
(9, 'limits of emotion', 0, 'cover/limits of emotion.jpg', 'pdfs/Limits of Emotion.pdf', 6);

-- --------------------------------------------------------

--
-- Table structure for table `contact_us`
--

CREATE TABLE `contact_us` (
  `user_id` int DEFAULT NULL,
  `user_email` varchar(150) NOT NULL,
  `problem` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `contact_us`
--

INSERT INTO `contact_us` (`user_id`, `user_email`, `problem`) VALUES
(1, 'aloneyash555@gmail.com', 'yes'),
(NULL, 'aloneyash555@gmail.com', 'g');

-- --------------------------------------------------------

--
-- Table structure for table `friend_requests`
--

CREATE TABLE `friend_requests` (
  `id` int NOT NULL,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `friend_requests`
--

INSERT INTO `friend_requests` (`id`, `sender_id`, `receiver_id`, `status`, `created_at`) VALUES
(1, 2, 3, 'accepted', '2026-04-19 07:04:35'),
(2, 7, 2, 'accepted', '2026-04-20 06:13:05');

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `user_id` int NOT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`user_id`, `profile_photo`, `created_at`) VALUES
(1, 'user_1_a82bafe92aeeaa9a73df064d2ff83537.jpg', '2026-03-19 10:34:12'),
(2, 'user_2_a82bafe92aeeaa9a73df064d2ff83537.jpg', '2026-04-19 07:02:08'),
(3, 'user_3_a82bafe92aeeaa9a73df064d2ff83537.jpg', '2026-04-19 07:03:50'),
(6, NULL, '2026-04-19 18:51:19');

-- --------------------------------------------------------

--
-- Table structure for table `reading_invites`
--

CREATE TABLE `reading_invites` (
  `id` int NOT NULL,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `book_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `reading_invites`
--

INSERT INTO `reading_invites` (`id`, `sender_id`, `receiver_id`, `book_id`, `status`, `created_at`) VALUES
(8, 3, 2, 2, 'pending', '2026-04-19 18:10:33'),
(9, 2, 3, 2, 'pending', '2026-04-20 07:41:33');

-- --------------------------------------------------------

--
-- Table structure for table `reading_progress`
--

CREATE TABLE `reading_progress` (
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `current_page` int DEFAULT '1',
  `total_pages` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `reading_progress`
--

INSERT INTO `reading_progress` (`user_id`, `book_id`, `current_page`, `total_pages`) VALUES
(1, 2, 9, 11),
(1, 3, 1, 12),
(1, 5, 2, 6),
(2, 2, 7, 11),
(3, 2, 1, 11),
(2, 3, 2, 12),
(3, 3, 3, 12),
(3, 8, 1, 6),
(6, 2, 1, 11),
(6, 6, 1, 15),
(3, 5, 1, 6);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `book_title` varchar(255) DEFAULT NULL,
  `review_text` text NOT NULL,
  `rating` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(256) NOT NULL,
  `is_verified` tinyint(1) DEFAULT '0',
  `verification_code` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'active',
  `reset_token` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `is_verified`, `verification_code`, `status`, `reset_token`) VALUES
(1, 'ok', 'aloneyash555@gmail.com', 'pbkdf2:sha256:600000$KSsgggTMoZ3Qxmd9$99cce9337a2f2e36ca75d54e892cba2bc7c4db5628c9c0326271a191266d1748', 1, NULL, 'active', NULL),
(2, 'love', 'yashsolanki8384@gmail.com', 'pbkdf2:sha256:600000$Z3CIUqqqwtADc0Le$2d640099b0a9b74a376967095cd91d079037440fb9f5bc555e2d565cb455cfa8', 1, NULL, 'active', NULL),
(3, 'yash', 'q@gmail.com', 'pbkdf2:sha256:600000$q0eKLuWv0WYILIdj$fea7375da5d4e5f44477c4a1651127665c7ee1d656d4bb5242f75054e715d97f', 1, NULL, 'active', NULL),
(4, 'yuy', 'yash@gmail.com', 'pbkdf2:sha256:600000$0FMCRRm4Tx7C90Vz$053de92d42193a89563be43a3c0949515f2fa75af28b916e4f60bb2f6e7564f2', 0, NULL, 'active', NULL),
(5, '12', '12@gmail.com', 'pbkdf2:sha256:600000$ZezeCc0jgTb9V58f$a005b2bcaa6c2ee2be84ff3cc5a83635737b5983be19a9106c1caab764ef8218', 0, NULL, 'active', NULL),
(6, '123', '123@gmail.com', 'pbkdf2:sha256:600000$OFL42vGf3jewAXdS$151726079048adacc8bd3f0a2b75615a2fceeed0fcf58601c497b2b189535326', 1, NULL, 'active', NULL),
(7, '1234', '1234@gmail.com', 'pbkdf2:sha256:600000$twEYUM00qmxlCWgF$24efa6726ce3584d5d81b25bef209761316aed91d109683af95c5e868907f07f', 0, NULL, 'active', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_achievements`
--

CREATE TABLE `user_achievements` (
  `user_id` int NOT NULL,
  `badge_name` varchar(100) NOT NULL,
  `badge_icon` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_activity`
--

CREATE TABLE `user_activity` (
  `user_id` int NOT NULL,
  `activity_type` varchar(100) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_activity`
--

INSERT INTO `user_activity` (`user_id`, `activity_type`, `description`, `created_at`) VALUES
(1, 'Account Created', 'Welcome to ReadSmart!', '2026-03-19 10:34:12'),
(2, 'Account Created', 'Welcome to ReadSmart!', '2026-04-19 07:02:08'),
(3, 'Account Created', 'Welcome to ReadSmart!', '2026-04-19 07:03:50'),
(6, 'Account Created', 'Welcome to ReadSmart!', '2026-04-19 18:51:19');

-- --------------------------------------------------------

--
-- Table structure for table `user_favorites`
--

CREATE TABLE `user_favorites` (
  `user_id` int NOT NULL,
  `book_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_favorites`
--

INSERT INTO `user_favorites` (`user_id`, `book_id`) VALUES
(1, 2),
(1, 8),
(1, 4),
(1, 5),
(1, 9),
(3, 3),
(2, 4),
(2, 5),
(3, 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact_us`
--
ALTER TABLE `contact_us`
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `friend_requests`
--
ALTER TABLE `friend_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`);

--
-- Indexes for table `profile`
--
ALTER TABLE `profile`
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `reading_invites`
--
ALTER TABLE `reading_invites`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `reading_progress`
--
ALTER TABLE `reading_progress`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_achievements`
--
ALTER TABLE `user_achievements`
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user_activity`
--
ALTER TABLE `user_activity`
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user_favorites`
--
ALTER TABLE `user_favorites`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `friend_requests`
--
ALTER TABLE `friend_requests`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `reading_invites`
--
ALTER TABLE `reading_invites`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `contact_us`
--
ALTER TABLE `contact_us`
  ADD CONSTRAINT `contact_us_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `friend_requests`
--
ALTER TABLE `friend_requests`
  ADD CONSTRAINT `friend_requests_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `friend_requests_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `profile`
--
ALTER TABLE `profile`
  ADD CONSTRAINT `profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `reading_invites`
--
ALTER TABLE `reading_invites`
  ADD CONSTRAINT `reading_invites_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `reading_invites_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `reading_invites_ibfk_3` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`);

--
-- Constraints for table `reading_progress`
--
ALTER TABLE `reading_progress`
  ADD CONSTRAINT `reading_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reading_progress_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user_achievements`
--
ALTER TABLE `user_achievements`
  ADD CONSTRAINT `user_achievements_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user_activity`
--
ALTER TABLE `user_activity`
  ADD CONSTRAINT `user_activity_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user_favorites`
--
ALTER TABLE `user_favorites`
  ADD CONSTRAINT `user_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_favorites_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
