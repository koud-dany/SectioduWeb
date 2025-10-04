#!/usr/bin/env python3
"""
Test script for custom reason functionality
"""

def test_custom_reason_implementation():
    """Test if the custom reason feature is properly implemented"""
    print("🔧 Testing Custom Reason Feature")
    print("=" * 50)
    
    # Check if the template file has the expected custom reason functionality
    try:
        with open('templates/admin/users.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key custom reason features
        features_to_check = [
            'toggleCustomReason',
            'customReasonDiv',
            'custom_reason',
            'onchange="toggleCustomReason',
            'Please specify the reason',
            'textarea class="form-control"',
            'customReasonTextarea.value.trim()'
        ]
        
        print("Checking for custom reason features:")
        for feature in features_to_check:
            if feature in content:
                print(f"✅ {feature}: Found")
            else:
                print(f"❌ {feature}: Missing")
        
        # Check for validation features
        validation_features = [
            'customReasonTextarea.required = true',
            'customReasonTextarea.required = false',
            'Please provide a specific reason',
            'customReasonTextarea.value.trim()'
        ]
        
        print("\nChecking for validation features:")
        for feature in validation_features:
            if feature in content:
                print(f"✅ {feature}: Found")
            else:
                print(f"❌ {feature}: Missing")
        
        print("\n🎯 How to test the custom reason feature:")
        print("1. Start app: python app.py")
        print("2. Login as admin")
        print("3. Visit: http://localhost:5000/admin/users")
        print("4. Click block button next to any user")
        print("5. In the modal:")
        print("   - Select 'Other' from reason dropdown")
        print("   - Custom text area should appear")
        print("   - Type your custom reason")
        print("   - Submit the form")
        print("6. The custom reason should be saved instead of 'Other'")
        
        return True
        
    except FileNotFoundError:
        print("❌ Template file not found")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_custom_reason_implementation()
