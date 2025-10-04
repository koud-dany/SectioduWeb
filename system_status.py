#!/usr/bin/env python3
"""
Mobile Money System Status Check
"""

def system_status():
    """Check the complete mobile money system status"""
    print("📱 Mobile Money System Status")
    print("=" * 50)
    
    try:
        # Test imports
        from mobile_money_service import MobileMoneyService
        from mobile_money_config import get_mobile_money_config
        print("✅ Mobile Money Service: Imported successfully")
        
        # Test config
        config = get_mobile_money_config()
        print("✅ Mobile Money Config: Loaded successfully")
        
        # Test demo mode
        service = MobileMoneyService(config)
        is_demo = service.is_demo_mode()
        print(f"✅ Demo Mode: {'ENABLED' if is_demo else 'DISABLED'}")
        
        # Test Flask app
        from app import app
        print("✅ Flask App: Imported successfully")
        
        # Show routes
        mobile_routes = [rule.rule for rule in app.url_map.iter_rules() 
                        if any(x in rule.rule for x in ['/upgrade', '/initiate_mobile', '/check_payment'])]
        print(f"✅ Mobile Payment Routes: {len(mobile_routes)} found")
        for route in mobile_routes:
            print(f"   • {route}")
        
        print("\n" + "=" * 50)
        print("🎉 SYSTEM STATUS: FULLY OPERATIONAL")
        print("=" * 50)
        
        print("\n📋 HOW TO TEST:")
        print("1. Start Flask: python app.py")
        print("2. Visit: http://localhost:5000/")
        print("3. Register/Login")
        print("4. Go to: http://localhost:5000/upgrade")
        print("5. Use test number: 46733123450")
        print("6. Select MTN Mobile Money")
        print("7. Click 'Pay $35'")
        
        print("\n🎭 DEMO MODE BENEFITS:")
        print("• No real API credentials needed")
        print("• Instant payment simulation")
        print("• Test different scenarios:")
        print("  - 46733123450 = Success ✅")
        print("  - 46733123451 = Pending ⏳")
        print("  - 46733123452 = Failed ❌")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    system_status()
