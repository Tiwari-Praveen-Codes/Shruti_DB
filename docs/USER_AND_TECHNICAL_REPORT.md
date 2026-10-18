# ScholarTrack — User & Technical DBMS Report

## 1. Executive Summary & Architecture Overview

**ScholarTrack** is a 3NF-normalized Relational Database Management System (RDBMS) paired with an interactive Python/Streamlit intelligence interface. It is built to maintain student master records, monitor academic grade point progression (SGPA/CGPA), track attendance and defaulter risks, manage co-curricular portfolios, and mirror data in real time to **Google Sheets**.

### System Architecture
- **Primary Relational Engine**: MySQL 8.0 (Database: `Shruti_41`, User: `Shruti_41`, Port: `3306`)
- **Web Interface**: Python 3.10+ / Streamlit Enterprise Framework
- **Data Visualization**: Altair Declarative Statistical Charts & Pandas DataFrames
- **Real-Time Cloud Mirror**: Google Sheets via Apps Script Webhook API (`sync_all` & incremental sync)
- **Zero-Config Standby Fallback**: SQLite (`scholartrack.db`) for isolated container deployments
- **Dataset**: 100 distinct students with `@viva-technology.org` email addresses and over 3,400 linked progression records.

---

## 2. Step-by-Step Operational Guide (GUI & Sync Feature)

### 2.1 Navigation & Workspace Layout
The application features a clean sidebar navigation with 11 specialized modules:
1. **📊 Student Analytics (360°)**: Comprehensive individual student performance dossier.
2. **Dashboard**: High-level institutional KPI metrics, department distributions, and batch summaries.
3. **Student Directory**: Student profile management (CRUD operations).
4. **SSC / HSC**: Prior secondary and higher-secondary academic history.
5. **Semester Results**: SGPA, CGPA, pass/fail status, and active backlog records.
6. **Subjects & Marks**: Course catalogue management and examination marks recording.
7. **Attendance**: Lecture surveillance, class participation, and defaulter warnings.
8. **Academic Gaps**: Documented educational interruptions with reasons.
9. **Portfolio**: Co-curricular, extra-curricular, and technical achievements.
10. **Certificates**: Professional certifications and dynamic Target CGPA Forecaster.
11. **Google Sheets Sync**: Manual webhook testing and sync status dashboard.

### 2.2 Using the 360° Student Analytics Dossier
1. Navigate to **`📊 Student Analytics (360°)`** in the sidebar.
2. In the **🔍 Search Student** field, type a name (e.g. `Shruti`), roll number (e.g. `41`), or department (`Computer Science`). The dropdown automatically filters matching students.
3. Select a student from the **Select Student Dossier** dropdown.
4. The system immediately renders:
   - **Student Profile Header Card**: Roll number, department, admission year, status, and email.
   - **Summary KPI Badges**: Semesters completed, active backlog count, overall attendance percentage, and portfolio accolades count.
   - **Progression Trendline**: Dual-series Altair chart plotting SGPA and CGPA per semester against the institutional 7.00 First Class benchmark.
   - **Marks vs Benchmark Chart**: Grouped bars comparing the student's percentage in each subject against institutional minimum passing thresholds.
   - **Attendance Surveillance**: Bar chart with a dashed red line at the mandatory 75% attendance threshold, dynamically flagging Defaulter Risk.
   - **Component Donut Chart**: Breakdown of marks across Final, Internal, External, and Practical assessments.
   - **Target CGPA Forecaster**: Interactive slider calculating the required future SGPA average needed to achieve a target CGPA.

### 2.3 Operating the Google Sheets Live Sync
ScholarTrack features **dual-mode synchronization**:

#### A. Automated Real-Time Background Sync (Zero-Click)
- Every time a user adds, edits, or deletes a record in any table through the GUI, the database abstraction layer (`run()`) automatically invokes a background daemon thread (`auto_sync_to_sheets()`).
- The thread packages the changes and sends an authenticated HTTP POST payload to the Google Apps Script Webhook.
- Changes appear in the corresponding worksheet tab on Google Sheets within 1–2 seconds without freezing the user interface.

#### B. Manual On-Demand Full Sync
1. In the sidebar under the **Sheets Connected** badge, click **🔄 Sync with Google Sheets Now**.
2. A progress spinner will activate while all 10 normalized tables (over 3,400 rows) are serialized and transmitted.
3. Upon completion, a green toast notification will display:
   `✅ Google Apps Script synced 10 tables with 3400+ total records successfully!`
4. Alternatively, open the **Google Sheets Sync** page from the sidebar to inspect the webhook URL or view synchronization diagnostics.

---

## 3. Instructions on How to Modify & Update Records

### 3.1 Modifying Records via the GUI

Every transactional entity page (**Student Directory**, **SSC / HSC**, **Semester Results**, **Subjects & Marks**, **Attendance**) provides dedicated sub-tabs:

#### A. Updating via the "✏️ Edit Record" Tab
1. Navigate to the relevant entity page (e.g., **SSC / HSC**).
2. Click on the **✏️ Edit Record** tab.
3. Open the **Select record to edit** dropdown:
   - Records are labeled with student roll numbers, names, and identifiers (e.g., `41 — Shruti Patil [SSC] (ID 81)`).
