DROP TABLE IF EXISTS course;

CREATE TABLE course (
  id INTEGER PRIMARY KEY,
  major TEXT,
  course_code TEXT,
  division TEXT,
  course_name TEXT,
  credit TEXT,
  time TEXT,
  location TEXT,
  professor TEXT,
  is_english BOOLEAN,
  target_year TEXT,
  recommended_year TEXT
);
