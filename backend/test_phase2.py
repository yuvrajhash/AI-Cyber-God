#!/usr/bin/env python3
"""
Test script for Phase 2 components
"""

def test_imports():
    """Test all Phase 2 imports"""
    print("🧪 Testing Phase 2 imports...")
    
    try:
        print("  ✓ Importing blockchain monitor...")
        from services.blockchain_monitor import blockchain_monitor
        
        print("  ✓ Importing real-time analytics...")
        from services.realtime_analytics import realtime_analytics
        
        print("  ✓ Importing Web3 integration...")
        from services.web3_integration import web3_integration
        
        print("  ✓ Importing Phase 2 server...")
        import phase2_server
        
        print("✅ All Phase 2 components imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of Phase 2 components"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        from services.realtime_analytics import realtime_analytics
        
        # Test analytics dashboard data
        dashboard_data = realtime_analytics.get_dashboard_data()
        print(f"  ✓ Analytics dashboard data: {len(dashboard_data)} keys")
        
        from services.web3_integration import web3_integration
        
        # Test Web3 integration
        protocols = web3_integration.defi_protocols
        print(f"  ✓ Web3 integration protocols: {len(protocols)} chains configured")
        
        print("✅ Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 QUANTUM-AI CYBER GOD - PHASE 2 TESTS")
    print("=" * 50)
    
    # Run tests
    imports_ok = test_imports()
    
    if imports_ok:
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 ALL PHASE 2 TESTS PASSED!")
            print("Phase 2 is ready for launch! 🚀")
        else:
            print("\n⚠️  Some functionality tests failed")
    else:
        print("\n❌ Import tests failed - check dependencies")
    
    print("\n" + "=" * 50) 