const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database("db.sqlite");

db.run("DELETE FROM tblStudent WHERE Username = 'gaurika'", (err) => {
  if (err) console.error("❌", err.message);
  else console.log("✅ Removed Gaurika from tblStudent");
  db.close();
});
