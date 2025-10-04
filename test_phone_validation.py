#!/usr/bin/env python3
"""
Test phone number validation for mobile money
"""

def test_phone_validation():
    """Test the phone number validation logic"""
    
    print("🧪 Testing Phone Number Validation")
    print("=" * 40)
    
    # Test cases
    test_numbers = [
        # MTN test numbers (should pass)
        "46733123450",  # Success
        "46733123451",  # Pending  
        "46733123452",  # Failed
        
        # Various formats (should pass)
        "+237123456789",
        "0123456789",
        "237-123-456-789",
        "237 123 456 789",
        
        # Invalid (should fail)
        "123",        # Too short
        "abc123",     # Contains letters
        "",           # Empty
        "   ",        # Only spaces
    ]
    
    for phone in test_numbers:
        # Simulate the validation logic from app.py
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        is_valid = len(cleaned_phone) >= 8
        
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{status} | '{phone}' -> '{cleaned_phone}' (len: {len(cleaned_phone)})")

if __name__ == "__main__":
    test_phone_validation()
    
    print("\n📱 Quick Test Numbers for Mobile Money:")
    print("=" * 40)
    print("🟢 Success: 46733123450")
    print("🟡 Pending: 46733123451") 
    print("🔴 Failed:  46733123452")
    print("\n💡 Use the 'Quick test numbers' buttons on the payment page!")
