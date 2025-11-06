const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("db.sqlite");

// Define new English names for each student (you can change these!)
const updates = [
  { old: "आरव शर्मा", new: "Aarav Sharma" },
  { old: "काव्या सिंह", new: "Kavya Singh" },
  { old: "राहुल वर्मा", new: "Rahul Verma" },
  { old: "अनन्या गुप्ता", new: "Ananya Gupta" },
  { old: "रोहित कुमार", new: "Rohit Kumar" },
];

db.serialize(() => {
  updates.forEach(({ old, new: newName }) => {
    db.run("UPDATE tblStudent SET Name = ? WHERE Name = ?", [newName, old], (err) => {
      if (err) console.error("❌ Error updating:", err.message);
      else console.log(`✅ Updated ${old} → ${newName}`);
    });
  });
});

db.close();
