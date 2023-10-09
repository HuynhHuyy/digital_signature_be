-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 30, 2023 at 07:58 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cntt2`
--
CREATE DATABASE IF NOT EXISTS `cntt2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `cntt2`;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add admin accounts', 7, 'add_adminaccounts'),
(26, 'Can change admin accounts', 7, 'change_adminaccounts'),
(27, 'Can delete admin accounts', 7, 'delete_adminaccounts'),
(28, 'Can view admin accounts', 7, 'view_adminaccounts'),
(29, 'Can add application', 8, 'add_application'),
(30, 'Can change application', 8, 'change_application'),
(31, 'Can delete application', 8, 'delete_application'),
(32, 'Can view application', 8, 'view_application'),
(33, 'Can add departments', 9, 'add_departments'),
(34, 'Can change departments', 9, 'change_departments'),
(35, 'Can delete departments', 9, 'delete_departments'),
(36, 'Can view departments', 9, 'view_departments'),
(37, 'Can add process', 10, 'add_process'),
(38, 'Can change process', 10, 'change_process'),
(39, 'Can delete process', 10, 'delete_process'),
(40, 'Can view process', 10, 'view_process'),
(41, 'Can add role', 11, 'add_role'),
(42, 'Can change role', 11, 'change_role'),
(43, 'Can delete role', 11, 'delete_role'),
(44, 'Can view role', 11, 'view_role'),
(45, 'Can add step', 12, 'add_step'),
(46, 'Can change step', 12, 'change_step'),
(47, 'Can delete step', 12, 'delete_step'),
(48, 'Can view step', 12, 'view_step'),
(49, 'Can add signature', 13, 'add_signature'),
(50, 'Can change signature', 13, 'change_signature'),
(51, 'Can delete signature', 13, 'delete_signature'),
(52, 'Can view signature', 13, 'view_signature'),
(53, 'Can add receiver application', 14, 'add_receiverapplication'),
(54, 'Can change receiver application', 14, 'change_receiverapplication'),
(55, 'Can delete receiver application', 14, 'delete_receiverapplication'),
(56, 'Can view receiver application', 14, 'view_receiverapplication'),
(57, 'Can add files', 15, 'add_files'),
(58, 'Can change files', 15, 'change_files'),
(59, 'Can delete files', 15, 'delete_files'),
(60, 'Can view files', 15, 'view_files');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(7, 'tdtu_cntt2', 'adminaccounts'),
(8, 'tdtu_cntt2', 'application'),
(9, 'tdtu_cntt2', 'departments'),
(15, 'tdtu_cntt2', 'files'),
(10, 'tdtu_cntt2', 'process'),
(14, 'tdtu_cntt2', 'receiverapplication'),
(11, 'tdtu_cntt2', 'role'),
(13, 'tdtu_cntt2', 'signature'),
(12, 'tdtu_cntt2', 'step'),
(6, 'tdtu_cntt2', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'tdtu_cntt2', '0001_initial', '2023-08-30 05:00:57.419276'),
(2, 'contenttypes', '0001_initial', '2023-08-30 05:00:57.573052'),
(3, 'admin', '0001_initial', '2023-08-30 05:00:57.692827'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-08-30 05:00:57.701353'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-08-30 05:00:57.709876'),
(6, 'contenttypes', '0002_remove_content_type_name', '2023-08-30 05:00:57.769277'),
(7, 'auth', '0001_initial', '2023-08-30 05:00:57.999795'),
(8, 'auth', '0002_alter_permission_name_max_length', '2023-08-30 05:00:58.054359'),
(9, 'auth', '0003_alter_user_email_max_length', '2023-08-30 05:00:58.060894'),
(10, 'auth', '0004_alter_user_username_opts', '2023-08-30 05:00:58.066426'),
(11, 'auth', '0005_alter_user_last_login_null', '2023-08-30 05:00:58.072644'),
(12, 'auth', '0006_require_contenttypes_0002', '2023-08-30 05:00:58.076643'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2023-08-30 05:00:58.084646'),
(14, 'auth', '0008_alter_user_username_max_length', '2023-08-30 05:00:58.090162'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2023-08-30 05:00:58.096171'),
(16, 'auth', '0010_alter_group_name_max_length', '2023-08-30 05:00:58.117315'),
(17, 'auth', '0011_update_proxy_permissions', '2023-08-30 05:00:58.128537'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2023-08-30 05:00:58.134527'),
(19, 'sessions', '0001_initial', '2023-08-30 05:00:58.166781');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_adminaccounts`
--

CREATE TABLE `tdtu_cntt2_adminaccounts` (
  `id` bigint(20) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` longtext NOT NULL,
  `last_login` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tdtu_cntt2_adminaccounts`
--

INSERT INTO `tdtu_cntt2_adminaccounts` (`id`, `username`, `password`, `last_login`) VALUES
(1, 'admin', 'pbkdf2_sha256$600000$UXGRbsQTKqaYZ3vtf1qhqj$f4i6dLSg5tbc4AQ6F7g4SlkJ0+8LQmk9oo4zzW1xScI=', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_application`
--

CREATE TABLE `tdtu_cntt2_application` (
  `id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `status` int(11) NOT NULL,
  `delete_by_sender` tinyint(1) NOT NULL,
  `pdf_content` longtext DEFAULT NULL,
  `is_public` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `file_id_id` bigint(20) DEFAULT NULL,
  `process_id_id` bigint(20) DEFAULT NULL,
  `sender_id_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_departments`
--

CREATE TABLE `tdtu_cntt2_departments` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tdtu_cntt2_departments`
--

INSERT INTO `tdtu_cntt2_departments` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES
(1, 'Human Resource', 'Manager: 1; Staff: 2; Internship: 2', '2023-08-30 05:06:04.788645', '2023-08-30 05:06:04.788645'),
(2, 'Sales', 'Manager: 1; Staff: 2; Internship: 2', '2023-08-30 05:06:15.743616', '2023-08-30 05:06:15.743616'),
(3, 'Product Development', 'Manager: 1; Staff: 2; Internship: 2', '2023-08-30 05:06:37.594207', '2023-08-30 05:06:37.594207'),
(4, 'Accounting', 'Manager: 1; Staff: 2; Internship: 2', '2023-08-30 05:07:44.255997', '2023-08-30 05:07:44.255997'),
(5, 'Finance', 'Manager: 1; Staff: 2; Internship: 2', '2023-08-30 05:08:02.125549', '2023-08-30 05:08:02.125549');

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_files`
--

CREATE TABLE `tdtu_cntt2_files` (
  `id` bigint(20) NOT NULL,
  `name` longtext NOT NULL,
  `file` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_process`
--

CREATE TABLE `tdtu_cntt2_process` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tdtu_cntt2_process`
--

INSERT INTO `tdtu_cntt2_process` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES
(1, 'Offboarding Process', 'Offboarding Process for all department', '2023-08-30 05:48:08.324984', '2023-08-30 05:48:08.324984'),
(2, 'Salary increase process', 'Salary increase process for all department', '2023-08-30 05:48:55.875108', '2023-08-30 05:48:55.875108');

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_receiverapplication`
--

CREATE TABLE `tdtu_cntt2_receiverapplication` (
  `id` bigint(20) NOT NULL,
  `status` int(11) NOT NULL,
  `delete` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `application_id_id` bigint(20) DEFAULT NULL,
  `user_receiver_id_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_role`
--

CREATE TABLE `tdtu_cntt2_role` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `department_id_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tdtu_cntt2_role`
--

INSERT INTO `tdtu_cntt2_role` (`id`, `name`, `description`, `created_at`, `updated_at`, `department_id_id`) VALUES
(1, 'Manager', 'Human Resource Department\'s manager', '2023-08-30 05:10:19.797498', '2023-08-30 05:10:19.797498', 1),
(2, 'Manager', 'Sales Department\'s manager', '2023-08-30 05:10:37.159493', '2023-08-30 05:10:37.159493', 2),
(3, 'Manager', 'Product Development Department\'s manager', '2023-08-30 05:12:05.952090', '2023-08-30 05:12:05.952595', 3),
(4, 'Manager', 'Accounting Department\'s manager', '2023-08-30 05:12:23.755109', '2023-08-30 05:12:23.755109', 4),
(5, 'Manager', 'Finance Department\'s manager', '2023-08-30 05:12:38.339304', '2023-08-30 05:12:38.339304', 5),
(6, 'Staff', 'Human Resource Department\'s staff', '2023-08-30 05:14:51.434606', '2023-08-30 05:14:51.434606', 1),
(7, 'Staff', 'Sales Department\'s staff', '2023-08-30 05:15:02.629438', '2023-08-30 05:15:02.629438', 2),
(8, 'Staff', 'Product Development Department\'s staff', '2023-08-30 05:15:43.520058', '2023-08-30 05:15:43.520058', 3),
(9, 'Staff', 'Accounting Department\'s staff', '2023-08-30 05:16:01.372209', '2023-08-30 05:16:01.372209', 4),
(10, 'Staff', 'Finance Department\'s staff', '2023-08-30 05:16:15.197679', '2023-08-30 05:16:15.197679', 5),
(11, 'Internship', 'Human Resource Department\'s internship', '2023-08-30 05:17:05.389755', '2023-08-30 05:17:05.389755', 1),
(12, 'Internship', 'Sales Department\'s internship', '2023-08-30 05:17:26.103508', '2023-08-30 05:17:26.103508', 2),
(13, 'Internship', 'Product Development Department\'s internship', '2023-08-30 05:17:45.191019', '2023-08-30 05:17:45.191019', 3),
(14, 'Internship', 'Accounting Department\'s internship', '2023-08-30 05:17:58.898197', '2023-08-30 05:17:58.898197', 4),
(15, 'Internship', 'Finance Department\'s internship', '2023-08-30 05:18:16.311265', '2023-08-30 05:18:16.311265', 5);

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_signature`
--

CREATE TABLE `tdtu_cntt2_signature` (
  `id` bigint(20) NOT NULL,
  `signature` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_step`
--

CREATE TABLE `tdtu_cntt2_step` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `department_id_id` bigint(20) DEFAULT NULL,
  `process_id_id` bigint(20) DEFAULT NULL,
  `role_id_id` bigint(20) DEFAULT NULL,
  `user_id_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tdtu_cntt2_step`
--

INSERT INTO `tdtu_cntt2_step` (`id`, `name`, `created_at`, `updated_at`, `department_id_id`, `process_id_id`, `role_id_id`, `user_id_id`) VALUES
(1, 'Step1', '2023-08-30 05:49:18.260824', '2023-08-30 05:49:18.260824', 1, 1, 1, 1),
(2, 'Step1', '2023-08-30 05:49:37.664307', '2023-08-30 05:49:37.664307', 4, 2, 4, 4),
(3, 'Step2', '2023-08-30 05:49:51.155325', '2023-08-30 05:49:51.155325', 5, 2, 5, 5);

-- --------------------------------------------------------

--
-- Table structure for table `tdtu_cntt2_user`
--

CREATE TABLE `tdtu_cntt2_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `full_name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `private_key` longtext DEFAULT NULL,
  `public_key` longtext DEFAULT NULL,
  `certificate` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `department_id_id` bigint(20) DEFAULT NULL,
  `role_id_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tdtu_cntt2_user`
--

INSERT INTO `tdtu_cntt2_user` (`id`, `password`, `last_login`, `full_name`, `username`, `is_active`, `private_key`, `public_key`, `certificate`, `created_at`, `updated_at`, `department_id_id`, `role_id_id`) VALUES
(1, 'managerA1', NULL, 'Acacia Alexander', 'managerA1', 0, 'bf2f8065', 'bf2f8065', 'bf2f8065', '2023-08-30 05:20:28.733875', '2023-08-30 05:20:28.736886', 1, 1),
(2, 'managerA2', NULL, 'Acacia Abner', 'managerA2', 0, '8a2f6c5f', '8a2f6c5f', '8a2f6c5f', '2023-08-30 05:22:24.369955', '2023-08-30 05:22:24.371953', 2, 2),
(3, 'managerA3', NULL, 'Adelaide Aaron', 'managerA3', 0, '3d823b34', '3d823b34', '3d823b34', '2023-08-30 05:23:03.731800', '2023-08-30 05:23:03.732812', 3, 3),
(4, 'managerA4', NULL, 'Agatha Abhaya', 'managerA4', 0, '5232b979', '5232b979', '5232b979', '2023-08-30 05:23:27.422072', '2023-08-30 05:23:27.425067', 4, 4),
(5, 'managerA5', NULL, 'Agnes Adonis', 'managerA5', 0, 'ab524953', 'ab524953', 'ab524953', '2023-08-30 05:23:50.093888', '2023-08-30 05:23:50.095893', 5, 5),
(6, 'staffB1', NULL, 'Bernice Alger', 'staffB1', 0, 'b5dfec0d', 'b5dfec0d', 'b5dfec0d', '2023-08-30 05:25:12.452834', '2023-08-30 05:25:12.455834', 1, 6),
(7, 'staffB2', NULL, 'Bertha Andrea', 'staffB2', 0, '2516552c', '2516552c', '2516552c', '2023-08-30 05:30:52.569947', '2023-08-30 05:30:52.572934', 1, 6),
(8, 'staffB3', NULL, 'Blanche Andrew', 'staffB3', 0, '3012f33b', '3012f33b', '3012f33b', '2023-08-30 05:31:32.486418', '2023-08-30 05:31:32.488412', 2, 7),
(9, 'staffB4', NULL, 'Brenna Amity', 'staffB4', 0, 'c774319e', 'c774319e', 'c774319e', '2023-08-30 05:32:00.681817', '2023-08-30 05:32:00.683813', 2, 7),
(10, 'staffB5', NULL, 'Bridget Alva', 'staffB5', 0, 'f67012d1', 'f67012d1', 'f67012d1', '2023-08-30 05:32:38.761595', '2023-08-30 05:32:38.763596', 3, 8),
(11, 'staffB6', NULL, 'Bella Alvar', 'staffB6', 0, 'ee7f9828', 'ee7f9828', 'ee7f9828', '2023-08-30 05:33:13.551113', '2023-08-30 05:33:13.553113', 3, 8),
(12, 'staffB7', NULL, 'Calantha Amory', 'staffB7', 0, '6353946e', '6353946e', '6353946e', '2023-08-30 05:33:39.143283', '2023-08-30 05:33:39.146283', 4, 9),
(13, 'staffB8', NULL, 'Calliope Archibald', 'staffB8', 0, '7b8b05ab', '7b8b05ab', '7b8b05ab', '2023-08-30 05:39:35.392647', '2023-08-30 05:39:35.394649', 4, 9),
(14, 'staffB9', NULL, 'Celina Athelstan', 'staffB9', 0, '9996c23e', '9996c23e', '9996c23e', '2023-08-30 05:40:07.297753', '2023-08-30 05:40:07.299749', 5, 10),
(15, 'staffB10', NULL, 'Ceridwen Aubrey', 'staffB10', 0, 'b4684ece', 'b4684ece', 'b4684ece', '2023-08-30 05:40:36.135184', '2023-08-30 05:40:36.137175', 5, 10),
(16, 'internC1', NULL, 'Daria Augustus', 'internC1', 0, '05c313fc', '05c313fc', '05c313fc', '2023-08-30 05:41:44.610714', '2023-08-30 05:41:44.612713', 1, 11),
(17, 'internC2', NULL, 'Delwyn Aylmer', 'internC2', 0, 'd303cc0a', 'd303cc0a', 'd303cc0a', '2023-08-30 05:42:08.167153', '2023-08-30 05:42:08.169150', 1, 11),
(18, 'internC3', NULL, 'Dilys Anselm', 'internC3', 0, '08920b8e', '08920b8e', '08920b8e', '2023-08-30 05:42:38.763088', '2023-08-30 05:42:38.765088', 2, 12),
(19, 'internC4', NULL, 'Donna Azaria', 'internC4', 0, 'ae1c46ec', 'ae1c46ec', 'ae1c46ec', '2023-08-30 05:43:18.236472', '2023-08-30 05:43:18.238470', 2, 12),
(20, 'internC5', NULL, 'Doris Aidan', 'internC5', 0, 'a38063cb', 'a38063cb', 'a38063cb', '2023-08-30 05:43:51.480885', '2023-08-30 05:43:51.482885', 3, 13),
(21, 'internC6', NULL, 'Drusilla Anatole', 'internC6', 0, '2477ddc8', '2477ddc8', '2477ddc8', '2023-08-30 05:44:39.929165', '2023-08-30 05:44:39.931163', 3, 13),
(22, 'internC7', NULL, 'Dulcie Alden', 'internC7', 0, '5cc4ee58', '5cc4ee58', '5cc4ee58', '2023-08-30 05:45:21.962383', '2023-08-30 05:45:21.964376', 4, 14),
(23, 'internC8', NULL, 'Edana Alvin', 'internC8', 0, '96c1bca1', '96c1bca1', '96c1bca1', '2023-08-30 05:45:49.434177', '2023-08-30 05:45:49.436189', 4, 14),
(24, 'internC9', NULL, 'Edna Amyas', 'internC9', 0, '1e09d5bf', '1e09d5bf', '1e09d5bf', '2023-08-30 05:46:20.064932', '2023-08-30 05:46:20.067988', 5, 15),
(25, 'internC10', NULL, 'Eira Aneurin', 'internC10', 0, 'd1210175', 'd1210175', 'd1210175', '2023-08-30 05:46:45.375167', '2023-08-30 05:46:45.377172', 5, 15);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_tdtu_cntt2_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `tdtu_cntt2_adminaccounts`
--
ALTER TABLE `tdtu_cntt2_adminaccounts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `tdtu_cntt2_application`
--
ALTER TABLE `tdtu_cntt2_application`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tdtu_cntt2_applicati_file_id_id_ca98cfea_fk_tdtu_cntt` (`file_id_id`),
  ADD KEY `tdtu_cntt2_applicati_process_id_id_7c8abcbd_fk_tdtu_cntt` (`process_id_id`),
  ADD KEY `tdtu_cntt2_applicati_sender_id_id_7f352faa_fk_tdtu_cntt` (`sender_id_id`);

--
-- Indexes for table `tdtu_cntt2_departments`
--
ALTER TABLE `tdtu_cntt2_departments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tdtu_cntt2_files`
--
ALTER TABLE `tdtu_cntt2_files`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tdtu_cntt2_files_user_id_id_db156bf2_fk_tdtu_cntt2_user_id` (`user_id_id`);

--
-- Indexes for table `tdtu_cntt2_process`
--
ALTER TABLE `tdtu_cntt2_process`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tdtu_cntt2_receiverapplication`
--
ALTER TABLE `tdtu_cntt2_receiverapplication`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tdtu_cntt2_receivera_application_id_id_92cbdbd4_fk_tdtu_cntt` (`application_id_id`),
  ADD KEY `tdtu_cntt2_receivera_user_receiver_id_id_09fbb242_fk_tdtu_cntt` (`user_receiver_id_id`);

--
-- Indexes for table `tdtu_cntt2_role`
--
ALTER TABLE `tdtu_cntt2_role`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tdtu_cntt2_role_department_id_id_9a734fe2_fk_tdtu_cntt` (`department_id_id`);

--
-- Indexes for table `tdtu_cntt2_signature`
--
ALTER TABLE `tdtu_cntt2_signature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tdtu_cntt2_signature_user_id_id_cae241cb_fk_tdtu_cntt2_user_id` (`user_id_id`);

--
-- Indexes for table `tdtu_cntt2_step`
--
ALTER TABLE `tdtu_cntt2_step`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tdtu_cntt2_step_department_id_id_2b3f1976_fk_tdtu_cntt` (`department_id_id`),
  ADD KEY `tdtu_cntt2_step_process_id_id_32f2ec19_fk_tdtu_cntt2_process_id` (`process_id_id`),
  ADD KEY `tdtu_cntt2_step_role_id_id_8a85fbf0_fk_tdtu_cntt2_role_id` (`role_id_id`),
  ADD KEY `tdtu_cntt2_step_user_id_id_8edfa83f_fk_tdtu_cntt2_user_id` (`user_id_id`);

--
-- Indexes for table `tdtu_cntt2_user`
--
ALTER TABLE `tdtu_cntt2_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `tdtu_cntt2_user_department_id_id_b9c5885c_fk_tdtu_cntt` (`department_id_id`),
  ADD KEY `tdtu_cntt2_user_role_id_id_9c3dce42_fk_tdtu_cntt2_role_id` (`role_id_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_adminaccounts`
--
ALTER TABLE `tdtu_cntt2_adminaccounts`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_application`
--
ALTER TABLE `tdtu_cntt2_application`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_departments`
--
ALTER TABLE `tdtu_cntt2_departments`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_files`
--
ALTER TABLE `tdtu_cntt2_files`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_process`
--
ALTER TABLE `tdtu_cntt2_process`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_receiverapplication`
--
ALTER TABLE `tdtu_cntt2_receiverapplication`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_role`
--
ALTER TABLE `tdtu_cntt2_role`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_signature`
--
ALTER TABLE `tdtu_cntt2_signature`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_step`
--
ALTER TABLE `tdtu_cntt2_step`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tdtu_cntt2_user`
--
ALTER TABLE `tdtu_cntt2_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_tdtu_cntt2_user_id` FOREIGN KEY (`user_id`) REFERENCES `tdtu_cntt2_user` (`id`);

--
-- Constraints for table `tdtu_cntt2_application`
--
ALTER TABLE `tdtu_cntt2_application`
  ADD CONSTRAINT `tdtu_cntt2_applicati_file_id_id_ca98cfea_fk_tdtu_cntt` FOREIGN KEY (`file_id_id`) REFERENCES `tdtu_cntt2_files` (`id`),
  ADD CONSTRAINT `tdtu_cntt2_applicati_process_id_id_7c8abcbd_fk_tdtu_cntt` FOREIGN KEY (`process_id_id`) REFERENCES `tdtu_cntt2_process` (`id`),
  ADD CONSTRAINT `tdtu_cntt2_applicati_sender_id_id_7f352faa_fk_tdtu_cntt` FOREIGN KEY (`sender_id_id`) REFERENCES `tdtu_cntt2_user` (`id`);

--
-- Constraints for table `tdtu_cntt2_files`
--
ALTER TABLE `tdtu_cntt2_files`
  ADD CONSTRAINT `tdtu_cntt2_files_user_id_id_db156bf2_fk_tdtu_cntt2_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `tdtu_cntt2_user` (`id`);

--
-- Constraints for table `tdtu_cntt2_receiverapplication`
--
ALTER TABLE `tdtu_cntt2_receiverapplication`
  ADD CONSTRAINT `tdtu_cntt2_receivera_application_id_id_92cbdbd4_fk_tdtu_cntt` FOREIGN KEY (`application_id_id`) REFERENCES `tdtu_cntt2_application` (`id`),
  ADD CONSTRAINT `tdtu_cntt2_receivera_user_receiver_id_id_09fbb242_fk_tdtu_cntt` FOREIGN KEY (`user_receiver_id_id`) REFERENCES `tdtu_cntt2_user` (`id`);

--
-- Constraints for table `tdtu_cntt2_role`
--
ALTER TABLE `tdtu_cntt2_role`
  ADD CONSTRAINT `tdtu_cntt2_role_department_id_id_9a734fe2_fk_tdtu_cntt` FOREIGN KEY (`department_id_id`) REFERENCES `tdtu_cntt2_departments` (`id`);

--
-- Constraints for table `tdtu_cntt2_signature`
--
ALTER TABLE `tdtu_cntt2_signature`
  ADD CONSTRAINT `tdtu_cntt2_signature_user_id_id_cae241cb_fk_tdtu_cntt2_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `tdtu_cntt2_user` (`id`);

--
-- Constraints for table `tdtu_cntt2_step`
--
ALTER TABLE `tdtu_cntt2_step`
  ADD CONSTRAINT `tdtu_cntt2_step_department_id_id_2b3f1976_fk_tdtu_cntt` FOREIGN KEY (`department_id_id`) REFERENCES `tdtu_cntt2_departments` (`id`),
  ADD CONSTRAINT `tdtu_cntt2_step_process_id_id_32f2ec19_fk_tdtu_cntt2_process_id` FOREIGN KEY (`process_id_id`) REFERENCES `tdtu_cntt2_process` (`id`),
  ADD CONSTRAINT `tdtu_cntt2_step_role_id_id_8a85fbf0_fk_tdtu_cntt2_role_id` FOREIGN KEY (`role_id_id`) REFERENCES `tdtu_cntt2_role` (`id`),
  ADD CONSTRAINT `tdtu_cntt2_step_user_id_id_8edfa83f_fk_tdtu_cntt2_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `tdtu_cntt2_user` (`id`);

--
-- Constraints for table `tdtu_cntt2_user`
--
ALTER TABLE `tdtu_cntt2_user`
  ADD CONSTRAINT `tdtu_cntt2_user_department_id_id_b9c5885c_fk_tdtu_cntt` FOREIGN KEY (`department_id_id`) REFERENCES `tdtu_cntt2_departments` (`id`),
  ADD CONSTRAINT `tdtu_cntt2_user_role_id_id_9c3dce42_fk_tdtu_cntt2_role_id` FOREIGN KEY (`role_id_id`) REFERENCES `tdtu_cntt2_role` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
