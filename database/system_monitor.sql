--
-- Database: `system_monitor`
--

-- --------------------------------------------------------

--
-- Table structure for table `metrics`
--

CREATE TABLE `metrics` (
  `id` int(11) NOT NULL auto_increment,
  `system_id` int(11) default NULL,
  `hostname` varchar(100) default NULL,
  `ip_address` varchar(100) default NULL,
  `timestamp` varchar(50) default NULL,
  `uptime` bigint(20) default NULL,
  `os_type` varchar(50) default NULL,
  `os_version` varchar(100) default NULL,
  `os_release` varchar(100) default NULL,
  `kernel_version` varchar(100) default NULL,
  `architecture` varchar(50) default NULL,
  `platform` varchar(100) default NULL,
  `cpu_model` varchar(100) default NULL,
  `cpu_cores` int(11) default NULL,
  `cpu_threads` int(11) default NULL,
  `cpu_freq_current` float default NULL,
  `cpu_freq_max` float default NULL,
  `cpu_usage` float default NULL,
  `cpu_user` float default NULL,
  `cpu_system` float default NULL,
  `cpu_idle` float default NULL,
  `cpu_iowait` float default NULL,
  `load_1m` float default NULL,
  `load_5m` float default NULL,
  `load_15m` float default NULL,
  `ram_total` float default NULL,
  `ram_used` float default NULL,
  `ram_free` float default NULL,
  `ram_percent` float default NULL,
  `swap_percent` float default NULL,
  `disk_type` varchar(50) default NULL,
  `disk_total` float default NULL,
  `disk_used` float default NULL,
  `disk_free` float default NULL,
  `disk_percent` float default NULL,
  `disk_io_wait` float default NULL,
  `disk_read_bytes` bigint(20) default NULL,
  `disk_write_bytes` bigint(20) default NULL,
  `net_bytes_sent` bigint(20) default NULL,
  `net_bytes_recv` bigint(20) default NULL,
  `net_packets_sent` bigint(20) default NULL,
  `net_packets_recv` bigint(20) default NULL,
  `net_rtt` float default NULL,
  `process_count` int(11) default NULL,
  `thread_count` int(11) default NULL,
  `top_process_cpu` float default NULL,
  `top_process_memory` float default NULL,
  `cpu_temp` float default NULL,
  `fan_speed` int(11) default NULL,
  `power_usage` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `metrics`
--


-- --------------------------------------------------------

--
-- Table structure for table `systems`
--

CREATE TABLE `systems` (
  `id` int(11) NOT NULL auto_increment,
  `hostname` varchar(100) default NULL,
  `ip` varchar(50) default NULL,
  `timestamp` datetime default NULL,
  `os_name` varchar(100) default NULL,
  `os_version` varchar(100) default NULL,
  `cpu_model` text,
  `cpu_usage` float default NULL,
  `cpu_freq` float default NULL,
  `cpu_cores` int(11) default NULL,
  `cpu_threads` int(11) default NULL,
  `cpu_user` float default NULL,
  `cpu_system` float default NULL,
  `cpu_idle` float default NULL,
  `ram_total` float default NULL,
  `ram_used` float default NULL,
  `ram_free` float default NULL,
  `ram_percent` float default NULL,
  `disk_total` float default NULL,
  `disk_used` float default NULL,
  `disk_free` float default NULL,
  `disk_percent` float default NULL,
  `process_count` int(11) default NULL,
  `thread_count` int(11) default NULL,
  `battery_percent` float default NULL,
  `temperature` float default NULL,
  `net_sent` bigint(20) default NULL,
  `net_recv` bigint(20) default NULL,
  `net_packets_sent` bigint(20) default NULL,
  `net_packets_recv` bigint(20) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `systems`
--


-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(100) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `mobile`, `username`, `password`) VALUES
(1, 'Raj', 'akilnaveen36@gmail.com', '8148956634', 'raj', '1234');
