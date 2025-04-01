import re

# List of commonly used MPINs (can be extended for more use cases)
COMMON_MPIN_4 = {"1234", "1111", "0000", "7777", "1212", "1122", "6666", "2580", "5555"}
COMMON_MPIN_6 = {"123456", "111111", "010101", "999999", "131211", "654321", "777777"}

def is_common_mpin(mpin):
    """Checks if the MPIN is commonly used."""
    if len(mpin) == 4:
        return mpin in COMMON_MPIN_4
    elif len(mpin) == 6:
        return mpin in COMMON_MPIN_6
    return False

def extract_mpin_variations(date):
    """Extracts possible MPINs from a given date (DDMMYYYY)."""
    if not date:
        return set()
    
    if not re.match(r"^\d{8}$", date):
        return set()

    dd, mm, yyyy = date[:2], date[2:4], date[4:]
    yy = yyyy[-2:]  # Last two digits of year

    return {dd+mm, mm+dd, yy+mm, mm+yy, dd+yy, yy+dd, yyyy[-4:]}

def evaluate_mpin(mpin, dob=None, spouse_dob=None, anniversary=None):
    """Evaluates the MPIN strength and provides reasons if weak."""
    reasons = []

    # Check if commonly used
    if is_common_mpin(mpin):
        reasons.append("COMMONLY_USED")

    # Check against demographic data
    if dob and mpin in extract_mpin_variations(dob):
        reasons.append("DEMOGRAPHIC_DOB_SELF")
    if spouse_dob and mpin in extract_mpin_variations(spouse_dob):
        reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
    if anniversary and mpin in extract_mpin_variations(anniversary):
        reasons.append("DEMOGRAPHIC_ANNIVERSARY")

    # Determine strength
    strength = "WEAK" if reasons else "STRONG"
    return strength, reasons

if __name__ == "__main__":
    # Take user input
    mpin = input("Enter your MPIN that can be(4 or 6 digits): ").strip()
    if not re.match(r"^\d{4,6}$", mpin):
        print("Invalid MPIN format. It should be 4 or 6 digits.")
        exit(1)

    dob = input("Enter your DOB (DDMMYYYY) or press enter to skip: ").strip()
    spouse_dob = input("Enter your spouse's DOB (DDMMYYYY) or press enter to skip: ").strip()
    anniversary = input("Enter your wedding anniversary (DDMMYYYY) or press enter to skip: ").strip()

    # Evaluate MPIN
    strength, reasons = evaluate_mpin(mpin, dob, spouse_dob, anniversary)

    # Output result
    print(f"\nMPIN Strength: {strength}")
    print(f"Reasons: {reasons}" if reasons else "Your MPIN is strong!")
