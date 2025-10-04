#!/usr/bin/env python3
"""
Test demo mode detection
"""

def test_demo_mode():
    """Test if demo mode is properly detected"""
    try:
        from mobile_money_service import MobileMoneyService
        from mobile_money_config import get_mobile_money_config
        
        print("🧪 Testing Demo Mode Detection")
        print("=" * 40)
        
        # Get config
        config = get_mobile_money_config()
        
        # Create service
        service = MobileMoneyService(config)
        
        # Check demo mode
        is_demo = service.is_demo_mode()
        print(f"Demo Mode: {'✅ ENABLED' if is_demo else '❌ DISABLED'}")
        
        # Show current credentials
        mtn_config = config.get('mtn_momo', {})
        print(f"API User: {mtn_config.get('api_user', 'Not set')}")
        print(f"API Key: {mtn_config.get('api_key', 'Not set')}")
        
        # Test a payment request
        print("\n🔄 Testing Payment Request...")
        result = service.mtn_momo_request_payment("46733123450", 35, "USD")
        
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        print(f"Transaction ID: {result.get('transaction_id', 'N/A')}")
        
        if result.get('success'):
            print("\n✅ Demo mode is working!")
        else:
            print("\n❌ Demo mode issue detected")
            
        return is_demo
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_demo_mode()
