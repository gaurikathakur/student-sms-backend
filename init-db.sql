
CREATE TABLE IF NOT EXISTS tblDepartment (
  DepartmentId INTEGER PRIMARY KEY AUTOINCREMENT,
  DepartmentName TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS tblStudent (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT,
  Username TEXT UNIQUE,
  Role TEXT,
  Course TEXT,
  MobileNo TEXT,
  Semester INTEGER,
  CGPA REAL,
  DOB TEXT,
  Hometown TEXT,
  Password TEXT,
  DepartmentId INTEGER,
  FOREIGN KEY(DepartmentId) REFERENCES tblDepartment(DepartmentId)
);
INSERT INTO tblDepartment (DepartmentName) VALUES ('Computer Science'), ('Business Administration'), ('Computer Applications');
INSERT INTO tblStudent (Name, Username, Role, Course, MobileNo, Semester, CGPA, DOB, Hometown, Password, DepartmentId)
VALUES
('Gaurika Thakur','gaurika','Admin','B.Tech','9990001111',8,9.1,'2001-04-15','Dehradun','admin123',1),
('aarav sharma','aarav','Student','B.Tech','9998887771',5,8.2,'2003-08-10','Delhi','aarav123',1),
('kavya singh','kavya','Student','BBA','8887776662',4,8.9,'2004-01-12','Lucknow','kavya123',2),
('rahul sharma','rahul','Student','BCA','7776665553',6,7.9,'2002-11-05','Jaipur','rahul123',3);
