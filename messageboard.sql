CREATE DATABASE messageboard;
\c messageboard;
-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE IF NOT EXISTS message (
  username varchar(20),
  message varchar(200),
) ;

--

--

INSERT INTO message (username, message) VALUES
('Dalina', 'hi people'),
('jt', 'whats up hi');

-- --------------------------------------------------------

--

--

CREATE TABLE IF NOT EXISTS users (
  username varchar(20),
  password varchar(20)
) ;

--
-- Dumping data for table `stores`
--

INSERT INTO users (usename, password) VALUES
('Dalina', 'apple'),
('jt', 'banana');

-- --------------------------------------------------------

--

--
