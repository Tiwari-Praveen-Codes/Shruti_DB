/**
 * ==============================================================================
 * SCHOLARTRACK DBMS — GOOGLE APPS SCRIPT WEBHOOK & AUTOMATION ENGINE
 * ==============================================================================
 * Connects Google Sheets directly with ScholarTrack (MySQL & SQLite).
 * 
 * Features:
 * 1. Automatic 10-table synchronization from Streamlit via Web App API (doPost).
 * 2. Custom Spreadsheet UI Menu ('🎓 ScholarTrack DBMS') for instant setup.
 * 3. One-click tab generation, styling, frozen header rows, and column auto-sizing.
 * 4. Works without requiring complex Google Cloud service account JSON keys.
 */

// Master Schema Column Definitions for all 10 Normalized 3NF Tables
const SCHOLARTRACK_SCHEMAS = {
  "Students": [
    "id", "roll_number", "full_name", "email", "department", "admission_year", "current_status"
  ],
  "School_Records": [
    "id", "student_id", "level", "board", "passing_year", "marks_obtained", "marks_total", "percentage", "roll_number", "full_name"
  ],
  "Semester_Results": [
    "id", "student_id", "semester_number", "academic_year", "sgpa", "cgpa", "result_status", "backlog_count", "is_gap_after", "roll_number", "full_name"
  ],
  "Subjects": [
    "id", "subject_code", "subject_name", "subject_type", "credits"
  ],
  "Subject_Marks": [
    "id", "semester_result_id", "subject_id", "marks_obtained", "marks_total", "passing_marks", "component", "semester_number", "roll_number", "subject_code", "subject_name", "subject_type"
  ],
  "Attendance": [
    "id", "student_id", "subject_id", "academic_year", "semester_number", "classes_held", "classes_attended", "roll_number", "full_name", "subject_code", "subject_name"
  ],
  "Gap_Years": [
    "id", "student_id", "start_year", "end_year", "reason_category", "notes", "roll_number", "full_name"
  ],
  "Activities": [
    "id", "student_id", "title", "activity_type", "organization", "activity_date", "description", "roll_number", "full_name"
  ],
  "Seminars": [
    "id", "student_id", "title", "seminar_scope", "organizer", "seminar_date", "certificate_url", "roll_number", "full_name"
  ],
  "Certificates": [
    "id", "student_id", "title", "issuer", "category", "issue_date", "credential_url", "notes", "roll_number", "full_name"
  ]
};

/**
 * Custom Menu loaded automatically when opening the Spreadsheet
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎓 ScholarTrack DBMS')
    .addItem('🚀 Setup All 10 Database Tabs', 'setupAllSheets')
    .addItem('🎨 Format & Auto-Style All Sheets', 'formatAllSheets')
    .addSeparator()
    .addItem('🗑️ Clear Table Records (Keep Headers)', 'clearAllDataKeepHeaders')
    .addItem('ℹ️ Show Webhook Instructions', 'showInstructions')
    .addToUi();
}

/**
 * Creates and formats all 10 required database worksheets with headers
 */
function setupAllSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let createdCount = 0;

  for (const [sheetName, headers] of Object.entries(SCHOLARTRACK_SCHEMAS)) {
    let sheet = ss.getSheetByName(sheetName);
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
      createdCount++;
    }

    // Set headers if sheet is empty or headers missing
    if (sheet.getLastRow() === 0) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    }

    styleSheetHeader(sheet, headers.length);
  }

  // Remove default 'Sheet1' if empty and other sheets exist
  const sheet1 = ss.getSheetByName('Sheet1');
  if (sheet1 && ss.getSheets().length > 1 && sheet1.getLastRow() === 0) {
    ss.deleteSheet(sheet1);
  }

  SpreadsheetApp.getUi().alert(
    '✅ Setup Complete',
    `All 10 ScholarTrack DBMS tabs are ready and formatted with 3NF headers.\n\n` +
    `Tabs: Students, School_Records, Semester_Results, Subjects, Subject_Marks, Attendance, Gap_Years, Activities, Seminars, Certificates.`,
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

/**
 * Formats a sheet with sleek enterprise styling
 */
function styleSheetHeader(sheet, numCols) {
  if (numCols <= 0) return;
  
  // Format Header Row
  const headerRange = sheet.getRange(1, 1, 1, numCols);
  headerRange.setBackground('#0f172a'); // Slate 900
  headerRange.setFontColor('#f8fafc'); // White / Slate 50
  headerRange.setFontWeight('bold');
  headerRange.setFontSize(10);
  headerRange.setHorizontalAlignment('center');
  
  sheet.setFrozenRows(1);
  
  // Auto-fit column widths
  for (let c = 1; c <= numCols; c++) {
    sheet.autoResizeColumn(c);
    const w = sheet.getColumnWidth(c);
    if (w < 100) sheet.setColumnWidth(c, 110);
  }
}

/**
 * Formats all existing sheets in the spreadsheet
 */
function formatAllSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = ss.getSheets();
  
  for (const sheet of sheets) {
    const lastCol = sheet.getLastColumn();
    if (lastCol > 0) {
      styleSheetHeader(sheet, lastCol);
    }
  }
  
  SpreadsheetApp.getUi().alert('🎨 Complete', 'All 10 sheets formatted with dark headers and frozen rows.', SpreadsheetApp.getUi().ButtonSet.OK);
}

