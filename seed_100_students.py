import random
import os
import sqlite3
import mysql.connector

FIRST_NAMES = [
    "Shruti", "Rohan", "Ananya", "Aditya", "Sneha", "Aarav", "Pooja", "Siddharth", "Meera", "Kunal",
    "Neha", "Varun", "Riya", "Tanmay", "Ishita", "Harsh", "Divya", "Pranav", "Aniket", "Tanvi",
    "Yash", "Shreya", "Rahul", "Manasi", "Omkar", "Sakshi", "Tejas", "Aishwarya", "Parth", "Rutuja",
    "Vikrant", "Sanika", "Akshay", "Aditi", "Sahil", "Prachi", "Abhishek", "Gayatri", "Mayur", "Disha",
    "Saurabh", "Kalyani", "Gaurav", "Nikita", "Chinmay", "Rashmi", "Tushar", "Pallavi", "Mandar", "Sayali",
    "Nikhil", "Payal", "Swapnil", "Vaishnavi", "Rohit", "Janhavi", "Kedar", "Revati", "Sanket", "Samiksha",
    "Suraj", "Ketaki", "Nilesh", "Poonam", "Sandeep", "Komal", "Deepak", "Deepali", "Vishal", "Ashwini",
    "Ganesh", "Yogita", "Mahesh", "Sonali", "Chetan", "Radhika", "Sagar", "Priyanka", "Prasad", "Mohini",
    "Bhushan", "Swati", "Avinash", "Rupali", "Milind", "Madhuri", "Amol", "Sarika", "Sachin", "Pratibha",
    "Shrikant", "Rohini", "Ajinkya", "Anita", "Amit", "Namrata", "Sameer", "Rupesh", "Vinayak", "Dhanashree"
]

LAST_NAMES = [
    "Patil", "Verma", "Deshmukh", "Kulkarni", "Joshi", "Sharma", "Iyer", "Gupta", "Shinde", "More",
    "Pawar", "Kadam", "Jadhav", "Chavan", "Kale", "Bhosale", "Gaikwad", "Tambe", "Sawant", "Salunkhe",
    "Thorat", "Jagtap", "Naik", "Rao", "Bhat", "Prabhu", "Shenoy", "Kamat", "Hegde", "Pai",
    "Shetty", "Nambiar", "Menon", "Nair", "Pillai", "Varma", "Reddy", "Naidu", "Choudhury", "Das",
    "Banerjee", "Mukherjee", "Chatterjee", "Sen", "Dutta", "Roy", "Ghosh", "Bose", "Bhattacharya", "Chakraborty",
    "Mishra", "Pandey", "Tiwari", "Dubey", "Tripathi", "Shukla", "Awasthi", "Saxena", "Srivastava", "Agarwal",
    "Singhania", "Goel", "Bansal", "Mittal", "Garg", "Jain", "Mehta", "Shah", "Parekh", "Vora",
    "Kapoor", "Khanna", "Malhotra", "Chopra", "Bhatia", "Arora", "Sethi", "Kohli", "Dhawan", "Suri",
    "Bhardwaj", "Chauhan", "Rathore", "Tomar", "Solanki", "Parmar", "Gohil", "Zala", "Vaghela", "Sisodiya",
    "Bhatnagar", "Mathur", "Asthana", "Kulshrestha", "Nigam", "Johari", "Khatri", "Soni", "Lakhani", "Bavishi"
]

SUBJECTS_CATALOG = [
    ("CS101", "Engineering Mathematics I", "Theory", 4.0),
    ("CS102", "Applied Physics & Mechanics", "Theory", 3.0),
    ("CS103", "Basic Electrical & Electronics Lab", "Lab", 2.0),
    ("CS201", "Engineering Mathematics II", "Theory", 4.0),
    ("CS202", "Structured Programming in C/C++", "Theory", 4.0),
    ("CS203", "Programming Practice Lab", "Lab", 2.0),
    ("CS301", "Data Structures & Algorithms", "Theory", 4.0),
    ("CS302", "Database Management Systems", "Theory", 4.0),
    ("CS303", "DBMS & SQL Laboratory", "Lab", 2.0),
    ("CS401", "Operating Systems & Concurrency", "Theory", 4.0),
    ("CS402", "Computer Networks & Protocols", "Theory", 4.0),
    ("CS403", "Networks Simulation Lab", "Lab", 2.0),
    ("CS501", "Machine Learning & AI", "Theory", 4.0),
    ("CS502", "Software Engineering & Agile", "Theory", 3.0),
    ("CS503", "Cloud Computing & DevOps Lab", "Lab", 2.0),
    ("CS601", "Distributed Systems & Cloud", "Theory", 4.0),
    ("CS602", "Cybersecurity & Cryptography", "Theory", 3.0),
    ("CS603", "Full Stack Web Development Lab", "Lab", 2.0),
]

