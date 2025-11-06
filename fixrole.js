const sqlite3 = require("sqlite3").verbose();

const db = new sqlite3.Database("db.sqlite");

// Update the role for Gaurika
db.run(
  "UPDATE tblStudent SET Role = 'Admin' WHERE Username = 'gaurika'",
  (err) => {
    if (err) {
      console.error("❌ Error updating role:", err.message);
    } else {
      console.log("✅ Successfully updated Gaurika to Admin role!");
    }
    db.close();
  }
);
