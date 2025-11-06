const sqlite3 = require("sqlite3").verbose();
const bcrypt = require("bcrypt");

const db = new sqlite3.Database("db.sqlite");

// Predefined sample data
const admins = [
  { Name: "Gaurika Thakur", Username: "gaurika", Password: "admin123", Role: "Admin", DepartmentId: 1 },
  { Name: "Tanish Sharma", Username: "tanish", Password: "admin123", Role: "Admin", DepartmentId: 1 },
  { Name: "Arihant Mehta", Username: "arihant", Password: "admin123", Role: "Admin", DepartmentId: 3 },
  { Name: "Sukrit Bansal", Username: "sukrit", Password: "admin123", Role: "Admin", DepartmentId: 2 },
  { Name: "Riya Singh", Username: "riya", Password: "admin123", Role: "Admin", DepartmentId: 1 },
];

const students = [
  { Name: "Ananya Gupta", Username: "ananya", Password: "student123", Role: "Student", DepartmentId: 1 },
  { Name: "Krish Patel", Username: "krish", Password: "student123", Role: "Student", DepartmentId: 1 },
  { Name: "Ishita Verma", Username: "ishita", Password: "student123", Role: "Student", DepartmentId: 2 },
  { Name: "Rohit Kumar", Username: "rohit", Password: "student123", Role: "Student", DepartmentId: 3 },
  { Name: "Aarav Jain", Username: "aarav", Password: "student123", Role: "Student", DepartmentId: 3 },
];

async function seed() {
  for (const user of [...admins, ...students]) {
    const hash = await bcrypt.hash(user.Password, 10);
    db.run(
      "INSERT INTO tblStudent (Name, Username, Password, Role, DepartmentId) VALUES (?,?,?,?,?)",
      [user.Name, user.Username, hash, user.Role, user.DepartmentId],
      (err) => {
        if (err) console.error(err.message);
      }
    );
  }
  console.log("✅ Seeded 5 admins + 5 students!");
}

seed();

