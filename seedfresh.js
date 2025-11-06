const sqlite3 = require("sqlite3").verbose();
const bcrypt = require("bcrypt");

const db = new sqlite3.Database("db.sqlite");

const teachers = [
  { Name: "Tanish Sharma", Username: "tanish", Password: "admin123", Role: "Admin", DepartmentId: 1 },
  { Name: "Arihant Mehta", Username: "arihant", Password: "admin123", Role: "Admin", DepartmentId: 2 },
  { Name: "Sukrit Bansal", Username: "sukrit", Password: "admin123", Role: "Admin", DepartmentId: 3 },
  { Name: "Riya Singh", Username: "riya", Password: "admin123", Role: "Admin", DepartmentId: 1 },
  { Name: "Naman Gupta", Username: "naman", Password: "admin123", Role: "Admin", DepartmentId: 2 },
];

const students = [
  { Name: "Ananya Gupta", Username: "ananya", Password: "student123", Role: "Student", DepartmentId: 1 },
  { Name: "Krish Patel", Username: "krish", Password: "student123", Role: "Student", DepartmentId: 1 },
  { Name: "Ishita Verma", Username: "ishita", Password: "student123", Role: "Student", DepartmentId: 2 },
  { Name: "Rohit Kumar", Username: "rohit", Password: "student123", Role: "Student", DepartmentId: 3 },
  { Name: "Aarav Jain", Username: "aarav", Password: "student123", Role: "Student", DepartmentId: 3 },
];

(async () => {
  for (const person of [...teachers, ...students]) {
    const hash = await bcrypt.hash(person.Password, 10);
    db.run(
      "INSERT INTO tblStudent (Name, Username, Password, Role, DepartmentId) VALUES (?,?,?,?,?)",
      [person.Name, person.Username, hash, person.Role, person.DepartmentId],
      (err) => {
        if (err) console.error("❌", err.message);
      }
    );
  }
  console.log("✅ Seeded 5 new teachers and 5 new students");
  db.close();
})();