SEM_SUBJECT_MAP = {
    1: ["CS101", "CS102", "CS103"],
    2: ["CS201", "CS202", "CS203"],
    3: ["CS301", "CS302", "CS303"],
    4: ["CS401", "CS402", "CS403"],
    5: ["CS501", "CS502", "CS503"],
    6: ["CS601", "CS602", "CS603"],
}

ACAD_YEAR_MAP = {
    (2021, 1): "2021-22", (2021, 2): "2021-22",
    (2021, 3): "2022-23", (2021, 4): "2022-23",
    (2021, 5): "2023-24", (2021, 6): "2023-24",
    (2022, 1): "2022-23", (2022, 2): "2022-23",
    (2022, 3): "2023-24", (2022, 4): "2023-24",
    (2022, 5): "2024-25",
    (2023, 1): "2023-24", (2023, 2): "2023-24",
    (2023, 3): "2024-25",
    (2024, 1): "2024-25"
}

def seed_database(target="MySQL"):
    print(f"\n==========================================")
    print(f"SEEDING 100 REAL-TIME STUDENTS INTO {target}")
    print(f"==========================================")

    if target == "MySQL":
        conn = mysql.connector.connect(
            host='localhost',
            user='Shruti_41',
            password='Pravin@_123',
            database='Shruti_41'
        )
        cur = conn.cursor()
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        for tbl in ["certificates", "seminars", "activities", "gap_years", "attendance", "subject_marks", "semester_results", "school_records", "subjects", "students"]:
            cur.execute(f"TRUNCATE TABLE `{tbl}`")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
    else:
        db_path = "scholartrack.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = OFF")
        for tbl in ["certificates", "seminars", "activities", "gap_years", "attendance", "subject_marks", "semester_results", "school_records", "subjects", "students"]:
            cur.execute(f"DELETE FROM {tbl}")
        cur.execute("PRAGMA foreign_keys = ON")
        conn.commit()

    # 1. Insert Master Subjects
    ph = "%s" if target == "MySQL" else "?"
    for code, name, typ, cr in SUBJECTS_CATALOG:
        cur.execute(f"INSERT INTO subjects (subject_code, subject_name, subject_type, credits) VALUES ({ph}, {ph}, {ph}, {ph})",
                    (code, name, typ, cr))
    conn.commit()

    cur.execute("SELECT id, subject_code FROM subjects")
    sub_map = {row[1]: row[0] for row in cur.fetchall()}

    # 2. Prepare 100 Students
    rolls = ['41', '42', '43'] + [str(r) for r in range(1, 41)] + [str(r) for r in range(44, 101)]
    dept_cycle = [
        "Computer Science & Engineering",
        "Information Technology",
        "Artificial Intelligence & Data Science",
        "Electronics & Telecommunication",
        "Mechanical Engineering"
    ]

    random.seed(4141)  # deterministic realistic generation

    for i in range(100):
        roll = rolls[i]
        first = FIRST_NAMES[i]
        last = LAST_NAMES[i]
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}@viva-technology.org"
        dept = dept_cycle[i % len(dept_cycle)]

        if roll in ['41', '42']:
            adm_year = 2022
            status = 'Active'
        elif roll == '43':
            adm_year = 2023
            status = 'Active'
        else:
            if i < 40:
                adm_year = 2022
            elif i < 70:
                adm_year = 2023
            elif i < 90:
                adm_year = 2021
            else:
                adm_year = 2024
            status = 'Graduated' if adm_year == 2021 and i % 3 == 0 else 'Active'

        cur.execute(f"""
            INSERT INTO students (roll_number, full_name, email, department, admission_year, current_status)
            VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
        """, (roll, name, email, dept, adm_year, status))

    conn.commit()

    cur.execute("SELECT id, roll_number FROM students")
    student_map = {row[1]: row[0] for row in cur.fetchall()}

    # 3. Insert School Records, Semesters, Marks, Attendance, Activities
    BOARDS = ["Maharashtra State Board", "CBSE", "ICSE"]

    for i in range(100):
        roll = rolls[i]
        s_id = student_map[roll]
        first = FIRST_NAMES[i]
        last = LAST_NAMES[i]

        if roll == '41':
            adm_year = 2022
        elif roll == '42':
            adm_year = 2022
        elif roll == '43':
            adm_year = 2023
        else:
            if i < 40:
                adm_year = 2022
            elif i < 70:
                adm_year = 2023
            elif i < 90:
                adm_year = 2021
            else:
                adm_year = 2024

        # SSC & HSC
        ssc_yr = adm_year - 2
        hsc_yr = adm_year
        board = BOARDS[i % len(BOARDS)]

        if roll == '41': # Shruti
            ssc_pct, hsc_pct = 96.4, 93.33
        elif roll == '42':
            ssc_pct, hsc_pct = 92.0, 88.5
        elif roll == '43':
            ssc_pct, hsc_pct = 94.2, 90.0
        else:
            ssc_pct = round(random.uniform(75.0, 97.0), 2)
            hsc_pct = round(random.uniform(70.0, 95.0), 2)

        cur.execute(f"""
            INSERT INTO school_records (student_id, level, board, passing_year, marks_obtained, marks_total, percentage)
            VALUES ({ph}, 'SSC', {ph}, {ph}, {ph}, 500, {ph})
        """, (s_id, board, ssc_yr, round(ssc_pct * 5.0, 1), ssc_pct))

        cur.execute(f"""
            INSERT INTO school_records (student_id, level, board, passing_year, marks_obtained, marks_total, percentage)
            VALUES ({ph}, 'HSC', {ph}, {ph}, {ph}, 600, {ph})
        """, (s_id, board, hsc_yr, round(hsc_pct * 6.0, 1), hsc_pct))

        # Semesters
        if adm_year == 2021:
            sem_count = 6
        elif adm_year == 2022:
            sem_count = 5
        elif adm_year == 2023:
            sem_count = 3
        else:
            sem_count = 1

        base_gpa = 9.0 if roll == '41' else (8.5 if roll in ['42', '43'] else round(random.uniform(6.8, 9.2), 2))
        running_gpas = []
        has_gap = (i % 15 == 0 and sem_count >= 3)

        for sem_num in range(1, sem_count + 1):
            acad_yr = ACAD_YEAR_MAP.get((adm_year, sem_num), "2024-25")
            noise = round(random.uniform(-0.35, 0.45), 2)
            sgpa = min(10.0, max(5.5, round(base_gpa + noise, 2)))
            if roll == '41': # Shruti custom pristine progression
                sgpa_map = {1: 8.65, 2: 8.90, 3: 9.20, 4: 9.45, 5: 9.30}
                sgpa = sgpa_map[sem_num]
            running_gpas.append(sgpa)
            cgpa = round(sum(running_gpas) / len(running_gpas), 2)

            is_gap_after = 1 if (has_gap and sem_num == 2) else 0
            is_atkt = (sgpa < 6.0 and sem_num > 1 and roll not in ['41', '42', '43'])
            res_status = "ATKT" if is_atkt else "Pass"
            backlog_count = random.choice([1, 2]) if is_atkt else 0

            cur.execute(f"""
                INSERT INTO semester_results (student_id, semester_number, academic_year, sgpa, cgpa, result_status, backlog_count, is_gap_after)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            """, (s_id, sem_num, acad_yr, sgpa, cgpa, res_status, backlog_count, is_gap_after))

            sem_res_id = cur.lastrowid

            # Subject marks for this semester
            assigned_subs = SEM_SUBJECT_MAP.get(sem_num, ["CS101", "CS102", "CS103"])
            for sub_code in assigned_subs:
                sb_id = sub_map[sub_code]
                is_lab = "Lab" in sub_code or sub_code in ["CS103", "CS203", "CS303", "CS403", "CS503", "CS603"]
                tot = 50.0 if is_lab else 100.0
                pass_m = 20.0 if is_lab else 40.0
                comp = "Practical" if is_lab else ("Final" if random.random() > 0.3 else "Internal")

                # Realistic marks
                pct = sgpa / 10.0
                if roll == '41':
                    pct = 0.92
                marks_obt = min(tot, max(pass_m - 2 if is_atkt else pass_m + 5, round(tot * pct + random.uniform(-4, 4), 1)))

                cur.execute(f"""
                    INSERT INTO subject_marks (semester_result_id, subject_id, marks_obtained, marks_total, passing_marks, component)
                    VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
                """, (sem_res_id, sb_id, marks_obt, tot, pass_m, comp))

                # Attendance entry
                classes_held = 30 if is_lab else random.choice([40, 44, 48])
                # Make ~8 students have <75% attendance to trigger defaulter analytics
                if i % 11 == 0 and roll not in ['41', '42', '43']:
                    att_ratio = random.uniform(0.60, 0.73)
                else:
                    att_ratio = random.uniform(0.80, 0.97)

                if roll == '41':
                    att_ratio = 0.72 if sub_code == 'CS402' else random.uniform(0.92, 0.97)

                classes_att = int(round(classes_held * att_ratio))

                cur.execute(f"""
                    INSERT INTO attendance (student_id, subject_id, academic_year, semester_number, classes_held, classes_attended)
                    VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
                """, (s_id, sb_id, acad_yr, sem_num, classes_held, classes_att))

        # Gap year record
        if has_gap:
            cur.execute(f"""
                INSERT INTO gap_years (student_id, start_year, end_year, reason_category, notes)
                VALUES ({ph}, {ph}, {ph}, 'Medical', 'Medical leave and recovery sanctioned by university academic board.')
            """, (s_id, adm_year + 1, adm_year + 2))

        # Accolades for students
        if i % 2 == 0 or roll in ['41', '42', '43']:
            act_titles = [
                ("Smart India Hackathon National Finalist", "Technical", "AICTE & MoE", "2024-09-20", "Built smart healthcare analytics portal."),
                ("ACM-ICPC Algorithmic Challenge — Rank 12", "Technical", "ACM Student Chapter", "2024-02-15", "Competitive graph and DP problem solving."),
                ("Inter-Collegiate Technical Symposium Lead", "Co-curricular", "VIVA Technology CSI Branch", "2024-03-10", "Chaired technical paper presentation committee."),
                ("College Robotics Club Winner", "Technical", "Robotics Club", "2023-11-22", "Autonomous line follower and maze solver."),
                ("State Level Debate Championship — 2nd Prize", "Extra-curricular", "Youth Affairs Council", "2023-10-05", "Debated on AI ethics and data sovereignty.")
            ]
            t = act_titles[i % len(act_titles)]
            cur.execute(f"""
                INSERT INTO activities (student_id, title, activity_type, organization, activity_date, description)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            """, (s_id, t[0], t[1], t[2], t[3], t[4]))

            sem_titles = [
                ("Cloud Native Architecture & Microservices", "External", "Google Developer Groups", "2024-04-12", "https://viva-technology.org/verify/sem-cloud"),
                ("Advanced Distributed Database Engineering", "Internal", "Department of CSE", "2024-08-18", "https://viva-technology.org/verify/sem-dbms"),
                ("Foundations of Large Language Models & GenAI", "External", "IEEE Bombay Section", "2024-01-28", "https://viva-technology.org/verify/sem-ai")
            ]
            sm = sem_titles[i % len(sem_titles)]
            cur.execute(f"""
                INSERT INTO seminars (student_id, title, seminar_scope, organizer, seminar_date, certificate_url)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            """, (s_id, sm[0], sm[1], sm[2], sm[3], sm[4]))

            cert_titles = [
                ("AWS Certified Solutions Architect — Associate", "Amazon Web Services", "Course", "2024-06-15", "https://aws.amazon.com/verification/VIVA-9021", "Cloud architecture certification"),
                ("Oracle Certified Professional: Java SE 17", "Oracle University", "Course", "2023-12-10", "https://oracle.com/verify/VIVA-7842", "Backend systems and concurrency"),
                ("Deep Learning Specialization", "DeepLearning.AI / Coursera", "Course", "2024-02-20", "https://coursera.org/verify/VIVA-1184", "Neural networks and transformers"),
                ("NPTEL Elite Certificate in Database Management", "IIT Kharagpur / NPTEL", "Course", "2023-10-30", "https://nptel.ac.in/verify/VIVA-4402", "Top 5% candidate in 3NF and Query Optimization")
            ]
            c = cert_titles[i % len(cert_titles)]
            cur.execute(f"""
                INSERT INTO certificates (student_id, title, issuer, category, issue_date, credential_url, notes)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph}, {ph})
            """, (s_id, c[0], c[1], c[2], c[3], c[4], c[5]))

    conn.commit()

    # Verify counts
    cur.execute("SELECT COUNT(*) FROM students")
    st_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM semester_results")
    sr_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM subject_marks")
    sm_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM attendance")
    att_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM school_records")
    sc_count = cur.fetchone()[0]

    print(f"SUCCESS for {target}!")
    print(f"-> Students: {st_count} (target 100)")
    print(f"-> School Records: {sc_count}")
    print(f"-> Semester Results: {sr_count}")
    print(f"-> Subject Marks: {sm_count}")
    print(f"-> Attendance Records: {att_count}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    seed_database("MySQL")
    seed_database("SQLite")
    print("\nAll 100 students populated in MySQL and SQLite!")