4. The form automatically pre-populates with the record's current values.
5. Modify the desired fields (e.g., update `Marks obtained`, `Board`, or `Passing year`).
6. Click the primary **Update Record** button:
   - The system validates input ranges, recalculates derived values (such as percentage), executes `UPDATE`, displays a success confirmation, updates the live data table, and pushes the changes to Google Sheets.

#### B. Updating via Smart "➕ Add Record" (Auto-Upsert)
- If a user inputs data for a record where a unique candidate key already exists (for example, entering an SSC record for a student who already has one):
  - Rather than rejecting the submission with a raw database duplicate error, ScholarTrack's intelligent **Auto-Upsert** layer detects the existing row ID.
  - It safely updates the existing record with the newly submitted values and confirms:
    `✅ Existing SSC record updated successfully (485.0/500.0 = 97.0%).`

#### C. Deleting Records Safely ("🗑️ Delete Record" Tab)
1. Switch to the **🗑️ Delete Record** tab.
2. Select the target record from the selector dropdown.
3. Review the preview card detailing the record's attributes.
4. Click **Confirm Delete**:
   - For students: Cascades and automatically deletes linked school records, semester results, marks, attendance, and certificates.
   - For subjects: If marks or attendance records reference the subject, deletion is blocked by referential integrity (`RESTRICT`), and a clear warning prompt is presented to protect historical evaluation data.

### 3.2 Modifying Records via MySQL Direct Queries (CLI / Admin)
To perform administrative updates directly in the MySQL database:

```sql
-- 1. Connect to MySQL
mysql -u Shruti_41 -p Shruti_41

-- 2. Update a student's contact email and status
UPDATE students 
SET email = 'shruti.patil@viva-technology.org', current_status = 'Active' 
WHERE roll_number = '41';

-- 3. Update school marks and percentage
UPDATE school_records 
SET marks_obtained = 485.0, marks_total = 500.0, percentage = 97.00 
WHERE student_id = 41 AND level = 'SSC';

-- 4. Update semester SGPA and result status
UPDATE semester_results 
SET sgpa = 9.40, cgpa = 9.25, result_status = 'Pass', backlog_count = 0 
WHERE student_id = 41 AND semester_number = 1;

-- 5. Update attendance lecture counts
UPDATE attendance 
SET classes_held = 50, classes_attended = 46 
WHERE student_id = 41 AND subject_id = 1 AND semester_number = 1;
```

---

## 4. Summary of Enforced Schema Constraints & Violation Handling

ScholarTrack enforces database integrity at both the **RDBMS Engine Level** (MySQL DDL constraints) and the **Application Form Validation Layer** before query execution.

### 4.1 Schema Constraints Matrix

