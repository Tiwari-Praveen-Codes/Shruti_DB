import os
import sqlite3

DB_TEST = "test_scholartrack.db"

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

def get_connection():
    c = sqlite3.connect(DB_TEST)
    c.execute("PRAGMA foreign_keys=ON")
    c.row_factory = sqlite3.Row
    return c

def run_test_ops():
    if os.path.exists(DB_TEST):
        try: os.remove(DB_TEST)
        except: pass
    
    conn = get_connection()
    conn.executescript(SCHEMA)

    # 1. Insert valid student
    cur = conn.cursor()
    cur.execute("INSERT INTO students(roll_number, full_name, email, department, admission_year) VALUES(?,?,?,?,?)",
                ("22EC01", "Alice Smith", "alice@example.com", "ECE", 2022))
    conn.commit()
    s_id = cur.lastrowid
    assert s_id > 0

    # 2. Reject duplicate roll
    try:
        conn.execute("INSERT INTO students(roll_number, full_name, email, department, admission_year) VALUES(?,?,?,?,?)",
                  ("22EC01", "Alice Duplicate", "alice2@example.com", "ECE", 2022))
        conn.commit()
        assert False, "Duplicate roll should fail"
    except sqlite3.IntegrityError:
        pass

    # 3. Reject duplicate email
    try:
        conn.execute("INSERT INTO students(roll_number, full_name, email, department, admission_year) VALUES(?,?,?,?,?)",
                  ("22EC02", "Bob Duplicate Email", "alice@example.com", "ECE", 2022))
        conn.commit()
        assert False, "Duplicate email should fail"
    except sqlite3.IntegrityError:
        pass

    # 4. SSC/HSC duplicate level for same student rejected
    conn.execute("INSERT INTO school_records(student_id, level, board, passing_year, marks_obtained, marks_total, percentage) VALUES(?,?,?,?,?,?,?)",
              (s_id, "SSC", "CBSE", 2020, 90, 100, 90.0))
    conn.commit()
    try:
        conn.execute("INSERT INTO school_records(student_id, level, board, passing_year, marks_obtained, marks_total, percentage) VALUES(?,?,?,?,?,?,?)",
                  (s_id, "SSC", "ICSE", 2020, 85, 100, 85.0))
        conn.commit()
        assert False, "Duplicate SSC record for same student should fail"
    except sqlite3.IntegrityError:
        pass

    # 5. SGPA/CGPA outside 0..10 rejected
    try:
        conn.execute("INSERT INTO semester_results(student_id, semester_number, academic_year, sgpa, cgpa, result_status) VALUES(?,?,?,?,?,?)",
                  (s_id, 1, "2022-23", 10.5, 9.0, "Pass"))
        conn.commit()
        assert False, "SGPA > 10 should fail"
    except sqlite3.IntegrityError:
        pass

    try:
        conn.execute("INSERT INTO semester_results(student_id, semester_number, academic_year, sgpa, cgpa, result_status) VALUES(?,?,?,?,?,?)",
                  (s_id, 1, "2022-23", 8.5, -0.5, "Pass"))
        conn.commit()
        assert False, "CGPA < 0 should fail"
    except sqlite3.IntegrityError:
        pass

    # Valid semester
    cur = conn.cursor()
    cur.execute("INSERT INTO semester_results(student_id, semester_number, academic_year, sgpa, cgpa, result_status) VALUES(?,?,?,?,?,?)",
                (s_id, 1, "2022-23", 8.5, 8.5, "Pass"))
    conn.commit()
    sem_id = cur.lastrowid

    # Duplicate semester_number for student rejected
    try:
        conn.execute("INSERT INTO semester_results(student_id, semester_number, academic_year, sgpa, cgpa, result_status) VALUES(?,?,?,?,?,?)",
                  (s_id, 1, "2022-23", 9.0, 9.0, "Pass"))
        conn.commit()
        assert False, "Duplicate semester for same student should fail"
    except sqlite3.IntegrityError:
        pass

    # 6. Subjects and duplicate subject code rejected
    cur = conn.cursor()
    cur.execute("INSERT INTO subjects(subject_code, subject_name, subject_type, credits) VALUES(?,?,?,?)",
                ("EC301", "Signals and Systems", "Theory", 4.0))
    conn.commit()
    sub_id = cur.lastrowid
    try:
        conn.execute("INSERT INTO subjects(subject_code, subject_name, subject_type, credits) VALUES(?,?,?,?)",
                  ("EC301", "Signals Clone", "Theory", 4.0))
        conn.commit()
        assert False, "Duplicate subject code should fail"
    except sqlite3.IntegrityError:
        pass

    # 7. Marks outside valid range rejected
    try:
        conn.execute("INSERT INTO subject_marks(semester_result_id, subject_id, marks_obtained, marks_total, passing_marks) VALUES(?,?,?,?,?)",
                  (sem_id, sub_id, 105, 100, 40))
        conn.commit()
        assert False, "Marks obtained > marks total should fail"
    except sqlite3.IntegrityError:
        pass

    cur = conn.cursor()
    cur.execute("INSERT INTO subject_marks(semester_result_id, subject_id, marks_obtained, marks_total, passing_marks) VALUES(?,?,?,?,?)",
                (sem_id, sub_id, 88, 100, 40))
    conn.commit()
    mark_id = cur.lastrowid

    # Duplicate subject mark for same semester result rejected
    try:
        conn.execute("INSERT INTO subject_marks(semester_result_id, subject_id, marks_obtained, marks_total, passing_marks) VALUES(?,?,?,?,?)",
                  (sem_id, sub_id, 75, 100, 40))
        conn.commit()
        assert False, "Duplicate subject mark for same semester result should fail"
    except sqlite3.IntegrityError:
        pass

    # 8. Attendance attended > held rejected
    try:
        conn.execute("INSERT INTO attendance(student_id, subject_id, academic_year, semester_number, classes_held, classes_attended) VALUES(?,?,?,?,?,?)",
                  (s_id, sub_id, "2022-23", 1, 30, 35))
        conn.commit()
        assert False, "Attended > held should fail"
    except sqlite3.IntegrityError:
        pass

    conn.execute("INSERT INTO attendance(student_id, subject_id, academic_year, semester_number, classes_held, classes_attended) VALUES(?,?,?,?,?,?)",
              (s_id, sub_id, "2022-23", 1, 40, 35))
    conn.commit()

    # 9. Gap end year before start year rejected
    try:
        conn.execute("INSERT INTO gap_years(student_id, start_year, end_year, reason_category) VALUES(?,?,?,?)",
                  (s_id, 2023, 2022, "Academic"))
        conn.commit()
        assert False, "End year < start year should fail"
    except sqlite3.IntegrityError:
        pass
    conn.execute("INSERT INTO gap_years(student_id, start_year, end_year, reason_category) VALUES(?,?,?,?)",
              (s_id, 2023, 2024, "Academic"))
    conn.commit()

    # 10. Subject deletion restricted while referenced by subject_marks or attendance
    try:
        conn.execute("DELETE FROM subjects WHERE id=?", (sub_id,))
        conn.commit()
        assert False, "Subject deletion should be restricted when referenced"
    except sqlite3.IntegrityError:
        pass

    # 11. Student deletion cascades dependent rows
    conn.execute("DELETE FROM students WHERE id=?", (s_id,))
    conn.commit()
    
    # Verify dependent rows are deleted
    n_sr = conn.execute("SELECT COUNT(*) FROM school_records WHERE student_id=?", (s_id,)).fetchone()[0]
    n_sem = conn.execute("SELECT COUNT(*) FROM semester_results WHERE student_id=?", (s_id,)).fetchone()[0]
    n_sm = conn.execute("SELECT COUNT(*) FROM subject_marks WHERE semester_result_id=?", (sem_id,)).fetchone()[0]
    n_att = conn.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?", (s_id,)).fetchone()[0]
    n_gap = conn.execute("SELECT COUNT(*) FROM gap_years WHERE student_id=?", (s_id,)).fetchone()[0]
    assert n_sr == 0, "school_records not cascaded"
    assert n_sem == 0, "semester_results not cascaded"
    assert n_sm == 0, "subject_marks not cascaded"
    assert n_att == 0, "attendance not cascaded"
    assert n_gap == 0, "gap_years not cascaded"

    # Now that student is deleted and marks/attendance are cascaded, subject deletion should succeed
    conn.execute("DELETE FROM subjects WHERE id=?", (sub_id,))
    conn.commit()
    n_sub = conn.execute("SELECT COUNT(*) FROM subjects WHERE id=?", (sub_id,)).fetchone()[0]
    assert n_sub == 0, "Unreferenced subject deletion should succeed"

    conn.close()
    if os.path.exists(DB_TEST):
        try: os.remove(DB_TEST)
        except: pass

    print("ALL 11 MANDATORY CONSTRAINT AND CASCADE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_test_ops()

