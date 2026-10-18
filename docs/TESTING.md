# ScholarTrack Comprehensive Verification & Testing Checklist

This document details the automated test suite and manual verification checklist for ScholarTrack.

---

## 🚀 Quick Automated Test Run (Windows PowerShell)

Run the automated test suite covering all 11 constraint rules, full CRUD lifecycle, cascading deletes, restrict deletes, and analytical calculations:

```powershell
python test_suite.py
```

Expected output:
```
[1/8] Testing Student Operations (Add, Edit, Unique constraints)...
[2/8] Testing School Records (Add, Edit, Delete, Range checks)...
[3/8] Testing Semester Results (Add, Edit, SGPA/CGPA 0..10 checks)...
[4/8] Testing Subjects & Subject Marks (Catalogue, RESTRICT check, Evaluation Analytics)...
[5/8] Testing Attendance (Attended > held rejection, Defaulter calculation)...
[6/8] Testing Academic Gaps, Portfolio Activities, Seminars, Certificates...
[7/8] Testing CGPA Predictor Math & Assumptions...
[8/8] Testing Student CASCADE Deletion...
==================================================================
>>> ALL 8 FULL LIFECYCLE DBMS & BUSINESS LOGIC TESTS PASSED! <<<
==================================================================
```

---

## 📋 Comprehensive Feature & Test Verification Checklist

| Test Item | Verification Procedure | Expected Outcome | Status |
| :--- | :--- | :--- | :---: |
| **1. Duplicate Roll Number** | Attempt to insert or update a student with an existing roll number | Rejected with `UNIQUE constraint failed: students.roll_number` | ✅ PASS |
| **2. Duplicate Email** | Attempt to insert or update a student with an existing email | Rejected with `UNIQUE constraint failed: students.email` | ✅ PASS |
| **3. Duplicate Subject Code** | Attempt to add a subject with an existing code | Rejected with `UNIQUE constraint failed: subjects.subject_code` | ✅ PASS |
| **4. Duplicate School Level** | Attempt to add two SSC records for the same student | Rejected with `UNIQUE(student_id, level)` | ✅ PASS |
| **5. Duplicate Semester** | Attempt to add two results for the same student and semester number | Rejected with `UNIQUE(student_id, semester_number)` | ✅ PASS |
| **6. Duplicate Subject Mark** | Attempt to add marks for the same subject twice in one semester result | Rejected with `UNIQUE(semester_result_id, subject_id)` | ✅ PASS |
| **7. Duplicate Attendance** | Attempt to record attendance for the same student, subject, year, and semester | Rejected with `UNIQUE(student_id, subject_id, academic_year, semester_number)` | ✅ PASS |
| **8. SGPA / CGPA Range Check** | Attempt to enter SGPA or CGPA < 0.00 or > 10.00 | Rejected with `CHECK(sgpa BETWEEN 0 AND 10)` | ✅ PASS |
| **9. Marks Range Check** | Attempt marks obtained > total marks or total marks <= 0 | Rejected with `CHECK(marks_obtained <= marks_total)` | ✅ PASS |
| **10. Attendance Validity** | Attempt classes attended > classes held | Rejected with `CHECK(classes_attended <= classes_held)` | ✅ PASS |
| **11. Gap Year Validation** | Attempt end_year < start_year | Rejected with `CHECK(end_year >= start_year)` | ✅ PASS |
| **12. Cascade Delete on Student** | Delete a student via the directory | Deletes all linked records across all 9 child tables via `ON DELETE CASCADE` | ✅ PASS |
| **13. Restrict Delete on Subject** | Attempt to delete a subject referenced in marks or attendance | Operation blocked via `ON DELETE RESTRICT` with clear explanation | ✅ PASS |
| **14. Unreferenced Subject Delete** | Delete a subject not referenced in any marks or attendance | Deletion succeeds cleanly | ✅ PASS |
| **15. Live Trendline Graph** | Open Dashboard with a student having semester results | Line chart displays live SGPA and CGPA trends with interactive tooltips | ✅ PASS |
| **16. Subject Analytics** | Open Subjects & Marks tab | Computes live average percentage, fail count, and total attempts | ✅ PASS |
| **17. Attendance Defaulter Alert** | Adjust threshold slider in Attendance tab | Correctly categorizes and warns about students with attendance below threshold | ✅ PASS |
| **18. CGPA Predictor Math** | Forecast required SGPA for a target CGPA | Calculates required SGPA, flags unreachable targets (>10), states equal-weight assumption | ✅ PASS |
| **19. Google Sheets Sync Credential Check** | Trigger sync without environment variables | Returns clear descriptive error with instructions; does NOT fake success | ✅ PASS |
| **20. Google Sheets Worksheet Check** | Trigger sync with missing tabs | Identifies specific missing tabs and prompts user to create them | ✅ PASS |

---

## ⚖️ Implemented vs Incomplete Features

### Implemented Features
- Complete 3NF-compliant relational schema across 10 tables.
- Full CRUD operations (Create, Read, Update, Delete) for all 10 modules:
  - Students
  - School Records (SSC/HSC)
  - Semester Results
  - Subjects Catalogue
  - Subject Marks
  - Attendance Records
  - Academic Gaps
  - Co-curricular & Extra-curricular Activities
  - Seminars & Workshops
  - Certificates & Credentials
- Enforced relational integrity: `PRAGMA foreign_keys = ON`, `ON DELETE CASCADE`, and `ON DELETE RESTRICT`.
- Defensive input validation and user-friendly constraint error translation.
- Interactive Altair visualization for live SGPA/CGPA progression.
- Aggregated SQL subject evaluation analytics (average %, failed attempts).
- Attendance surveillance with configurable defaulter threshold.
- Simplified equal-weight CGPA forecaster with boundary detection.
- Real Google Sheets API one-way full sync with worksheet validation.

### Honest Limitations & Out-of-Scope Elements
- **Default Database**: Local SQLite file (`scholartrack.db`). Not a cloud MySQL/PostgreSQL/BigQuery instance. (Enterprise DBMS support requires live server host, port, user credentials, and network firewall access).
- **Google Sheets Sync**: One-way manual full refresh (Database → Sheets). Does not support bidirectional synchronization (edits made in the Google Sheet do not automatically write back to SQLite).
- **Authentication**: Single-session application without role-based login (no separate Student vs Administrator roles).
- **CGPA Calculation Model**: Simplified equal-weight semester average assumption; institutions using credit-weighted formulas ($CGPA = \frac{\sum (SGPA_i \times Credits_i)}{\sum Credits_i}$) will observe slight variations.
