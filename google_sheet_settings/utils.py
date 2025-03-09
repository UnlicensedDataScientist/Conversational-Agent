import re

def extract_url_from_message(user_input):
    """
    Detects if a user input contains a Google Sheets link, extracts its ID, full link, and gid.

    Args:
        user_input (str): The text provided by the user.

    Returns:
        dict: A dictionary with four keys:
              - "link_detected" (bool): True if a Google Sheets link is detected, False otherwise.
              - "sheet_id" (str): The ID of the Google Sheet if the link is valid, None if no link is found.
              - "full_link" (str): The complete Google Sheets link if detected, None otherwise.
              - "gid" (str): The gid of the specific sheet/tab if present in the link, None otherwise.
    """
    # Regular expression to detect Google Sheets links and extract gid
    pattern = r"(https?://docs\.google\.com/spreadsheets/d/[\w-]+(?:/[^\s]*)?)"
    
    # Search for the pattern in the user input
    match = re.search(pattern, user_input)

    if match:
        # Extract the full link, sheet ID, and gid
        full_link = match.group(0)
        # Extract the sheet ID from the full link
        sheet_id = full_link.split('/')[5]  # The ID is the 6th segment in the URL
        gid = extract_gid_from_url(full_link)

        return {"link_detected": True, "sheet_id": sheet_id, "full_link": full_link, "gid": gid}
    else:
        return None

def extract_gid_from_url(url):
    """
    Extracts the gid from a Google Sheets URL.

    Args:
        url (str): The Google Sheets URL.

    Returns:
        str: The gid if found, None otherwise.
    """
    # Regular expression to extract the gid
    pattern = r"[?&#]gid=(\d+)"
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)  # Return the gid
    else:
        return None  # No gid found