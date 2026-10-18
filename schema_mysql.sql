CREATE DATABASE IF NOT EXISTS `scholartrack_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `scholartrack_db`;

CREATE TABLE IF NOT EXISTS `students` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `roll_number` VARCHAR(50) NOT NULL UNIQUE,
  `full_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(150) UNIQUE,
  `department` VARCHAR(100) NOT NULL,
  `admission_year` INT NOT NULL,
  `current_status` ENUM('Active', 'Graduated', 'On Hold', 'Discontinued') NOT NULL DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS `school_records` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `level` ENUM('SSC', 'HSC') NOT NULL,
  `board` VARCHAR(100),
  `passing_year` INT NOT NULL,
  `marks_obtained` DOUBLE NOT NULL,
  `marks_total` DOUBLE NOT NULL,
  `percentage` DOUBLE NOT NULL,
  UNIQUE KEY `uk_student_level` (`student_id`, `level`),
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `semester_results` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `semester_number` INT NOT NULL,
  `academic_year` VARCHAR(20) NOT NULL,
  `sgpa` DOUBLE NOT NULL,
  `cgpa` DOUBLE NOT NULL,
  `result_status` ENUM('Pass', 'ATKT', 'Fail', 'Pending') NOT NULL,
  `backlog_count` INT NOT NULL DEFAULT 0,
  `is_gap_after` TINYINT(1) NOT NULL DEFAULT 0,
  UNIQUE KEY `uk_student_sem` (`student_id`, `semester_number`),
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `subjects` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `subject_code` VARCHAR(50) NOT NULL UNIQUE,
  `subject_name` VARCHAR(150) NOT NULL,
  `subject_type` ENUM('Theory', 'Lab') NOT NULL,
  `credits` DOUBLE NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS `subject_marks` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `semester_result_id` INT NOT NULL,
  `subject_id` INT NOT NULL,
  `marks_obtained` DOUBLE NOT NULL,
  `marks_total` DOUBLE NOT NULL,
  `passing_marks` DOUBLE NOT NULL,
  `component` ENUM('Internal', 'External', 'Practical', 'Final') NOT NULL DEFAULT 'Final',
  UNIQUE KEY `uk_sem_sub` (`semester_result_id`, `subject_id`),
  FOREIGN KEY (`semester_result_id`) REFERENCES `semester_results`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`subject_id`) REFERENCES `subjects`(`id`) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `attendance` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `subject_id` INT NOT NULL,
  `academic_year` VARCHAR(20) NOT NULL,
  `semester_number` INT NOT NULL,
  `classes_held` INT NOT NULL,
  `classes_attended` INT NOT NULL,
  UNIQUE KEY `uk_att` (`student_id`, `subject_id`, `academic_year`, `semester_number`),
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`subject_id`) REFERENCES `subjects`(`id`) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `gap_years` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `start_year` INT NOT NULL,
  `end_year` INT NOT NULL,
  `reason_category` ENUM('Academic', 'Medical', 'Personal', 'Other') NOT NULL,
  `notes` TEXT,
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `activities` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `activity_type` ENUM('Technical', 'Co-curricular', 'Extra-curricular') NOT NULL,
  `organization` VARCHAR(150),
  `activity_date` DATE,
  `description` TEXT,
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `seminars` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `seminar_scope` ENUM('Internal', 'External') NOT NULL,
  `organizer` VARCHAR(150),
  `seminar_date` DATE,
  `certificate_url` VARCHAR(500),
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `certificates` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `issuer` VARCHAR(150) NOT NULL,
  `category` ENUM('Course', 'Hackathon', 'Internship', 'Achievement', 'Seminar', 'Other') NOT NULL,
  `issue_date` DATE,
  `credential_url` VARCHAR(500),
  `notes` TEXT,
  FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
);
