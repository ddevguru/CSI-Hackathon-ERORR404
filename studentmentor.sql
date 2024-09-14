-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 14, 2024 at 02:20 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `studentmentor`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat_messages`
--

CREATE TABLE `chat_messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` int(11) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `mentor_id` int(11) DEFAULT NULL,
  `course_description` varchar(255) NOT NULL,
  `course_duration` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `course_name`, `mentor_id`, `course_description`, `course_duration`) VALUES
(1, 'HTML', NULL, 'Learn html basics using this free of cost course ', '2 weeks'),
(2, 'CSS Basics', NULL, 'Learn Basics CSS', '1 week'),
(3, 'HTML Intermediate ', NULL, 'Learn Html intermediate only after you have completed html basics', '2 weeks');

-- --------------------------------------------------------

--
-- Table structure for table `course_requests`
--

CREATE TABLE `course_requests` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_requests`
--

INSERT INTO `course_requests` (`id`, `student_id`, `course_id`, `status`) VALUES
(1, 2, 1, 'approved'),
(2, 2, 2, 'approved'),
(3, 2, 3, 'approved'),
(4, 2, 1, 'approved');

-- --------------------------------------------------------

--
-- Table structure for table `join_requests`
--

CREATE TABLE `join_requests` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `mentor_id` int(11) NOT NULL,
  `reason` text DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `join_requests`
--

INSERT INTO `join_requests` (`id`, `student_id`, `mentor_id`, `reason`, `status`, `created_at`) VALUES
(1, 2, 3, 'I want guideness from you', 'approved', '2024-09-13 08:11:29');

-- --------------------------------------------------------

--
-- Table structure for table `mentor_students`
--

CREATE TABLE `mentor_students` (
  `id` int(11) NOT NULL,
  `mentor_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `sender_id`, `recipient_id`, `content`, `timestamp`) VALUES
(1, 2, 3, 'hello Sir', '2024-09-14 11:58:00'),
(2, 2, 3, 'hello Sir', '2024-09-14 12:22:44'),
(3, 2, 3, 'Hii', '2024-09-14 13:46:14'),
(4, 2, 3, 'Hii', '2024-09-14 14:25:29');

-- --------------------------------------------------------

--
-- Table structure for table `study_materials`
--

CREATE TABLE `study_materials` (
  `id` int(11) NOT NULL,
  `material_title` varchar(255) DEFAULT NULL,
  `material_link` varchar(255) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `study_materials`
--

INSERT INTO `study_materials` (`id`, `material_title`, `material_link`, `course_id`) VALUES
(1, 'HTML Basics', '/uploads/Gmail%20-%20RE_%5BCASE%2010189426382%5D%20Brand%20Qualification%20Application%20for%20IMLIS%20-%20IN.pdf', NULL),
(2, 'HTML Basics', '/uploads/Gmail%20-%20RE_%5BCASE%2010189426382%5D%20Brand%20Qualification%20Application%20for%20IMLIS%20-%20IN.pdf', NULL),
(3, 'HTML Basics', '/uploads/Gmail%20-%20RE_%5BCASE%2010189426382%5D%20Brand%20Qualification%20Application%20for%20IMLIS%20-%20IN.pdf', NULL),
(4, 'HTML Basics', '/uploads/Gmail%20-%20RE_%5BCASE%2010189426382%5D%20Brand%20Qualification%20Application%20for%20IMLIS%20-%20IN.pdf', NULL),
(5, 'HTML Basics', '/uploads/Vansh%20Updated%20resume%202024%20(4).pdf', NULL),
(6, 'DBMS', '/uploads/admin-dashboard-panel-html-css-javascript.zip', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','mentor','student') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `approved` tinyint(1) DEFAULT 0,
  `bio` text DEFAULT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  `number` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `created_at`, `approved`, `bio`, `profile_photo`, `number`) VALUES
(1, 'Deepak Mishra', 'deepakm778@gmail.com', 'scrypt:32768:8:1$0YvtSUUPnGWCzADi$429e653b79bcea1eff6b558b3e318a23358b58bafa8fbb7985e3b40576043c27aa64d14980e792b0cf7b7689b8e560798b728c846c643c4a1ac37ac3560dbb62', 'admin', '2024-09-13 04:57:26', 1, NULL, NULL, ''),
(2, 'Deepak ', '121deepak2104@sjcem.edu.in', 'scrypt:32768:8:1$8wAJgWi74xxmm8vT$43c8feb5a2d8250737345721b85e23a1dfbb884adc45ac96b6fe1da8bc3f54b6dfdf7b5d572285baa21fe8f56216c65150054c597974b4ecb41cb45fbd8144b8', 'student', '2024-09-13 04:59:26', 1, NULL, NULL, ''),
(3, 'Yash Dubey', 'yashd@gmail.com', 'scrypt:32768:8:1$EicHqzYxQreVmubM$48b69d285b6f7d0731237f4ae450c495d80a22d31d0bfab81aaafaafcee09b4c3ceacfce7860dead6dbdabd316c1cfd3091758746c4d5e223c97ccb5a9a6af69', 'mentor', '2024-09-13 05:55:25', 1, 'Full stack Developer', 'IMG_20220522_094140_1.jpg', '+918208257509');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mentor_id` (`mentor_id`);

--
-- Indexes for table `course_requests`
--
ALTER TABLE `course_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `join_requests`
--
ALTER TABLE `join_requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `mentor_id` (`mentor_id`);

--
-- Indexes for table `mentor_students`
--
ALTER TABLE `mentor_students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mentor_id` (`mentor_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `recipient_id` (`recipient_id`);

--
-- Indexes for table `study_materials`
--
ALTER TABLE `study_materials`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chat_messages`
--
ALTER TABLE `chat_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `course_requests`
--
ALTER TABLE `course_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `join_requests`
--
ALTER TABLE `join_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `mentor_students`
--
ALTER TABLE `mentor_students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `study_materials`
--
ALTER TABLE `study_materials`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `chat_messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`mentor_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `course_requests`
--
ALTER TABLE `course_requests`
  ADD CONSTRAINT `course_requests_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `course_requests_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `join_requests`
--
ALTER TABLE `join_requests`
  ADD CONSTRAINT `join_requests_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `join_requests_ibfk_2` FOREIGN KEY (`mentor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `mentor_students`
--
ALTER TABLE `mentor_students`
  ADD CONSTRAINT `mentor_students_ibfk_1` FOREIGN KEY (`mentor_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `mentor_students_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`recipient_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `study_materials`
--
ALTER TABLE `study_materials`
  ADD CONSTRAINT `study_materials_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
