const sqlite3 = require("sqlite3").verbose();
const bcrypt = require("bcrypt");
const db = new sqlite3.Database("db.sqlite");

(async () => {
  // 1️⃣ Delete old records
  await new Promise((res, rej) => {
    db.run("DELETE FROM tblStudent", (err) => {
      if (err) rej(err);
      else res();
    });
  });

  console.log("🧹 Cleared all old student/admin entries");

  // 2️⃣ New teachers (Admins)
  const teachers = [
    { Name: "Tanish Sharma", Username: "tanish", Password: "admin123", Role: "Admin" },
    { Name: "Arihant Mehta", Username: "arihant", Password: "admin123", Role: "Admin" },
    { Name: "Sukrit Bansal", Username: "sukrit", Password: "admin123", Role: "Admin" },
    { Name: "Riya Singh", Username: "riya", Password: "admin123", Role: "Admin" },
    { Name: "Naman Gupta", Username: "naman", Password: "admin123", Role: "Admin" },
  ];

  // 3️⃣ New students
  const students = [
    { Name: "aarav sharma", Username: "aarav", Password: "student123", Role: "Student" },
    { Name: "kavya singh", Username: "kavya", Password: "student123", Role: "Student" },
    { Name: "rahul sharma", Username: "rahul", Password: "student123", Role: "Student" },
    { Name: "ananya gupta", Username: "ananya", Password: "student123", Role: "Student" },
    { Name: "rohit sharma", Username: "rohit", Password: "student123", Role: "Student" },
  ];

  // 4️⃣ Insert all
  for (const user of [...teachers, ...students]) {
    const hash = await bcrypt.hash(user.Password, 10);
    await new Promise((res, rej) => {
      db.run(
        "INSERT INTO tblStudent (Name, Username, Password, Role) VALUES (?,?,?,?)",
        [user.Name, user.Username, hash, user.Role],
        (err) => (err ? rej(err) : res())
      );
    });
  }

  console.log("✅ Added 5 teachers and 5 students");
  db.close();
})();
