import os
from app import sync_sheets

def test_sheets_logic():
    print("Testing Google Sheets Sync credential and API behavior...")
    
    # Test 1: No credentials set
    orig_key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    orig_sid = os.environ.get("GOOGLE_SHEET_ID")
    
    os.environ.pop("GOOGLE_SERVICE_ACCOUNT_FILE", None)
    os.environ.pop("GOOGLE_SHEET_ID", None)
    
    ok, msg = sync_sheets()
    assert not ok, "Sync should fail when credentials are not configured"
    assert "credentials missing" in msg.lower(), f"Unexpected error message: {msg}"
    print("[PASS] Test 1: Missing credentials error verified.")

    # Test 2: File does not exist
    os.environ["GOOGLE_SERVICE_ACCOUNT_FILE"] = "non_existent_key_file.json"
    os.environ["GOOGLE_SHEET_ID"] = "dummy_sheet_id_123"
    
    ok, msg = sync_sheets()
    assert not ok, "Sync should fail when service account file is not found"
    assert "not found" in msg.lower(), f"Unexpected error message: {msg}"
    print("[PASS] Test 2: Missing key file error verified.")

    # Restore original environment if any
    if orig_key:
        os.environ["GOOGLE_SERVICE_ACCOUNT_FILE"] = orig_key
    else:
        os.environ.pop("GOOGLE_SERVICE_ACCOUNT_FILE", None)
    if orig_sid:
        os.environ["GOOGLE_SHEET_ID"] = orig_sid
    else:
        os.environ.pop("GOOGLE_SHEET_ID", None)

    print("ALL GOOGLE SHEETS SYNC VALIDATION TESTS PASSED!")

if __name__ == "__main__":
    test_sheets_logic()
