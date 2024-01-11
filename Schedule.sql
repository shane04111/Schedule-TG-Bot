-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2023 年 12 月 06 日 15:44
-- 伺服器版本： 8.0.35-0ubuntu0.22.04.1
-- PHP 版本： 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `Schedule`
--

-- --------------------------------------------------------

--
-- 資料表結構 `Error`
--

CREATE TABLE `Error` (
  `ID` bigint NOT NULL,
  `Message` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'No Message',
  `UserID` bigint NOT NULL DEFAULT '-1',
  `ChatID` bigint NOT NULL DEFAULT '-1',
  `DateTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `UserTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `Send` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='使用者提醒';

-- --------------------------------------------------------

--
-- 資料表結構 `schedule`
--

CREATE TABLE `schedule` (
  `ID` bigint NOT NULL,
  `Message` varchar(4500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'No Message',
  `UserID` bigint NOT NULL DEFAULT '-1',
  `ChatID` bigint NOT NULL DEFAULT '-1',
  `DateTime` datetime DEFAULT NULL,
  `Zone` varchar(6) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT '+08:00',
  `UserTime` datetime DEFAULT NULL,
  `Send` varchar(5) COLLATE utf8mb4_unicode_520_ci DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='使用者提醒';

-- --------------------------------------------------------

--
-- 資料表結構 `UserData`
--

CREATE TABLE `UserData` (
  `ID` bigint NOT NULL,
  `UserID` bigint NOT NULL DEFAULT '-1',
  `ChatID` bigint NOT NULL DEFAULT '-1',
  `MessageID` bigint NOT NULL DEFAULT '-1',
  `UserMessageID` bigint NOT NULL DEFAULT '-1',
  `Redo` varchar(5) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'False',
  `Delete` varchar(5) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'False',
  `Text` varchar(4500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `Year` int NOT NULL DEFAULT '-1',
  `Month` int NOT NULL DEFAULT '-1',
  `Day` int NOT NULL DEFAULT '-1',
  `Hour` int NOT NULL DEFAULT '-1',
  `Miner` int NOT NULL DEFAULT '-1',
  `StartTime` datetime DEFAULT NULL,
  `EndTime` datetime DEFAULT NULL,
  `CheckDone` varchar(5) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'False',
  `isToday` varchar(5) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'False',
  `isOY` varchar(5) COLLATE utf8mb4_unicode_520_ci NOT NULL DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='使用者暫存資料';

-- --------------------------------------------------------

--
-- 資料表結構 `UserLocal`
--

CREATE TABLE `UserLocal` (
  `chatID` bigint NOT NULL,
  `userID` bigint NOT NULL,
  `Language` varchar(20) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `Localtime` varchar(20) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `OnlyAdmin` varchar(5) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL,
  `datePickStyle` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='使用者本地化設置';

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `Error`
--
ALTER TABLE `Error`
  ADD PRIMARY KEY (`ID`);

--
-- 資料表索引 `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`ID`);

--
-- 資料表索引 `UserData`
--
ALTER TABLE `UserData`
  ADD PRIMARY KEY (`ID`);

--
-- 資料表索引 `UserLocal`
--
ALTER TABLE `UserLocal`
  ADD PRIMARY KEY (`chatID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `Error`
--
ALTER TABLE `Error`
  MODIFY `ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `schedule`
--
ALTER TABLE `schedule`
  MODIFY `ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `UserData`
--
ALTER TABLE `UserData`
  MODIFY `ID` bigint NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
