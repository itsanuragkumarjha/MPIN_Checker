import unittest
from src.mpin_validator import evaluate_mpin

class TestMPINValidator(unittest.TestCase):
    
    def test_common_mpin_4(self):
        self.assertEqual(evaluate_mpin("1234"), ("WEAK", ["COMMONLY_USED"]))
        self.assertEqual(evaluate_mpin("0000"), ("WEAK", ["COMMONLY_USED"]))
        self.assertEqual(evaluate_mpin("7777"), ("WEAK", ["COMMONLY_USED"]))
    
    def test_common_mpin_6(self):
        self.assertEqual(evaluate_mpin("123456"), ("WEAK", ["COMMONLY_USED"]))
        self.assertEqual(evaluate_mpin("654321"), ("WEAK", ["COMMONLY_USED"]))
        self.assertEqual(evaluate_mpin("111111"), ("WEAK", ["COMMONLY_USED"]))
    
    def test_strong_mpin(self):
        self.assertEqual(evaluate_mpin("5389"), ("STRONG", []))
        self.assertEqual(evaluate_mpin("947562"), ("STRONG", []))
    
    # for dob
    def test_weak_due_to_dob(self):
        self.assertEqual(evaluate_mpin("0201", "02011998"), ("WEAK", ["DEMOGRAPHIC_DOB_SELF"]))
        self.assertEqual(evaluate_mpin("9802", "02011998"), ("WEAK", ["DEMOGRAPHIC_DOB_SELF"]))
        self.assertEqual(evaluate_mpin("1998", "02011998"), ("WEAK", ["DEMOGRAPHIC_DOB_SELF"]))
        self.assertEqual(evaluate_mpin("0119", "02011998"), ("WEAK", ["DEMOGRAPHIC_DOB_SELF"]))
    
    # for spouse_dob
    def test_weak_due_to_spouse_dob(self):
        self.assertEqual(evaluate_mpin("0302", None, "03021999"), ("WEAK", ["DEMOGRAPHIC_DOB_SPOUSE"]))
        self.assertEqual(evaluate_mpin("1999", None, "03021999"), ("WEAK", ["DEMOGRAPHIC_DOB_SPOUSE"]))
    
    # for anniversary
    def test_weak_due_to_anniversary(self):
        self.assertEqual(evaluate_mpin("0403", None, None, "04032020"), ("WEAK", ["DEMOGRAPHIC_ANNIVERSARY"]))
        self.assertEqual(evaluate_mpin("2020", None, None, "04032020"), ("WEAK", ["DEMOGRAPHIC_ANNIVERSARY"]))
    
    # for multiple reasons
    def test_weak_due_to_multiple_reasons(self):
        self.assertEqual(evaluate_mpin("0201", "02011998", "02011998", "02011998"), 
                         ("WEAK", ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_DOB_SPOUSE", "DEMOGRAPHIC_ANNIVERSARY"]))
    
    # for non-common and non-demographic mpin
    def test_non_common_non_demographic_mpin(self):
        self.assertEqual(evaluate_mpin("6271", "01011990", "02021991", "03031992"), ("STRONG", []))
    
    # for empty or invalid inputs
    def test_mpin_partially_matching_demographics(self):
        self.assertEqual(evaluate_mpin("1190", "01011990"), ("WEAK", ["DEMOGRAPHIC_DOB_SELF"]))
    
    # for random numbers
    def test_mpin_strong_with_random_numbers(self):
        self.assertEqual(evaluate_mpin("7485"), ("STRONG", []))
        self.assertEqual(evaluate_mpin("482976"), ("STRONG", []))
     # for weak with random numbers
    def test_mpin_weak_combined_demographics(self):
        self.assertEqual(evaluate_mpin("1990", "01011990", "02021991"), ("WEAK", ["DEMOGRAPHIC_DOB_SELF"]))
    # for empty mpin
    def test_empty_mpin(self):
        self.assertEqual(evaluate_mpin(""), ("STRONG", []))
    # for invalid mpin
    def test_random_mpin_weak_case(self):
        self.assertEqual(evaluate_mpin("777777"), ("WEAK", ["COMMONLY_USED"]))
    
if __name__ == "__main__":
    unittest.main()
