// backend/server.js
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const bodyParser = require('body-parser');

const DB_FILE = path.join(__dirname,'db.sqlite');
const INIT_SQL = `
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
  DepartmentName TEXT,
  Address TEXT,
  Languages TEXT,
  SecretQuestion TEXT,
  SecretAnswer TEXT
);
CREATE TABLE IF NOT EXISTS tblLeave (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  StudentId INTEGER,
  FromDate TEXT,
  ToDate TEXT,
  Reason TEXT,
  Status TEXT DEFAULT 'Pending'
);
CREATE TABLE IF NOT EXISTS tblSeminar (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Title TEXT,
  Description TEXT,
  Date TEXT
);
CREATE TABLE IF NOT EXISTS tblHoliday (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  Title TEXT,
  Date TEXT
);
`;

const app = express();
app.use(cors());
app.use(bodyParser.json());

const JWT_SECRET = 'replace_this_with_a_real_secret';

const db = new sqlite3.Database(DB_FILE);
db.serialize(()=>{
  db.exec(INIT_SQL);
  db.get("SELECT COUNT(*) as c FROM tblStudent", (e,row)=>{
    if(!e && row.c===0){
      // initial seed if DB empty — creates 2 admins and 3 students
      const users = [
        {Name:'Gaurika', Username:'gaurika', Role:'Admin', Password:'Admin@123', DepartmentName:'CSE'},
        {Name:'Shankar', Username:'shankar', Role:'Admin', Password:'Admin@123', DepartmentName:'CSE'},
        {Name:'Aarav Sharma', Username:'aarav', Role:'Student', Password:'student123', DepartmentName:'CSE', Semester:6, CGPA:8.9},
        {Name:'Kavya Singh', Username:'kavya', Role:'Student', Password:'student123', DepartmentName:'ECE', Semester:5, CGPA:8.5},
        {Name:'Rahul Verma', Username:'rahul', Role:'Student', Password:'student123', DepartmentName:'IT', Semester:4, CGPA:8.2}
      ];
      const insert = db.prepare("INSERT INTO tblStudent (Name,Username,Role,Course,MobileNo,Semester,CGPA,DOB,Hometown,Password,DepartmentName,Address,Languages,SecretQuestion,SecretAnswer) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)");
      users.forEach(u=>{
        const hash = bcrypt.hashSync(u.Password,10);
        insert.run(u.Name, u.Username, u.Role, u.Course||'', u.MobileNo||'', u.Semester||0, u.CGPA||0, u.DOB||'', u.Hometown||'', hash, u.DepartmentName||'', u.Address||'', (u.Languages||[]).join(','), u.SecretQuestion||'pet', u.SecretAnswer||'abc');
      });
      insert.finalize();
      console.log('Seeded users');
    }
  });
});

function runGet(sql, params=[]){
  return new Promise((res,rej)=>{ db.get(sql,params,(e,row)=> e?rej(e):res(row)); });
}
function runAll(sql, params=[]){
  return new Promise((res,rej)=>{ db.all(sql,params,(e,rows)=> e?rej(e):res(rows)); });
}
function runExec(sql, params=[]){
  return new Promise((res,rej)=>{ db.run(sql,params,function(e){ e?rej(e):res({ lastID: this.lastID }); }); });
}

function createToken(payload){ return jwt.sign(payload, JWT_SECRET, { expiresIn: '8h' }); }
function authMiddleware(req,res,next){
  const auth = req.headers.authorization;
  if(!auth) return res.status(401).json({ error: 'missing auth' });
  const token = auth.split(' ')[1];
  try { req.user = jwt.verify(token, JWT_SECRET); next(); }
  catch(e){ res.status(401).json({ error: 'invalid token' }); }
}

