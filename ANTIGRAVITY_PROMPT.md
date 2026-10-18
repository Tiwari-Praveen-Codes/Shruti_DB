# ScholarTrack Antigravity Completion Prompt

Act as a senior full-stack engineer and DBMS examiner. Inspect and run this existing Streamlit/Python project before modifying it. The deadline is today: prioritize working, testable rubric features over redesign or unnecessary architecture.

## Existing features to preserve
Student directory, SSC/HSC, semester SGPA/CGPA and result/backlog status, Theory/Lab subject catalogue and marks, subject analytics, attendance, academic gaps, activity/seminar filters, certificates, CGPA target predictor, and one-way Google Sheets sync.

## Your tasks
1. Run the app and fix any runtime errors first.
2. Test all forms, SQL queries, filters, chart interactions and constraint errors.
3. Verify the schema is 3NF-oriented: profile data only in students, subject catalogue separate from marks/attendance, and portfolios in separate relations.
4. Add safe edit/update functionality where missing. Keep delete operations explicit and show clear errors.
5. If Google Sheets credentials are configured, test actual synchronization. Do not fake success. If a worksheet is missing, provide a clear error and setup instructions.
6. Improve accessibility and usability only after the core features pass.
7. Add a testing checklist and accurately document implemented vs incomplete features.
8. If the professor requires BigQuery/PostgreSQL/MySQL instead of SQLite, do not misrepresent the default database. Implement the required backend only after verifying project credentials/access.

## Mandatory checks
- Duplicate roll/email/subject code rejected.
- SGPA/CGPA outside 0..10 rejected.
- Marks outside valid range rejected.
- Attendance attended > held rejected.
- Duplicate student-semester and duplicate subject mark rejected.
- Student deletion cascades dependent rows.
- Subject deletion restricted while referenced.
- Gap end year before start year rejected.
- SGPA and CGPA trend graph uses live database records.
- Subject analytics include average percentages and fail attempts.
- Attendance threshold warning is accurate.
- Predictor states its equal-weight assumption.
- Sheets sync only reports success after the API confirms it.

At the end provide exact Windows commands, a tested feature checklist, remaining limitations, and a short table-by-table viva explanation.
