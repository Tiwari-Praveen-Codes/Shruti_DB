# ScholarTrack — DBMS Academic Progression Intelligence Mini-Project

ScholarTrack is a 3NF-compliant Relational Database Management System built using Python, SQLite 3, and Streamlit. It delivers student academic tracking, grade point trendlines, attendance defaulter monitoring, subject performance analytics, portfolio tracking, and one-way Google Sheets mirroring.

---

## ⚡ Fastest Windows Setup

Open PowerShell in this directory:

```powershell
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Run automated verification test suite
python test_suite.py

# 3. Launch ScholarTrack
python -m streamlit run app.py
```

*Note*: The database file `scholartrack.db` is initialized automatically on first startup.

---

## 🌟 Key Features

1. **Student Master Directory (Full CRUD)**:
   - Registration, name/roll search, safe update, and explicit cascade deletion.
2. **School Records (SSC / HSC)**:
   - Tracks board, passing year, marks obtained/total, and auto-computed percentage.
   - Enforces single record per student per level (`UNIQUE(student_id, level)`).
3. **Semester Results & Backlogs**:
   - SGPA / CGPA progression with strict `0.00 - 10.00` check constraints.
   - Tracks backlog counts, academic gap flags, and result statuses (Pass, ATKT, Fail, Pending).
4. **Subjects Catalogue & Examination Marks**:
   - Reusable catalogue for Theory and Lab courses.
   - Foreign key `ON DELETE RESTRICT` protects subjects from deletion while referenced by marks or attendance.
   - Marks tracking with passing thresholds and assessment components (Internal, External, Practical, Final).
5. **Interactive Progression & Analytics**:
   - Live Altair SGPA / CGPA trendline chart powered directly by database queries.
   - Subject-wise evaluation analytics: average percentage, failed attempts, and total evaluation counts.
6. **Attendance Surveillance**:
   - Class participation tracking per student, subject, year, and semester.
   - Configurable defaulter warning threshold with instant alert notifications.
7. **Academic Gaps**:
   - Formal interruption history with reason classification and `CHECK(end_year >= start_year)`.
8. **Student Portfolio (Activities & Seminars)**:
   - Technical, Co-curricular, and Extra-curricular activities with filtering.
   - Internal and External seminars with certificate proof URLs.
9. **Certificates & Target CGPA Predictor**:
   - Credential repository categorized by Course, Hackathon, Internship, Achievement, Seminar.
   - CGPA Forecaster calculating required future SGPA average; explicitly states equal-weight assumption and flags impossible targets.
10. **Google Sheets Sync**:
    - Direct integration with Google Sheets API v4.
    - Full refresh of all 10 normalized tables with verified API status and missing worksheet validation.

---

## ☁️ Google Sheets API Setup (Optional)

1. Enable **Google Sheets API** in Google Cloud Console.
2. Create a **Service Account** and download its JSON key file.
3. Create a Google Spreadsheet and share it with the service account email as **Editor**.
4. Create the 10 worksheet tabs with exact names:
   `Students`, `School_Records`, `Semester_Results`, `Subjects`, `Subject_Marks`, `Attendance`, `Gap_Years`, `Activities`, `Seminars`, `Certificates`.
5. Set environment variables in PowerShell and start the app:
```powershell
$env:GOOGLE_SERVICE_ACCOUNT_FILE="C:\path\to\service-account.json"
$env:GOOGLE_SHEET_ID="your-spreadsheet-id"
python -m streamlit run app.py
```
*Note*: The application tests the credentials and worksheet tabs directly; it does not simulate success.

---

## 🧪 Testing Checklist & Verification

Execute the test suite at any time:
```powershell
python test_suite.py
```
All 8 verification blocks covering all 11 mandatory DBMS constraints, cascading deletes, restrict deletes, and analytical calculations will run and report status. See [`docs/TESTING.md`](docs/TESTING.md) for details.

---

## 🏛️ Viva & Examiner Guide

A comprehensive architectural explanation of all 10 relational tables, 3NF normalization justification, primary/foreign keys, and viva answers is documented in [`docs/USER_AND_TECHNICAL_REPORT.md`](docs/USER_AND_TECHNICAL_REPORT.md).