/**
 * Clears data rows while preserving headers
 */
function clearAllDataKeepHeaders() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.alert('Confirm Clear', 'Are you sure you want to clear all data rows across all 10 tables? (Headers will be preserved)', ui.ButtonSet.YES_NO);
  
  if (response !== ui.Button.YES) return;

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  for (const sheetName of Object.keys(SCHOLARTRACK_SCHEMAS)) {
    const sheet = ss.getSheetByName(sheetName);
    if (sheet && sheet.getLastRow() > 1) {
      sheet.getRange(2, 1, sheet.getLastRow() - 1, sheet.getLastColumn()).clearContent();
    }
  }

  ui.alert('Done', 'All table data rows cleared.', ui.ButtonSet.OK);
}

/**
 * Displays deployment instructions for the Webhook
 */
function showInstructions() {
  const html = `
    <div style="font-family: sans-serif; font-size: 13px; line-height: 1.6; color: #1e293b;">
      <h3 style="color: #2563eb; margin-top: 0;">🚀 How to Connect ScholarTrack:</h3>
      <ol>
        <li>Click <b>Deploy</b> (top right) &rarr; <b>New deployment</b>.</li>
        <li>Select type: <b>Web app</b> (gear icon).</li>
        <li>Set:
          <ul>
            <li><b>Execute as:</b> Me</li>
            <li><b>Who has access:</b> Anyone</li>
          </ul>
        </li>
        <li>Click <b>Deploy</b> and copy the <b>Web app URL</b>.</li>
        <li>Paste the Web app URL into ScholarTrack under <b>Google Sheets Sync</b> page.</li>
        <li>Click <b>Sync All 10 Tables</b>.</li>
      </ol>
    </div>
  `;
  const userInterface = HtmlService.createHtmlOutput(html).setWidth(450).setHeight(320);
  SpreadsheetApp.getUi().showModalDialog(userInterface, 'ScholarTrack Webhook Setup');
}

/**
 * ==============================================================================
 * HTTP API ENDPOINTS (doPost & doGet)
 * ==============================================================================
 */

/**
 * HTTP GET Health Check / Ping
 */
function doGet(e) {
  const output = {
    status: "active",
    service: "ScholarTrack Google Sheets Webhook Engine",
    timestamp: new Date().toISOString(),
    supportedTables: Object.keys(SCHOLARTRACK_SCHEMAS)
  };
  return ContentService.createTextOutput(JSON.stringify(output))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * HTTP POST: Synchronizes data pushed from ScholarTrack Python backend
 */
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    // Wait up to 30 seconds for lock to prevent race conditions
    lock.waitLock(30000);

    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput(JSON.stringify({
        status: "error",
        message: "No POST body received."
      })).setMimeType(ContentService.MimeType.JSON);
    }

    const payload = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let totalUpdatedSheets = 0;
    let totalRowsSynced = 0;

    const sheetsData = payload.sheets || {};

    for (const [sheetName, rows] of Object.entries(sheetsData)) {
      if (!Array.isArray(rows) || rows.length === 0) continue;

      let sheet = ss.getSheetByName(sheetName);
      if (!sheet) {
        sheet = ss.insertSheet(sheetName);
      }

      // Clear existing content and formats
      sheet.clear();

      const numRows = rows.length;
      const numCols = rows[0].length;

      // Batch write for maximum performance
      const targetRange = sheet.getRange(1, 1, numRows, numCols);
      targetRange.setValues(rows);

      // Style header
      styleSheetHeader(sheet, numCols);

      totalUpdatedSheets++;
      totalRowsSynced += (numRows - 1); // exclude header
    }

    SpreadsheetApp.flush();

    const response = {
      status: "success",
      message: `Successfully synchronized ${totalUpdatedSheets} tables with ${totalRowsSynced} total records into Google Sheets!`,
      sheetsUpdated: totalUpdatedSheets,
      totalRows: totalRowsSynced,
      timestamp: new Date().toISOString()
    };

    return ContentService.createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}
