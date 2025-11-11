#!/usr/bin/env python3
"""Test script to verify tournament toggle route"""

try:
    from app import app
    print("✅ Flask app imported successfully")
    
    # Check if route exists
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    tournament_routes = [r for r in routes if 'tournament' in r.lower()]
    
    if tournament_routes:
        print(f"\n🏆 Found {len(tournament_routes)} tournament-related route(s):")
        for route in tournament_routes:
            print(f"   {route}")
    else:
        print("\n❌ No tournament routes found!")
        
    # Check specifically for toggle route
    if '/admin/toggle-tournament' in routes:
        print("\n✅ admin_toggle_tournament route is registered correctly")
    else:
        print("\n❌ admin_toggle_tournament route NOT found!")
        print("\nAll admin routes:")
        admin_routes = [r for r in routes if '/admin' in r]
        for route in admin_routes[:10]:
            print(f"   {route}")
            
except Exception as e:
    print(f"❌ Error: {e}")
