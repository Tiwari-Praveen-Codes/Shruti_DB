-- ==============================================================================
-- ScholarTrack Relational Database Schema (3NF Compliant)
-- SQLite 3 / Relational DBMS Schema Definition
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- 1. Students Entity (Profile facts only - 3NF)
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    department TEXT NOT NULL,
    admission_year INTEGER NOT NULL CHECK(admission_year BETWEEN 1990 AND 2100),
    current_status TEXT NOT NULL DEFAULT 'Active' CHECK(current_status IN ('Active','Graduated','On Hold','Discontinued'))
);

-- 2. School Records (SSC & HSC Prior Academic History)
CREATE TABLE IF NOT EXISTS school_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    level TEXT NOT NULL CHECK(level IN ('SSC','HSC')),
    board TEXT,
    passing_year INTEGER NOT NULL CHECK(passing_year BETWEEN 1990 AND 2100),
    marks_obtained REAL NOT NULL CHECK(marks_obtained >= 0),
    marks_total REAL NOT NULL CHECK(marks_total > 0 AND marks_obtained <= marks_total),
    percentage REAL NOT NULL CHECK(percentage BETWEEN 0 AND 100),
    UNIQUE(student_id, level)
);

-- 3. Semester Progression Results
CREATE TABLE IF NOT EXISTS semester_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    semester_number INTEGER NOT NULL CHECK(semester_number BETWEEN 1 AND 12),
    academic_year TEXT NOT NULL,
    sgpa REAL NOT NULL CHECK(sgpa BETWEEN 0 AND 10),
    cgpa REAL NOT NULL CHECK(cgpa BETWEEN 0 AND 10),
    result_status TEXT NOT NULL CHECK(result_status IN ('Pass','ATKT','Fail','Pending')),
    backlog_count INTEGER NOT NULL DEFAULT 0 CHECK(backlog_count >= 0),
    is_gap_after INTEGER NOT NULL DEFAULT 0 CHECK(is_gap_after IN (0, 1)),
    UNIQUE(student_id, semester_number)
);

-- 4. Subjects Catalogue (Reusable Theory / Lab Catalogue - 3NF)
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_code TEXT NOT NULL UNIQUE,
    subject_name TEXT NOT NULL,
    subject_type TEXT NOT NULL CHECK(subject_type IN ('Theory','Lab')),
    credits REAL NOT NULL DEFAULT 0 CHECK(credits >= 0)
);

-- 5. Examination Subject Marks (Links Semester Result & Subject)
CREATE TABLE IF NOT EXISTS subject_marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_result_id INTEGER NOT NULL REFERENCES semester_results(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    marks_obtained REAL NOT NULL CHECK(marks_obtained >= 0),
    marks_total REAL NOT NULL CHECK(marks_total > 0 AND marks_obtained <= marks_total),
    passing_marks REAL NOT NULL CHECK(passing_marks >= 0 AND passing_marks <= marks_total),
    component TEXT NOT NULL DEFAULT 'Final' CHECK(component IN ('Internal','External','Practical','Final')),
    UNIQUE(semester_result_id, subject_id)
);

-- 6. Attendance Surveillance (Per Student, Subject, Year, Semester)
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    academic_year TEXT NOT NULL,
    semester_number INTEGER NOT NULL CHECK(semester_number BETWEEN 1 AND 12),
    classes_held INTEGER NOT NULL CHECK(classes_held >= 0),
    classes_attended INTEGER NOT NULL CHECK(classes_attended >= 0 AND classes_attended <= classes_held),
    UNIQUE(student_id, subject_id, academic_year, semester_number)
);

-- 7. Academic Gaps & Interruptions
CREATE TABLE IF NOT EXISTS gap_years (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    start_year INTEGER NOT NULL,
    end_year INTEGER NOT NULL CHECK(end_year >= start_year),
    reason_category TEXT NOT NULL CHECK(reason_category IN ('Academic','Medical','Personal','Other')),
    notes TEXT
);

-- 8. Co-Curricular & Extra-Curricular Activities
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    activity_type TEXT NOT NULL CHECK(activity_type IN ('Technical','Co-curricular','Extra-curricular')),
    organization TEXT,
    activity_date TEXT,
    description TEXT
);

-- 9. Seminars & Workshops
CREATE TABLE IF NOT EXISTS seminars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    seminar_scope TEXT NOT NULL CHECK(seminar_scope IN ('Internal','External')),
    organizer TEXT,
    seminar_date TEXT,
    certificate_url TEXT
);

-- 10. Certificates & Credentials
CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    issuer TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Course','Hackathon','Internship','Achievement','Seminar','Other')),
    issue_date TEXT,
    credential_url TEXT,
    notes TEXT
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_student_name ON students(full_name);
CREATE INDEX IF NOT EXISTS idx_semester_student ON semester_results(student_id, semester_number);
CREATE INDEX IF NOT EXISTS idx_marks_subject ON subject_marks(subject_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id, semester_number);
