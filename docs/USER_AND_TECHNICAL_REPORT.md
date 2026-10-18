# ScholarTrack User & Technical DBMS Report

## 1. Executive Summary & Purpose
ScholarTrack is a normalized relational database management system (RDBMS) designed to evaluate student academic progression, attendance surveillance, and comprehensive portfolio achievements.

ScholarTrack connects natively to **MySQL** (using user `Shruti_41` and database `Shruti_41`), supports **Google Sheets API v4** for real-time cloud synchronization, and provides a dedicated **Individual Student Analytics (360°)** suite with a dynamic search menu and visual analytics.

---

## 2. MySQL `Shruti_41` Database Connection

ScholarTrack connects directly to the local MySQL 8.0 server:
- **Host**: `localhost:3306`
- **Database**: `Shruti_41`
- **User**: `Shruti_41`
- **Password**: `Pravin@_123`
- **Driver**: `mysql-connector-python` (version 26.7.0)

All 10 normalized tables have been created with full referential integrity (`FOREIGN KEY ... ON DELETE CASCADE`, `ON DELETE RESTRICT`), primary keys (`AUTO_INCREMENT`), domain `CHECK` constraints, and candidate keys (`UNIQUE KEY`).

A graceful fallback to local SQLite (`scholartrack.db`) is included, selectable via the sidebar backend toggle.

---

## 3. Dedicated Individual Student Analytics (360° View)

The **`📊 Student Analytics (360°)`** dashboard delivers student-centric evaluation:

### A. Dynamic Search Menu
- **Real-Time Search Bar**: Filter by Roll Number (e.g. `41`), Student Name (`Shruti`), or Department (`Computer Science`).
- **Interactive Dossier Selector**: Select any student to immediately load their complete profile and data records.
- **Profile Header Card**: Displays roll number, department, admission year, status, and contact details.

### B. Meaningful Visual Analytics Charts
1. **SGPA & CGPA Academic Progression Trendline (Altair)**:
   - Dual-series line chart tracking SGPA (semester GPA) and CGPA (cumulative GPA) across all completed semesters.
   - Distinct green dashed reference line at **7.00 CGPA** marking the First Class with Distinction benchmark.
   - Interactive tooltips with semester number, academic year, result status, and backlog count.
   - Academic interruption / gap warnings displayed automatically when flagged.
2. **Course Performance vs Passing Benchmark**:
   - Comparative grouped bar chart plotting the student's **Marks Obtained (%)** against the institutional **Min Passing Benchmark (%)** for each evaluated course.
   - Color-coded by Course Type (**Theory** vs **Lab**).
3. **Attendance Surveillance & Defaulter Risk**:
   - Subject-wise attendance bar chart with a red dashed reference line at the mandatory **75% threshold**.
   - Bars are dynamically color-coded: **Green (Eligible >= 75%)** and **Red (Defaulter Risk < 75%)**.
   - Defaulter alert banner warning students at risk of exam debarment.
4. **Assessment Component Composition**:
   - Donut chart displaying the distribution of marks across assessment components (`Final`, `Internal`, `External`, `Practical`).
5. **Portfolio & Achievement Accolades Summary**:
   - Total count and breakdown of Activities (Technical, Co-curricular, Extra-curricular), Seminars (Internal, External), and Verified Certifications.
6. **Student-Specific CGPA Target Forecaster**:
   - Dynamic slider to estimate required future SGPA averages per remaining semester based on current cumulative CGPA.

---

## 4. Google Sheets API Integration

ScholarTrack connects directly to Google Sheets API v4 to mirror the 10 normalized tables from MySQL (`Shruti_41`):
1. Authenticates using Google Service Account credentials.
2. Verifies the existence of all 10 worksheet tabs:
   `Students`, `School_Records`, `Semester_Results`, `Subjects`, `Subject_Marks`, `Attendance`, `Gap_Years`, `Activities`, `Seminars`, `Certificates`.
3. Performs a full transactional update and confirms live API status.

---

## 5. Quick Run & Testing Commands (PowerShell)

```powershell
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Run automated test suite
python test_suite.py

# 3. Launch live Streamlit app
python -m streamlit run app.py
```
App URL: [http://localhost:8502](http://localhost:8502)