// Register
app.post('/api/register', async (req,res) => {
  try {
    const s = req.body;
    if (!s.Username || !s.Password) return res.status(400).json({ error: 'username & password required' });
    const exists = await runGet("SELECT Id FROM tblStudent WHERE Username = ?", [s.Username]).catch(()=>null);
    if (exists) return res.status(400).json({ error: 'username exists' });
    const passHash = await bcrypt.hash(s.Password, 10);
    const sql = `INSERT INTO tblStudent (Name,Username,Role,Course,MobileNo,Semester,CGPA,DOB,Hometown,Password,DepartmentName,Address,Languages,SecretQuestion,SecretAnswer)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`;
    const params = [
      s.Name||'', s.Username, s.Role||'Student', s.Course||'', s.MobileNo||'',
      s.Semester||0, s.CGPA||0, s.DOB||'', s.Hometown||'', passHash,
      s.DepartmentName||'', s.Address||'', (s.Languages||[]).join(','), s.SecretQuestion||'', s.SecretAnswer||''
    ];
    const r = await runExec(sql, params);
    const user = await runGet("SELECT Id,Name,Username,Role,DepartmentName,Semester,CGPA,Hometown,Address,Languages FROM tblStudent WHERE Id = ?", [r.lastID]);
    res.json({ ok: true, user });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Login
app.post('/api/login', async (req,res) => {
  try {
    const { username, password } = req.body;
    const user = await runGet("SELECT * FROM tblStudent WHERE Username = ?", [username]);
    if (!user) return res.status(401).json({ error: 'invalid credentials' });
    const match = await bcrypt.compare(password, user.Password);
    if (!match) return res.status(401).json({ error: 'invalid credentials' });
    const token = createToken({ id: user.Id, username: user.Username, role: user.Role });
    delete user.Password;
    res.json({ token, user });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Forgot password (secret answer)
app.post('/api/forgot-password', async (req,res) => {
  try {
    const { username, secretAnswer, newPassword } = req.body;
    const user = await runGet("SELECT * FROM tblStudent WHERE Username = ?", [username]);
    if (!user) return res.status(404).json({ error: 'user not found' });
    if (!secretAnswer || secretAnswer !== user.SecretAnswer) return res.status(400).json({ error: 'invalid secret answer' });
    const hash = await bcrypt.hash(newPassword, 10);
    await runExec("UPDATE tblStudent SET Password = ? WHERE Id = ?", [hash, user.Id]);
    res.json({ ok: true, message: 'password updated' });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Admin: list students
app.get('/api/students', authMiddleware, async (req,res) => {
  if (req.user.role !== 'Admin') return res.status(403).json({ error: 'admin only' });
  const rows = await runAll("SELECT Id,Name,Username,Role,DepartmentName,Semester,CGPA,Hometown,Address,Languages FROM tblStudent");
  res.json({ students: rows });
});

// Get student (admin or owner)
app.get('/api/student/:id', authMiddleware, async (req,res) => {
  const id = Number(req.params.id);
  const row = await runGet("SELECT Id,Name,Username,Role,DepartmentName,Semester,CGPA,Hometown,Address,Languages FROM tblStudent WHERE Id = ?", [id]);
  if (!row) return res.status(404).json({ error: 'not found' });
  if (req.user.role !== 'Admin' && req.user.id !== id) return res.status(403).json({ error: 'forbidden' });
  res.json({ student: row });
});

// Update profile (student or admin)
app.put('/api/updateProfile/:id', authMiddleware, async (req,res) => {
  try {
    const id = Number(req.params.id);
    if (req.user.role !== 'Admin' && req.user.id !== id) return res.status(403).json({ error: 'forbidden' });
    const s = req.body;
    await runExec(`UPDATE tblStudent SET Name=?, DepartmentName=?, Semester=?, CGPA=?, Hometown=?, Address=?, Languages=? WHERE Id=?`, [
      s.Name||'', s.DepartmentName||'', s.Semester||0, s.CGPA||0, s.Hometown||'', s.Address||'', (s.Languages||[]).join(','), id
    ]);
    const updated = await runGet("SELECT Id,Name,Username,Role,DepartmentName,Semester,CGPA,Hometown,Address,Languages FROM tblStudent WHERE Id = ?", [id]);
    res.json({ ok: true, student: updated });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Leave endpoints
app.post('/api/leave', authMiddleware, async (req,res) => {
  try {
    const s = req.body;
    const r = await runExec("INSERT INTO tblLeave (StudentId,FromDate,ToDate,Reason,Status) VALUES (?,?,?,?,?)", [s.StudentId, s.FromDate, s.ToDate, s.Reason, 'Pending']);
    res.json({ ok: true, id: r.lastID });
  } catch (e) { res.status(500).json({ error: e.message }); }
});
app.get('/api/leave', authMiddleware, async (req,res) => {
  if (req.user.role === 'Admin') {
    const rows = await runAll("SELECT * FROM tblLeave");
    res.json({ leaves: rows });
  } else {
    const rows = await runAll("SELECT * FROM tblLeave WHERE StudentId = ?", [req.user.id]);
    res.json({ leaves: rows });
  }
});
app.put('/api/leave/:id/decide', authMiddleware, async (req,res) => {
  if (req.user.role !== 'Admin') return res.status(403).json({ error: 'admin only' });
  const id = req.params.id;
  const { status } = req.body;
  await runExec("UPDATE tblLeave SET Status = ? WHERE Id = ?", [status, id]);
  res.json({ ok: true });
});

// Seminars + holidays
app.post('/api/seminars', authMiddleware, async (req,res) => {
  if (req.user.role !== 'Admin') return res.status(403).json({ error: 'admin only' });
  const s = req.body;
  const r = await runExec("INSERT INTO tblSeminar (Title,Description,Date) VALUES (?,?,?)", [s.Title, s.Description, s.Date]);
  res.json({ ok: true, id: r.lastID });
});
app.get('/api/seminars', authMiddleware, async (req,res) => {
  const rows = await runAll("SELECT * FROM tblSeminar");
  res.json({ seminars: rows });
});
app.post('/api/holidays', authMiddleware, async (req,res) => {
  if (req.user.role !== 'Admin') return res.status(403).json({ error: 'admin only' });
  const s = req.body;
  const r = await runExec("INSERT INTO tblHoliday (Title,Date) VALUES (?,?)", [s.Title, s.Date]);
  res.json({ ok: true, id: r.lastID });
});
app.get('/api/holidays', authMiddleware, async (req,res) => {
  const rows = await runAll("SELECT * FROM tblHoliday");
  res.json({ holidays: rows });
});

app.listen(5000, ()=> console.log('Server running on port 5000'));
