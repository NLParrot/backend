
DROP TABLE IF EXISTS building;
DROP TABLE IF EXISTS building_names;

CREATE TABLE building(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  latitude REAL,
  longitude REAL
);

CREATE TABLE building_names(
  id INTEGER,
  building_name TEXT,
  FOREIGN KEY(id) REFERENCES building(id)
);
