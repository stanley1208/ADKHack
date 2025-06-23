"""
AI-Powered Analysis Agent for disaster response risk assessment.

This version uses real Google AI (Gemini) to analyze sensor data with intelligent reasoning,
not just programmatic rules. The AI can understand context, make nuanced decisions,
and provide sophisticated emergency response recommendations.
"""

import os
from datetime import datetime
from typing import Dict, List, Any, Union
from dotenv import load_dotenv

# Import Google ADK components
from google.adk.agents import BaseAgent
from google.adk.sessions import Session

# Import Google AI
from google.genai import Client

# Load environment variables
load_dotenv()

class AIAnalysisAgent(BaseAgent):
    """
    AI-Powered agent for disaster response using real Google AI reasoning.
    
    This agent uses Gemini AI to analyze sensor data with sophisticated reasoning,
    considering context, patterns, and providing intelligent recommendations
    beyond simple threshold-based analysis.
    """
    
    def __init__(self, name: str = "ai_disaster_analysis_agent", description: str = None):
        """
        Initialize the AI Analysis Agent.
        
        Args:
            name: The name of the agent
            description: Description of the agent's capabilities
        """
        if description is None:
            description = (
                "AI-powered disaster response agent using Google Gemini AI. "
                "Provides intelligent analysis of sensor data with contextual understanding, "
                "sophisticated reasoning, and nuanced emergency response recommendations."
            )
        
        # Initialize the BaseAgent first
        super().__init__(name=name, description=description)
        
        # Initialize Google AI client after BaseAgent
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            try:
                self._ai_client = Client(api_key=api_key)
                self._ai_available = True
                print(f"✅ AI-Powered Analysis Agent - Google Gemini Ready!")
            except Exception as e:
                self._ai_client = None
                self._ai_available = False
                print(f"⚠️  AI client setup failed: {e}")
        else:
            self._ai_client = None
            self._ai_available = False
            print(f"⚠️  AI-Powered Analysis Agent - No API key, using fallback")
    
    @property
    def ai_available(self) -> bool:
        """Check if AI is available for analysis."""
        return getattr(self, '_ai_available', False)
    
    async def run(self, session: Session, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ADK-compatible run method for AI-powered sensor data analysis.
        
        Args:
            session: ADK session object for maintaining state
            input_data: Dictionary containing sensor data for analysis
            
        Returns:
            Dictionary with AI-enhanced risk analysis results
        """
        print(f"🤖 AI AnalysisAgent running with session: {session.id}")
        return await self.ai_analyze(input_data)
    
    async def ai_analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered analysis of sensor data using Google Gemini.
        
        Args:
            data: Dictionary containing 'sensor_data' key with sensor readings
            
        Returns:
            Dictionary with AI-enhanced risk assessment and recommendations
        """
        sensor_data = data.get('sensor_data', [])
        
        # Handle both single readings and arrays
        if not isinstance(sensor_data, list):
            sensor_data = [sensor_data]
        
        if not sensor_data:
            raise ValueError("No sensor data provided")
        
        if getattr(self, '_ai_available', False):
            return await self._ai_powered_analysis(sensor_data)
        else:
            return self._fallback_analysis(sensor_data)
    
    async def _ai_powered_analysis(self, sensor_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Use Google AI for intelligent disaster analysis.
        
        Args:
            sensor_data: List of sensor readings
            
        Returns:
            AI-enhanced analysis results
        """
        try:
            # Prepare data for AI analysis
            data_summary = self._prepare_data_for_ai(sensor_data)
            
            # Create AI prompt for disaster analysis
            prompt = f"""You are an expert emergency response AI coordinator analyzing real-time disaster sensor data.

SENSOR DATA:
{data_summary}

ANALYSIS REQUIRED:
1. Assess overall risk level (Low/Medium/High) based on temperature and smoke readings
2. Identify the most critical locations requiring immediate attention
3. Provide specific emergency response actions for each risk level
4. Consider patterns, trends, and contextual factors

RISK GUIDELINES:
- High Risk: Generally >50°C temperature OR >70% smoke (but use your judgment for context)
- Medium Risk: Generally >35°C temperature OR >40% smoke (but consider combinations)
- Low Risk: Normal operational parameters

RESPONSE FORMAT:
Provide a detailed analysis considering:
- Overall risk assessment with reasoning
- Location-specific risk levels and reasons
- Immediate actions required
- Resource deployment recommendations
- Evacuation priorities if needed

Be specific, actionable, and prioritize life safety."""

            # Get AI analysis
            ai_client = getattr(self, '_ai_client', None)
            if not ai_client:
                raise Exception("AI client not available")
                
            response = ai_client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            
            if response and response.text:
                ai_analysis = response.text
                
                # Parse AI response and format for system compatibility
                formatted_result = self._format_ai_response(sensor_data, ai_analysis)
                
                return formatted_result
            else:
                print("⚠️  No AI response, falling back to programmatic analysis")
                return self._fallback_analysis(sensor_data)
                
        except Exception as e:
            print(f"⚠️  AI analysis failed ({e}), using fallback")
            return self._fallback_analysis(sensor_data)
    
    def _prepare_data_for_ai(self, sensor_data: List[Dict[str, Any]]) -> str:
        """Prepare sensor data in a format suitable for AI analysis."""
        data_lines = []
        for i, reading in enumerate(sensor_data, 1):
            location = reading.get('location', f'Location {i}')
            temp = reading.get('temperature', 'Unknown')
            smoke = reading.get('smoke_level', 'Unknown')
            timestamp = reading.get('timestamp', 'Unknown')
            
            data_lines.append(f"Location {i}: {location}")
            data_lines.append(f"  Temperature: {temp}°C")
            data_lines.append(f"  Smoke Level: {smoke}%")
            data_lines.append(f"  Timestamp: {timestamp}")
            data_lines.append("")
        
        return "\n".join(data_lines)
    
    def _format_ai_response(self, sensor_data: List[Dict[str, Any]], ai_analysis: str) -> Dict[str, Any]:
        """
        Format AI response into system-compatible format.
        
        Args:
            sensor_data: Original sensor data
            ai_analysis: AI analysis text
            
        Returns:
            Formatted analysis result
        """
        # Extract risk level from AI response (simple approach)
        ai_text_lower = ai_analysis.lower()
        
        if 'high risk' in ai_text_lower or 'critical' in ai_text_lower or 'emergency' in ai_text_lower:
            overall_risk = 'High'
        elif 'medium risk' in ai_text_lower or 'moderate' in ai_text_lower or 'elevated' in ai_text_lower:
            overall_risk = 'Medium'
        else:
            overall_risk = 'Low'
        
        # Analyze each location with AI insights
        analysis_results = []
        for reading in sensor_data:
            location_analysis = self._analyze_single_location_with_ai(reading, ai_analysis)
            analysis_results.append(location_analysis)
        
        return {
            'overall_risk_level': overall_risk,
            'total_readings': len(sensor_data),
            'analysis': analysis_results,
            'ai_analysis': ai_analysis,  # Include full AI analysis
            'ai_powered': True,
            'timestamp': datetime.now().isoformat() + 'Z',
            'agent_info': {
                'agent_name': self.name,
                'agent_type': 'AI-Powered Analysis Agent',
                'ai_model': 'Google Gemini',
                'processing_timestamp': datetime.now().isoformat() + 'Z'
            }
        }
    
    def _analyze_single_location_with_ai(self, reading: Dict[str, Any], ai_analysis: str) -> Dict[str, Any]:
        """Analyze single location with AI context."""
        temperature = reading.get('temperature', 0)
        smoke_level = reading.get('smoke_level', 0)
        location = reading.get('location', 'Unknown')
        timestamp = reading.get('timestamp', datetime.now().isoformat() + 'Z')
        
        # Determine risk level based on thresholds (with AI context)
        if temperature > 50 or smoke_level > 70:
            risk_level = 'High'
            reasons = []
            if temperature > 50:
                reasons.append(f"Critical temperature: {temperature}°C")
            if smoke_level > 70:
                reasons.append(f"Dangerous smoke level: {smoke_level}%")
        elif temperature > 35 or smoke_level > 40:
            risk_level = 'Medium'
            reasons = []
            if temperature > 35:
                reasons.append(f"Elevated temperature: {temperature}°C")
            if smoke_level > 40:
                reasons.append(f"Elevated smoke level: {smoke_level}%")
        else:
            risk_level = 'Low'
            reasons = ['Readings within normal parameters']
        
        # Add AI insights if available
        location_lower = location.lower()
        if location_lower in ai_analysis.lower():
            reasons.append("AI analysis: See detailed assessment")
        
        return {
            'location': location,
            'timestamp': timestamp,
            'temperature': temperature,
            'smoke_level': smoke_level,
            'risk_level': risk_level,
            'reasons': reasons,
            'ai_enhanced': True
        }
    
    def _fallback_analysis(self, sensor_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback to programmatic analysis if AI is unavailable."""
        print("🔧 Using fallback programmatic analysis")
        
        highest_risk = 'Low'
        analysis = []
        
        for reading in sensor_data:
            risk_assessment = self._assess_single_reading_fallback(reading)
            analysis.append(risk_assessment)
            
            # Track highest risk level
            if risk_assessment['risk_level'] == 'High':
                highest_risk = 'High'
            elif risk_assessment['risk_level'] == 'Medium' and highest_risk == 'Low':
                highest_risk = 'Medium'
        
        return {
            'overall_risk_level': highest_risk,
            'total_readings': len(sensor_data),
            'analysis': analysis,
            'ai_powered': False,
            'timestamp': datetime.now().isoformat() + 'Z',
            'agent_info': {
                'agent_name': self.name,
                'agent_type': 'Analysis Agent (Fallback Mode)',
                'processing_timestamp': datetime.now().isoformat() + 'Z'
            }
        }
    
    def _assess_single_reading_fallback(self, reading: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback assessment for single reading."""
        temperature = reading.get('temperature')
        smoke_level = reading.get('smoke_level')
        location = reading.get('location', 'Unknown')
        timestamp = reading.get('timestamp', datetime.now().isoformat() + 'Z')
        
        if temperature is None or smoke_level is None:
            raise ValueError("Each reading must include numeric temperature and smoke_level fields")
        
        risk_level = 'Low'
        reasons = []
        
        # Standard risk assessment logic
        if temperature > 50 or smoke_level > 70:
            risk_level = 'High'
            if temperature > 50:
                reasons.append(f"Critical temperature: {temperature}°C")
            if smoke_level > 70:
                reasons.append(f"Dangerous smoke level: {smoke_level}%")
        elif temperature > 35 or smoke_level > 40:
            risk_level = 'Medium'
            if temperature > 35:
                reasons.append(f"Elevated temperature: {temperature}°C")
            if smoke_level > 40:
                reasons.append(f"Elevated smoke level: {smoke_level}%")
        else:
            reasons.append('All readings within normal parameters')
        
        return {
            'location': location,
            'timestamp': timestamp,
            'temperature': temperature,
            'smoke_level': smoke_level,
            'risk_level': risk_level,
            'reasons': reasons,
            'ai_enhanced': False
        } 