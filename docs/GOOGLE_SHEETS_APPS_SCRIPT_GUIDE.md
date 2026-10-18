# 📄 ScholarTrack — Google Sheets & Google Apps Script Connection Guide

This guide explains how to connect your **ScholarTrack Academic DBMS** (MySQL & SQLite) to your **Google Sheet** using **Google Apps Script**.

---

## 🚀 Why Use Google Apps Script?
- **Zero Google Cloud Project Setup**: No need to create service accounts, enable billing, or manage complex `.json` private keys.
- **Auto-Formatting**: Automatically generates all 10 normalized 3NF database tabs, colors headers (navy slate), freezes the top row, and auto-sizes columns.
- **Custom UI Menu**: Adds a native menu inside Google Sheets (`🎓 ScholarTrack DBMS`).
- **One-Click Sync**: Streams all 100 students, marks, attendance records, school records, and certificates straight into Google Sheets.

---

## 🛠️ Step-by-Step Setup (Takes Under 2 Minutes)

### Step 1: Open a Google Sheet
1. Open [Google Sheets](https://sheets.new) and create a new blank spreadsheet.
2. Title it: **`ScholarTrack Academic Progression DBMS`**.

---

### Step 2: Paste the Apps Script Code
1. In the top navigation bar of your Google Sheet, click **Extensions** &rarr; **Apps Script**.
2. Clear any default code in the editor (`function myFunction() { ... }`).
3. Open [`GoogleAppsScript.gs`](file:///c:/Users/pt489/OneDrive/Desktop/DBMS_41/Student_Progress_track_DBMS_Project/GoogleAppsScript.gs) in your project, copy the entire code, and paste it into the editor.
4. Click the **Save** icon (💾) or press `Ctrl + S`.
5. Name the Apps Script project: **`ScholarTrack Engine`**.

---

### Step 3: Deploy as a Web App (Webhook Endpoint)
1. In the top right corner of the Apps Script window, click the blue **Deploy** button &rarr; select **New deployment**.
2. Click the gear icon (**Select type**) next to "Select type" and choose **Web app**.
3. Configure the deployment settings:
   - **Description**: `ScholarTrack Live Sync`
   - **Execute as**: `Me (your-email@gmail.com)`
   - **Who has access**: **`Anyone`** *(Important: This allows the Streamlit app to post data without OAuth friction).*
4. Click **Deploy**.
5. When prompted with **Authorize access**, click **Authorize access** &rarr; choose your Google account &rarr; click **Advanced** &rarr; click **Go to ScholarTrack Engine (unsafe)** &rarr; click **Allow**.
6. Copy the generated **Web app URL** (it looks like `https://script.google.com/macros/s/AKfycb.../exec`).

---

### Step 4: Sync from the ScholarTrack Website
1. Open your live app at [http://localhost:8502](http://localhost:8502/).
2. In the sidebar, select **Google Sheets Sync**.
3. Under **⚡ Method 1: Google Apps Script Web App**, paste your **Web app URL**.
4. Click **🚀 Push All 10 Tables to Google Sheets via Apps Script**.
5. Switch back to your Google Sheet: All 10 tabs (`Students`, `School_Records`, `Semester_Results`, `Subjects`, `Subject_Marks`, `Attendance`, `Gap_Years`, `Activities`, `Seminars`, `Certificates`) will be created and populated with live records!

---

## 📑 The 10 Synchronized Database Tables

| Tab Name | Records Included |
| :--- | :--- |
| **`Students`** | 100 Students with `@viva-technology.org` emails, roll numbers 1–100, and departments |
| **`School_Records`** | SSC & HSC qualification marks, boards, passing years, and percentages |
| **`Semester_Results`** | Semester progression 1–6, SGPA, CGPA, pass status, and backlogs |
| **`Subjects`** | Master Course Catalogue (CS101 through CS603, Theory & Lab) |
| **`Subject_Marks`** | Evaluation records with components (Final, Internal, Practical) |
| **`Attendance`** | Class participation tracking, classes held vs attended, and attendance % |
| **`Gap_Years`** | Documented drop periods and reasons |
| **`Activities`** | Technical events, hackathons, and extra-curricular accolades |
| **`Seminars`** | Internal and external seminar presentations with verification links |
| **`Certificates`** | Industry certifications (AWS, Coursera, Oracle, NPTEL) |

---

## 🎓 Custom Menu in Google Sheets
Whenever you open the spreadsheet, a custom menu appears in the menu bar:
- **`🎓 ScholarTrack DBMS` &rarr; `🚀 Setup All 10 Database Tabs`**: Pre-creates and formats blank tables with headers if needed.
- **`🎓 ScholarTrack DBMS` &rarr; `🎨 Format & Auto-Style All Sheets`**: Applies dark headers, bold text, and frozen top rows.
- **`🎓 ScholarTrack DBMS` &rarr; `🗑️ Clear Table Records (Keep Headers)`**: Wipes data rows if you want a clean slate.
