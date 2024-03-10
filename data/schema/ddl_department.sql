DROP TABLE if exists department;
DROP TABLE if exists location;
DROP TABLE if exists contacts;


CREATE TABLE department(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  department_name TEXT
);

CREATE TABLE location(
  id INTEGER,
  location_name TEXT,
  FOREIGN KEY(id) REFERENCES department(id)
);
create TABLE contacts(
  id INTEGER,
  contact_type TEXT,
  contact_value TEXT,
  FOREIGN KEY(id) REFERENCES department(id)
);
