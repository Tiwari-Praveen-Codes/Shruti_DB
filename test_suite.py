import os
import sqlite3
import pandas as pd

DB_TEST = "test_suite_scholartrack.db"

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS students(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 roll_number TEXT NOT NULL UNIQUE,
 full_name TEXT NOT NULL,
 email TEXT UNIQUE,
 department TEXT NOT NULL,
 admission_year INTEGER NOT NULL CHECK(admission_year BETWEEN 1990 AND 2100),
 current_status TEXT NOT NULL DEFAULT 'Active' CHECK(current_status IN ('Active','Graduated','On Hold','Discontinued'))
);
CREATE TABLE IF NOT EXISTS school_records(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
 level TEXT NOT NULL CHECK(level IN ('SSC','HSC')),
 board TEXT, passing_year INTEGER NOT NULL CHECK(passing_year BETWEEN 1990 AND 2100),
 marks_obtained REAL NOT NULL CHECK(marks_obtained>=0),
 marks_total REAL NOT NULL CHECK(marks_total>0 AND marks_obtained<=marks_total),
 percentage REAL NOT NULL CHECK(percentage BETWEEN 0 AND 100),
 UNIQUE(student_id,level)
);
CREATE TABLE IF NOT EXISTS semester_results(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
 semester_number INTEGER NOT NULL CHECK(semester_number BETWEEN 1 AND 12),
 academic_year TEXT NOT NULL,
 sgpa REAL NOT NULL CHECK(sgpa BETWEEN 0 AND 10),
 cgpa REAL NOT NULL CHECK(cgpa BETWEEN 0 AND 10),
 result_status TEXT NOT NULL CHECK(result_status IN ('Pass','ATKT','Fail','Pending')),
 backlog_count INTEGER NOT NULL DEFAULT 0 CHECK(backlog_count>=0),
 is_gap_after INTEGER NOT NULL DEFAULT 0 CHECK(is_gap_after IN (0,1)),
 UNIQUE(student_id,semester_number)
);
CREATE TABLE IF NOT EXISTS subjects(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 subject_code TEXT NOT NULL UNIQUE,
 subject_name TEXT NOT NULL,
 subject_type TEXT NOT NULL CHECK(subject_type IN ('Theory','Lab')),
 credits REAL NOT NULL DEFAULT 0 CHECK(credits>=0)
);
CREATE TABLE IF NOT EXISTS subject_marks(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 semester_result_id INTEGER NOT NULL REFERENCES semester_results(id) ON DELETE CASCADE,
 subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
 marks_obtained REAL NOT NULL CHECK(marks_obtained>=0),
 marks_total REAL NOT NULL CHECK(marks_total>0 AND marks_obtained<=marks_total),
 passing_marks REAL NOT NULL CHECK(passing_marks>=0 AND passing_marks<=marks_total),
 component TEXT NOT NULL DEFAULT 'Final' CHECK(component IN ('Internal','External','Practical','Final')),
 UNIQUE(semester_result_id,subject_id)
);
CREATE TABLE IF NOT EXISTS attendance(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
 subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
 academic_year TEXT NOT NULL,
 semester_number INTEGER NOT NULL CHECK(semester_number BETWEEN 1 AND 12),
 classes_held INTEGER NOT NULL CHECK(classes_held>=0),
 classes_attended INTEGER NOT NULL CHECK(classes_attended>=0 AND classes_attended<=classes_held),
 UNIQUE(student_id,subject_id,academic_year,semester_number)
);
CREATE TABLE IF NOT EXISTS gap_years(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
 start_year INTEGER NOT NULL,
 end_year INTEGER NOT NULL CHECK(end_year>=start_year),
 reason_category TEXT NOT NULL CHECK(reason_category IN ('Academic','Medical','Personal','Other')),
 notes TEXT
);
CREATE TABLE IF NOT EXISTS activities(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
 title TEXT NOT NULL,
 activity_type TEXT NOT NULL CHECK(activity_type IN ('Technical','Co-curricular','Extra-curricular')),
 organization TEXT, activity_date TEXT, description TEXT
);
CREATE TABLE IF NOT EXISTS seminars(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
 title TEXT NOT NULL,
 seminar_scope TEXT NOT NULL CHECK(seminar_scope IN ('Internal','External')),
 organizer TEXT, seminar_date TEXT, certificate_url TEXT
);
CREATE TABLE IF NOT EXISTS certificates(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
 title TEXT NOT NULL,
 issuer TEXT NOT NULL,
 category TEXT NOT NULL CHECK(category IN ('Course','Hackathon','Internship','Achievement','Seminar','Other')),
 issue_date TEXT,
 credential_url TEXT,
 notes TEXT
);
"""

def test_full_lifecycle():
    if os.path.exists(DB_TEST):
        try: os.remove(DB_TEST)
        except: pass

    conn = sqlite3.connect(DB_TEST)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)

    print("[1/8] Testing Student Operations (Add, Edit, Unique constraints)...")
    cur = conn.cursor()
    cur.execute("INSERT INTO students(roll_number, full_name, email, department, admission_year, current_status) VALUES(?,?,?,?,?,?)",
                ("22CS101", "Rohan Mehta", "rohan@college.edu", "CSE", 2022, "Active"))
    conn.commit()
    s_id = cur.lastrowid

    # Test Edit Student
    conn.execute("UPDATE students SET full_name=?, current_status=? WHERE id=?",
                 ("Rohan K. Mehta", "Active", s_id))
    conn.commit()
    updated_name = conn.execute("SELECT full_name FROM students WHERE id=?", (s_id,)).fetchone()[0]
    assert updated_name == "Rohan K. Mehta"

    # Test Duplicate Roll
    try:
        conn.execute("INSERT INTO students(roll_number, full_name, email, department, admission_year) VALUES(?,?,?,?,?)",
                     ("22CS101", "Duplicate Rohan", "other@college.edu", "CSE", 2022))
        conn.commit()
        assert False, "Duplicate roll number allowed"
    except sqlite3.IntegrityError:
        pass

    # Test Duplicate Email
    try:
        conn.execute("INSERT INTO students(roll_number, full_name, email, department, admission_year) VALUES(?,?,?,?,?)",
                     ("22CS102", "New Student", "rohan@college.edu", "CSE", 2022))
        conn.commit()
        assert False, "Duplicate email allowed"
    except sqlite3.IntegrityError:
        pass

    print("[2/8] Testing School Records (Add, Edit, Delete, Range checks)...")
    # Marks > total rejected
    try:
        conn.execute("INSERT INTO school_records(student_id, level, board, passing_year, marks_obtained, marks_total, percentage) VALUES(?,?,?,?,?,?,?)",
                     (s_id, "SSC", "State", 2020, 550, 500, 110.0))
        conn.commit()
        assert False, "Marks > total allowed"
    except sqlite3.IntegrityError:
        pass

    conn.execute("INSERT INTO school_records(student_id, level, board, passing_year, marks_obtained, marks_total, percentage) VALUES(?,?,?,?,?,?,?)",
                 (s_id, "SSC", "CBSE", 2020, 450, 500, 90.0))
    conn.commit()

    # Edit school record
    conn.execute("UPDATE school_records SET marks_obtained=?, percentage=? WHERE student_id=? AND level=?",
                 (460, 92.0, s_id, "SSC"))
    conn.commit()
    assert conn.execute("SELECT marks_obtained FROM school_records WHERE student_id=? AND level=?", (s_id, "SSC")).fetchone()[0] == 460

    print("[3/8] Testing Semester Results (Add, Edit, SGPA/CGPA 0..10 checks)...")
    # SGPA > 10 rejected
    try:
        conn.execute("INSERT INTO semester_results(student_id, semester_number, academic_year, sgpa, cgpa, result_status) VALUES(?,?,?,?,?,?)",
                     (s_id, 1, "2022-23", 10.5, 9.0, "Pass"))
        conn.commit()
        assert False, "SGPA > 10 allowed"
    except sqlite3.IntegrityError:
        pass

    cur.execute("INSERT INTO semester_results(student_id, semester_number, academic_year, sgpa, cgpa, result_status, backlog_count, is_gap_after) VALUES(?,?,?,?,?,?,?,?)",
                (s_id, 1, "2022-23", 8.2, 8.2, "Pass", 0, 0))
    conn.commit()
    sem1_id = cur.lastrowid

    cur.execute("INSERT INTO semester_results(student_id, semester_number, academic_year, sgpa, cgpa, result_status, backlog_count, is_gap_after) VALUES(?,?,?,?,?,?,?,?)",
                (s_id, 2, "2022-23", 8.8, 8.5, "Pass", 0, 1))
    conn.commit()
    sem2_id = cur.lastrowid

    # Edit semester result
    conn.execute("UPDATE semester_results SET sgpa=?, cgpa=? WHERE id=?", (8.4, 8.4, sem1_id))
    conn.commit()
    assert conn.execute("SELECT sgpa FROM semester_results WHERE id=?", (sem1_id,)).fetchone()[0] == 8.4

    print("[4/8] Testing Subjects & Subject Marks (Catalogue, RESTRICT check, Evaluation Analytics)...")
    cur.execute("INSERT INTO subjects(subject_code, subject_name, subject_type, credits) VALUES(?,?,?,?)",
                ("CS301", "Data Structures & Algorithms", "Theory", 4.0))
    sub1_id = cur.lastrowid

    cur.execute("INSERT INTO subjects(subject_code, subject_name, subject_type, credits) VALUES(?,?,?,?)",
                ("CS302", "DSA Lab", "Lab", 2.0))
    sub2_id = cur.lastrowid

    # Add marks: student sem1 scored 75/100, pass threshold 40
    conn.execute("INSERT INTO subject_marks(semester_result_id, subject_id, marks_obtained, marks_total, passing_marks, component) VALUES(?,?,?,?,?,?)",
                 (sem1_id, sub1_id, 75, 100, 40, "Final"))
    # Add fail attempt: student sem1 scored 32/100, pass threshold 40
    conn.execute("INSERT INTO subject_marks(semester_result_id, subject_id, marks_obtained, marks_total, passing_marks, component) VALUES(?,?,?,?,?,?)",
                 (sem1_id, sub2_id, 32, 100, 40, "Practical"))
    conn.commit()

    # RESTRICT check on referenced subject
    try:
        conn.execute("DELETE FROM subjects WHERE id=?", (sub1_id,))
        conn.commit()
        assert False, "Subject deletion should be RESTRICTED when referenced by subject_marks"
    except sqlite3.IntegrityError:
        pass

    # Analytics query verification
    perf_df = pd.read_sql_query("""
        SELECT sub.subject_code, sub.subject_name, sub.subject_type,
               ROUND(AVG(100.0 * sm.marks_obtained / sm.marks_total), 2) AS avg_percentage,
               SUM(CASE WHEN sm.marks_obtained < sm.passing_marks THEN 1 ELSE 0 END) AS failed_attempts,
               COUNT(*) AS attempts
        FROM subject_marks sm
        JOIN subjects sub ON sub.id = sm.subject_id
        GROUP BY sub.id
        ORDER BY sub.subject_code
    """, conn)
    assert len(perf_df) == 2
    assert perf_df.loc[perf_df.subject_code=="CS301", "avg_percentage"].iloc[0] == 75.0
    assert perf_df.loc[perf_df.subject_code=="CS301", "failed_attempts"].iloc[0] == 0
    assert perf_df.loc[perf_df.subject_code=="CS302", "avg_percentage"].iloc[0] == 32.0
    assert perf_df.loc[perf_df.subject_code=="CS302", "failed_attempts"].iloc[0] == 1

    print("[5/8] Testing Attendance (Attended > held rejection, Defaulter calculation)...")
    # Attended > held rejected
    try:
        conn.execute("INSERT INTO attendance(student_id, subject_id, academic_year, semester_number, classes_held, classes_attended) VALUES(?,?,?,?,?,?)",
                     (s_id, sub1_id, "2022-23", 1, 40, 45))
        conn.commit()
        assert False, "Attended > held allowed"
    except sqlite3.IntegrityError:
        pass

    # Add valid attendance: 36/40 = 90% (eligible)
    conn.execute("INSERT INTO attendance(student_id, subject_id, academic_year, semester_number, classes_held, classes_attended) VALUES(?,?,?,?,?,?)",
                 (s_id, sub1_id, "2022-23", 1, 40, 36))
    # Add low attendance: 24/40 = 60% (below 75% threshold)
    conn.execute("INSERT INTO attendance(student_id, subject_id, academic_year, semester_number, classes_held, classes_attended) VALUES(?,?,?,?,?,?)",
                 (s_id, sub2_id, "2022-23", 1, 40, 24))
    conn.commit()

    att_df = pd.read_sql_query("""
        SELECT a.*, ROUND(100.0 * a.classes_attended / NULLIF(a.classes_held,0), 2) AS attendance_pct
        FROM attendance a
    """, conn)
    threshold = 75
    defaulters = att_df[att_df["attendance_pct"] < threshold]
    assert len(defaulters) == 1
    assert defaulters.iloc[0]["classes_attended"] == 24

    print("[6/8] Testing Academic Gaps, Portfolio Activities, Seminars, Certificates...")
    # Gap end < start rejected
    try:
        conn.execute("INSERT INTO gap_years(student_id, start_year, end_year, reason_category) VALUES(?,?,?,?)",
                     (s_id, 2024, 2023, "Medical"))
        conn.commit()
        assert False, "End year < start year allowed"
    except sqlite3.IntegrityError:
        pass

    conn.execute("INSERT INTO gap_years(student_id, start_year, end_year, reason_category, notes) VALUES(?,?,?,?,?)",
                 (s_id, 2023, 2024, "Medical", "Medical recuperation"))

    # Activity & filter
    conn.execute("INSERT INTO activities(student_id, title, activity_type, organization, activity_date) VALUES(?,?,?,?,?)",
                 (s_id, "Smart India Hackathon", "Technical", "AICTE", "2023-09-15"))
    conn.execute("INSERT INTO activities(student_id, title, activity_type, organization, activity_date) VALUES(?,?,?,?,?)",
                 (s_id, "Inter-College Cricket", "Extra-curricular", "Sports Club", "2024-02-10"))

    # Seminar
    conn.execute("INSERT INTO seminars(student_id, title, seminar_scope, organizer, seminar_date) VALUES(?,?,?,?,?)",
                 (s_id, "Deep Learning Workshop", "External", "IIT Bombay", "2023-11-05"))

    # Certificate
    conn.execute("INSERT INTO certificates(student_id, title, issuer, category, issue_date) VALUES(?,?,?,?,?)",
                 (s_id, "Deep Learning Specialization", "Coursera / Deeplearning.ai", "Course", "2023-12-01"))
    conn.commit()

    print("[7/8] Testing CGPA Predictor Math & Assumptions...")
    # Completed = 2 semesters, current CGPA = 8.5
    current_cgpa = 8.5
    completed_sems = 2
    total_prog_sems = 8
    target_cgpa = 9.0

    rem = total_prog_sems - completed_sems # 6
    req = ((target_cgpa * total_prog_sems) - (current_cgpa * completed_sems)) / rem
    # (9.0*8 - 8.5*2)/6 = (72 - 17)/6 = 55/6 = 9.1666...
    assert round(req, 2) == 9.17

    # Impossible target test: target 9.9
    impossible_req = ((9.9 * total_prog_sems) - (current_cgpa * completed_sems)) / rem
    # (9.9*8 - 17)/6 = (79.2 - 17)/6 = 62.2/6 = 10.366... > 10.0
    assert impossible_req > 10.0

    print("[8/8] Testing Student CASCADE Deletion...")
    conn.execute("DELETE FROM students WHERE id=?", (s_id,))
    conn.commit()

    # Check that all dependent tables are emptied for this student
    assert conn.execute("SELECT COUNT(*) FROM school_records WHERE student_id=?", (s_id,)).fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM semester_results WHERE student_id=?", (s_id,)).fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM subject_marks").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?", (s_id,)).fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM gap_years WHERE student_id=?", (s_id,)).fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM activities WHERE student_id=?", (s_id,)).fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM seminars WHERE student_id=?", (s_id,)).fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM certificates WHERE student_id=?", (s_id,)).fetchone()[0] == 0

    # Subject is now unreferenced, so deletion must succeed
    conn.execute("DELETE FROM subjects WHERE id=?", (sub1_id,))
    conn.execute("DELETE FROM subjects WHERE id=?", (sub2_id,))
    conn.commit()
    assert conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0] == 0

    conn.close()
    if os.path.exists(DB_TEST):
        try: os.remove(DB_TEST)
        except: pass

    print("==================================================================")
    print(">>> ALL 8 FULL LIFECYCLE DBMS & BUSINESS LOGIC TESTS PASSED! <<<")
    print("==================================================================")

if __name__ == "__main__":
    test_full_lifecycle()