| Table | Constraint Type | Column(s) / Condition | Business Rule Enforced |
| :--- | :--- | :--- | :--- |
| `students` | `PRIMARY KEY` | `id AUTO_INCREMENT` | Unique student surrogate identifier. |
| `students` | `UNIQUE KEY` | `roll_number` | No two students may share the same roll number. |
| `students` | `UNIQUE KEY` | `email` | Institutional email addresses must be unique. |
| `students` | `CHECK` | `admission_year BETWEEN 1990 AND 2100` | Admission year must be plausible. |
| `students` | `CHECK` | `current_status IN ('Active','Graduated','On Hold','Discontinued')` | Status must match institutional lifecycle states. |
| `school_records` | `FOREIGN KEY` | `student_id REFERENCES students(id) ON DELETE CASCADE` | Records belong to valid students; purged if student is removed. |
| `school_records` | `UNIQUE KEY` | `(student_id, level)` | A student may possess only one SSC and one HSC record. |
| `school_records` | `CHECK` | `level IN ('SSC','HSC')` | Record type restricted to SSC or HSC. |
| `school_records` | `CHECK` | `marks_obtained >= 0 AND marks_obtained <= marks_total` | Obtained marks cannot exceed total marks. |
| `school_records` | `CHECK` | `percentage BETWEEN 0 AND 100` | Percentage must strictly fall between 0.00% and 100.00%. |
| `semester_results` | `FOREIGN KEY` | `student_id REFERENCES students(id) ON DELETE CASCADE` | Progression tracks valid students; cascades on removal. |
| `semester_results` | `UNIQUE KEY` | `(student_id, semester_number)` | Exactly one result record per student per semester. |
| `semester_results` | `CHECK` | `semester_number BETWEEN 1 AND 12` | Semester index must fall within academic boundaries (1–12). |
| `semester_results` | `CHECK` | `sgpa BETWEEN 0.00 AND 10.00 AND cgpa BETWEEN 0.00 AND 10.00` | Grade point averages must strictly adhere to the 10-point scale. |
| `semester_results` | `CHECK` | `result_status IN ('Pass','ATKT','Fail','Pending')` | Result status restricted to authorized values. |
| `semester_results` | `CHECK` | `backlog_count >= 0` | Backlog count cannot be negative. |
| `subjects` | `PRIMARY KEY` | `id AUTO_INCREMENT` | Unique subject surrogate identifier. |
| `subjects` | `UNIQUE KEY` | `subject_code` | Course codes (e.g. `CS301`) must be globally unique. |
| `subjects` | `CHECK` | `subject_type IN ('Theory','Lab')` | Subject classification restricted to Theory or Lab. |
| `subjects` | `CHECK` | `credits >= 0` | Course credits cannot be negative. |
| `subject_marks` | `FOREIGN KEY` | `semester_result_id REFERENCES semester_results(id) ON DELETE CASCADE` | Marks link to an existing semester result record. |
| `subject_marks` | `FOREIGN KEY` | `subject_id REFERENCES subjects(id) ON DELETE RESTRICT` | Prevents deletion of subjects that have existing evaluation records. |
| `subject_marks` | `UNIQUE KEY` | `(semester_result_id, subject_id)` | Prevents duplicate mark entries for the same course in a semester. |
| `subject_marks` | `CHECK` | `marks_obtained >= 0 AND marks_obtained <= marks_total` | Marks obtained cannot exceed the exam total. |
| `subject_marks` | `CHECK` | `passing_marks >= 0 AND passing_marks <= marks_total` | Passing threshold must be a valid sub-score of total marks. |
| `subject_marks` | `CHECK` | `component IN ('Internal','External','Practical','Final')` | Evaluation component restricted to authorized categories. |
| `attendance` | `FOREIGN KEY` | `student_id REFERENCES students(id) ON DELETE CASCADE` | Attendance links to valid enrolled students. |
| `attendance` | `FOREIGN KEY` | `subject_id REFERENCES subjects(id) ON DELETE RESTRICT` | Prevents deletion of courses with attendance logs. |
| `attendance` | `UNIQUE KEY` | `(student_id, subject_id, academic_year, semester_number)` | Exactly one attendance summary per student per subject per term. |
| `attendance` | `CHECK` | `classes_attended <= classes_held` | Attended lectures cannot exceed conducted lectures. |
| `gap_years` | `FOREIGN KEY` | `student_id REFERENCES students(id) ON DELETE CASCADE` | Interruption logs belong to registered students. |
| `gap_years` | `CHECK` | `end_year >= start_year` | Interruption conclusion year must equal or exceed start year. |

---

### 4.2 Error Handling & User Translation (`format_db_error`)

When an unexpected database violation occurs, raw low-level database errors are intercepted by `format_db_error()` in `app.py` and converted into clear, user-friendly diagnostic banners:

| Database Error Code / Signature | Root Cause | User Interface Notification |
| :--- | :--- | :--- |
| **MySQL 1062** / `roll_number` | Attempt to register an existing roll number | `Duplicate Roll Number rejected: A student with this roll number already exists.` |
| **MySQL 1062** / `email` | Attempt to register a duplicate email address | `Duplicate Email rejected: A student with this email address already exists.` |
| **MySQL 1062** / `subject_code` | Attempt to add duplicate course code | `Duplicate Subject Code rejected: A subject with this code already exists.` |
| **MySQL 1062** / `level` | Duplicate SSC or HSC entry (bypassing upsert) | `Duplicate School Record: This student already has an SSC/HSC record for this level.` |
| **MySQL 1062** / `semester_number` | Duplicate semester result entry | `Duplicate Semester Result: A record for this student and semester number already exists.` |
| **MySQL 1062** / `subject_id` | Duplicate marks entry for a course in a term | `Duplicate Subject Mark: Marks for this subject have already been entered for this semester.` |
| **MySQL 1451** / `FOREIGN KEY RESTRICT` | Attempting to delete a subject referenced in marks/attendance | `Referential Integrity Restriction (RESTRICT): Cannot delete this record because dependent records reference it. Delete or reassign referencing marks/attendance records first.` |
| **MySQL 1452** / `FOREIGN KEY` | Missing parent foreign key reference | `Referential Integrity Violation: The referenced student or subject does not exist.` |
| **MySQL 3819** / `CHECK constraint` | Value outside valid range (e.g. attended > held) | `Check Constraint Violation: [Specific column range violation explanation]` |

---

## 5. Verification & Testing Evidence

The system has been verified against a dedicated automated test suite ([test_suite.py](file:///c:/Users/pt489/OneDrive/Desktop/DBMS_41/Student_Progress_track_DBMS_Project/test_suite.py)):
- **3NF Normalization**: Passed (Profile facts isolated in `students`; courses decoupled in `subjects`; evaluations in `subject_marks`).
- **Cascade Deletion**: Passed (Deleting student ID cascades to school records, results, attendance, and achievements without orphaned rows).
- **Restrict Integrity**: Passed (Deleting a course referenced by active marks is prevented with HTTP/SQL 1451).
- **Range Constraints**: Passed (Invalid marks, invalid SGPA/CGPA, and inverted attendance values are rejected).
- **Google Sheets Live Sync**: Verified (All 10 worksheet tables confirmed receiving live payloads via Apps Script Webhook).
