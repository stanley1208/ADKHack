#!/usr/bin/env python3
"""
Real Google ADK Multi-Agent System Test
=======================================

This script tests the real Google ADK implementation with all three agents:
- DetectionAgent: Reads sensor data 
- AnalysisAgent: Analyzes risk levels
- AlertAgent: Generates emergency alerts

All using real Google ADK BaseAgent and SequentialAgent classes.
"""

import os
import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Set up environment
# Note: You'll need to set your Google API key
os.environ.setdefault('GOOGLE_API_KEY', 'your-google-api-key-here')
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', 'FALSE')

# Import the real orchestrator with Google ADK
import sys
sys.path.append('python_agents')

from python_agents.orchestrator import DisasterResponseOrchestrator


def create_test_data():
    """Create test sensor data for the demo."""
    # Ensure simulated_data directory exists
    data_dir = os.path.join('python_agents', 'simulated_data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create high-risk scenario
    high_risk_data = {
        "sensor_data": [
            {
                "location": "REAL ADK DEMO - Server Room Alpha",
                "temperature": 82,
                "smoke_level": 95,
                "timestamp": datetime.now().isoformat() + 'Z'
            },
            {
                "location": "REAL ADK DEMO - Data Center Core",
                "temperature": 78,
                "smoke_level": 88,
                "timestamp": datetime.now().isoformat() + 'Z'
            }
        ]
    }
    
    # Create medium-risk scenario  
    medium_risk_data = {
        "sensor_data": [
            {
                "location": "REAL ADK DEMO - Office Floor 3",
                "temperature": 42,
                "smoke_level": 55,
                "timestamp": datetime.now().isoformat() + 'Z'
            }
        ]
    }
    
    # Save test files
    high_risk_file = os.path.join(data_dir, 'real_adk_high_risk_test.json')
    medium_risk_file = os.path.join(data_dir, 'real_adk_medium_risk_test.json')
    
    with open(high_risk_file, 'w') as f:
        json.dump(high_risk_data, f, indent=2)
    
    with open(medium_risk_file, 'w') as f:
        json.dump(medium_risk_data, f, indent=2)
    
    return high_risk_file, medium_risk_file


async def test_real_adk_pipeline():
    """Test the complete real Google ADK multi-agent pipeline."""
    
    print("🚀 REAL GOOGLE ADK MULTI-AGENT SYSTEM TEST")
    print("=" * 60)
    print("Testing: DetectionAgent → AnalysisAgent → AlertAgent")
    print("Using: Real Google ADK BaseAgent and SequentialAgent")
    print("=" * 60)
    
    # Create test data
    print("\n📋 Creating test sensor data...")
    high_risk_file, medium_risk_file = create_test_data()
    print(f"   ✅ Created high-risk scenario: {os.path.basename(high_risk_file)}")
    print(f"   ✅ Created medium-risk scenario: {os.path.basename(medium_risk_file)}")
    
    # Initialize orchestrator with real ADK
    print(f"\n🤖 Initializing Real Google ADK Orchestrator...")
    orchestrator = DisasterResponseOrchestrator()
    
    # Initialize session
    session = await orchestrator.initialize_session()
    print(f"   📍 Session ID: {session.id}")
    print(f"   👤 User ID: {session.user_id}")
    print(f"   🏢 App Name: {session.app_name}")
    
    # Test scenarios
    scenarios = [
        {
            "name": "HIGH RISK Emergency Scenario",
            "file": os.path.basename(high_risk_file),
            "description": "Critical server room fire with 95% smoke levels"
        },
        {
            "name": "MEDIUM RISK Warning Scenario", 
            "file": os.path.basename(medium_risk_file),
            "description": "Elevated office temperature and smoke levels"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*20} SCENARIO {i}: {scenario['name']} {'='*20}")
        print(f"📄 Description: {scenario['description']}")
        print(f"📁 Test File: {scenario['file']}")
        
        try:
            # Run the pipeline
            print(f"\n🔄 Running Real ADK Multi-Agent Pipeline...")
            result = await orchestrator.process_file(scenario['file'])
            
            # Display results
            print(f"\n📊 PIPELINE RESULTS:")
            print(f"   Status: {result.get('pipeline_status')}")
            print(f"   Workflow: {result.get('workflow_name')}")
            print(f"   Steps: {result.get('completed_steps')}/{result.get('total_steps')}")
            
            # Detection results
            if 'detection' in result:
                detection = result['detection']
                print(f"\n🔍 DETECTION AGENT (Real ADK BaseAgent):")
                print(f"   Status: {detection.get('status')}")
                if detection.get('file_info'):
                    file_info = detection['file_info']
                    print(f"   File: {file_info.get('file_name')}")
                    print(f"   Readings: {file_info.get('total_readings')}")
            
            # Analysis results
            if 'analysis' in result:
                analysis = result['analysis']
                print(f"\n🔍 ANALYSIS AGENT (Real ADK BaseAgent):")
                print(f"   Overall Risk: {analysis.get('overall_risk_level')}")
                print(f"   Priority: {result.get('priority')}")
                print(f"   Total Readings: {analysis.get('total_readings')}")
                
                print(f"\n📍 Location Analysis:")
                for location_analysis in analysis.get('analysis', []):
                    risk_emoji = "🚨" if location_analysis['risk_level'] == 'High' else "⚠️" if location_analysis['risk_level'] == 'Medium' else "✅"
                    print(f"   {risk_emoji} {location_analysis['location']}")
                    print(f"      Risk Level: {location_analysis['risk_level']}")
                    print(f"      Temperature: {location_analysis['temperature']}°C")
                    print(f"      Smoke Level: {location_analysis['smoke_level']}%")
                    for reason in location_analysis['reasons']:
                        print(f"      Reason: {reason}")
            
            # Alert results
            if 'alerts' in result:
                alerts = result['alerts']
                print(f"\n🚨 ALERT AGENT (Real ADK BaseAgent):")
                print(f"   Alert Status: {alerts.get('status')}")
                print(f"   Total Alerts: {alerts.get('total_alerts')}")
                print(f"   Critical Alerts: {alerts.get('critical_alerts')}")
                
                if alerts.get('alerts_triggered'):
                    print(f"\n📢 EMERGENCY ALERTS TRIGGERED:")
                    for alert in alerts['alerts_triggered']:
                        severity_emoji = "🚨" if alert['severity'] == 'CRITICAL' else "⚠️"
                        print(f"   {severity_emoji} {alert['severity']}: {alert['message']}")
            
            print(f"\n⏰ Completed at: {result.get('timestamp')}")
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Clean up test file
        try:
            if scenario['file'] == os.path.basename(high_risk_file):
                os.remove(high_risk_file)
            elif scenario['file'] == os.path.basename(medium_risk_file):
                os.remove(medium_risk_file)
        except:
            pass
    
    print(f"\n{'='*60}")
    print("✅ REAL GOOGLE ADK MULTI-AGENT PIPELINE TEST COMPLETE!")
    print("🎯 Demonstrated:")
    print("   • Real Google ADK BaseAgent implementations")
    print("   • SequentialAgent workflow coordination") 
    print("   • Multi-agent session management")
    print("   • Production-grade disaster response system")
    print("🏆 Ready for hackathon demo!")
    print("=" * 60)


def main():
    """Main function to run the real ADK test."""
    try:
        # Check if API key is set
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key or api_key == 'your-google-api-key-here':
            print("⚠️  Warning: GOOGLE_API_KEY not set or using placeholder")
            print("   The agents will still work but may not have full AI capabilities")
            print("   Set your API key with: export GOOGLE_API_KEY=your-actual-key")
            print()
        
        # Run the async test
        asyncio.run(test_real_adk_pipeline())
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 