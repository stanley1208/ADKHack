"""
Detection Agent for disaster response sensor data detection.

This agent is responsible for detecting and reading sensor data from JSON files
stored in the simulated_data/ directory. It processes one file at a time and
outputs the JSON dictionary for further analysis by other agents.
Enhanced with BigQuery logging to store detected sensor data for historical analysis.
"""

import os
import json
import glob
from datetime import datetime
from typing import Dict, List, Any, Optional

# Try to import Google Cloud BigQuery, fall back gracefully if not available
try:
    from google.cloud import bigquery
    from google.cloud.exceptions import NotFound, Forbidden
    BIGQUERY_AVAILABLE = True
except ImportError:
    print("⚠️  Google Cloud BigQuery not available, detection will work without logging")
    bigquery = None
    NotFound = Forbidden = Exception
    BIGQUERY_AVAILABLE = False

# Import real Google ADK components
from google.adk.agents import BaseAgent
from google.adk.sessions import Session
ADK_AVAILABLE = True

print("✅ Google ADK Detection Agent - Real ADK Available!")

class DetectionAgent(BaseAgent):
    """
    Agent responsible for detecting and reading sensor data from JSON files.
    Enhanced with BigQuery logging for historical data storage and analysis.
    
    This agent monitors the simulated_data/ directory for JSON files containing
    sensor readings, processes them one at a time, and optionally logs the data
    to BigQuery for long-term storage and trend analysis.
    """
    
    def __init__(self, name: str = "sensor_detection_agent", description: str = None, 
                 bigquery_config: Optional[Dict[str, str]] = None):
        """
        Initialize the Detection Agent with optional BigQuery logging.
        
        Args:
            name: The name of the agent
            description: Description of the agent's capabilities
            bigquery_config: Optional BigQuery configuration with keys:
                - project_id: Google Cloud project ID
                - dataset_id: BigQuery dataset ID (default: "disaster_response")
                - table_id: BigQuery table ID (default: "sensor_readings")
                - location: BigQuery dataset location (default: "US")
        """
        if description is None:
            description = (
                "AI agent specialized in detecting and reading sensor data from JSON files. "
                "Monitors the simulated_data directory for new sensor readings, processes "
                "one file at a time, and optionally logs data to BigQuery for historical analysis."
            )
        
        # Initialize the BaseAgent with ADK-specific parameters
        super().__init__(
            name=name,
            description=description
        )
        
        # Initialize instance variables using object.__setattr__ to bypass Pydantic validation
        object.__setattr__(self, 'data_directory', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'simulated_data')))
        object.__setattr__(self, 'bigquery_config', bigquery_config or {})
        object.__setattr__(self, 'bigquery_enabled', BIGQUERY_AVAILABLE and self.bigquery_config.get('project_id') is not None)
        object.__setattr__(self, 'bigquery_client', None)
        object.__setattr__(self, 'bigquery_table', None)
        
        # Ensure the data directory exists
        os.makedirs(self.data_directory, exist_ok=True)
        
        # Initialize BigQuery client if enabled
        if self.bigquery_enabled:
            self._initialize_bigquery()
    
    def _initialize_bigquery(self):
        """Initialize BigQuery client and table if configuration is provided."""
        try:
            project_id = self.bigquery_config.get('project_id')
            dataset_id = self.bigquery_config.get('dataset_id', 'disaster_response')
            table_id = self.bigquery_config.get('table_id', 'sensor_readings')
            location = self.bigquery_config.get('location', 'US')
            
            # Initialize BigQuery client
            self.bigquery_client = bigquery.Client(project=project_id)
            
            # Create dataset if it doesn't exist
            dataset_ref = self.bigquery_client.dataset(dataset_id)
            try:
                self.bigquery_client.get_dataset(dataset_ref)
            except NotFound:
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = location
                dataset.description = "Disaster Response System - Sensor Data"
                self.bigquery_client.create_dataset(dataset)
                print(f"✅ Created BigQuery dataset: {project_id}.{dataset_id}")
            
            # Create table if it doesn't exist
            table_ref = dataset_ref.table(table_id)
            try:
                self.bigquery_table = self.bigquery_client.get_table(table_ref)
            except NotFound:
                schema = [
                    bigquery.SchemaField("sensor_timestamp", "TIMESTAMP", mode="REQUIRED"),
                    bigquery.SchemaField("location", "STRING", mode="REQUIRED"),
                    bigquery.SchemaField("temperature", "FLOAT", mode="REQUIRED"),
                    bigquery.SchemaField("smoke_level", "FLOAT", mode="REQUIRED"),
                    bigquery.SchemaField("processed_timestamp", "TIMESTAMP", mode="REQUIRED"),
                    bigquery.SchemaField("file_source", "STRING", mode="NULLABLE"),
                ]
                
                table = bigquery.Table(table_ref, schema=schema)
                table.description = "Sensor readings for disaster response monitoring"
                self.bigquery_table = self.bigquery_client.create_table(table)
                print(f"✅ Created BigQuery table: {project_id}.{dataset_id}.{table_id}")
            
            print(f"✅ BigQuery logging enabled: {project_id}.{dataset_id}.{table_id}")
            
        except Exception as e:
            print(f"⚠️  BigQuery initialization failed: {e}")
            self.bigquery_enabled = False
            self.bigquery_client = None
            self.bigquery_table = None
    
    def _log_to_bigquery(self, sensor_data: List[Dict[str, Any]], file_name: str) -> Dict[str, Any]:
        """
        Log sensor data to BigQuery for historical analysis.
        
        Args:
            sensor_data: List of sensor readings to log
            file_name: Source file name for tracking
            
        Returns:
            Dictionary with logging status and details
        """
        if not self.bigquery_enabled or not self.bigquery_client:
            return {
                "enabled": False,
                "status": "disabled",
                "message": "BigQuery logging not enabled"
            }
        
        try:
            # Prepare rows for insertion
            rows_to_insert = []
            current_time = datetime.now()
            
            for reading in sensor_data:
                # Parse timestamp or use current time
                try:
                    sensor_timestamp = datetime.fromisoformat(
                        reading.get('timestamp', '').replace('Z', '+00:00')
                    )
                except (ValueError, TypeError):
                    sensor_timestamp = current_time
                
                row = {
                    "sensor_timestamp": sensor_timestamp,
                    "location": reading.get('location', 'Unknown'),
                    "temperature": float(reading.get('temperature', 0)),
                    "smoke_level": float(reading.get('smoke_level', 0)),
                    "processed_timestamp": current_time,
                    "file_source": file_name,
                }
                rows_to_insert.append(row)
            
            # Insert rows into BigQuery
            errors = self.bigquery_client.insert_rows_json(
                self.bigquery_table, rows_to_insert
            )
            
            if errors:
                return {
                    "enabled": True,
                    "status": "error",
                    "errors": errors,
                    "message": f"Failed to insert {len(errors)} rows"
                }
            else:
                table_id = f"{self.bigquery_table.project}.{self.bigquery_table.dataset_id}.{self.bigquery_table.table_id}"
                return {
                    "enabled": True,
                    "status": "success",
                    "rows_inserted": len(rows_to_insert),
                    "table_id": table_id,
                    "message": f"Successfully logged {len(rows_to_insert)} readings"
                }
                
        except Exception as e:
            return {
                "enabled": True,
                "status": "error",
                "error": str(e),
                "message": f"BigQuery logging failed: {e}"
            }
    
    async def run(self, session: Session, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ADK-compatible run method for detecting and reading sensor data files.
        
        Args:
            session: ADK session object for maintaining state
            input_data: Dictionary that may contain a specific file path or search parameters
            
        Returns:
            Dictionary containing the sensor data from the detected JSON file
        """
        print(f"🔍 DetectionAgent running with real ADK session: {session.id}")
        return self.detect_and_read(input_data)
    
    def detect_and_read(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Detect and read sensor data from JSON files in the simulated_data directory.
        Enhanced with BigQuery logging for detected data.
        
        Args:
            input_data: Optional dictionary that may contain:
                - file_path: Specific file to read
                - pattern: File pattern to match (default: "*.json")
                
        Returns:
            Dictionary with detected sensor data and BigQuery logging status
        """
        if input_data is None:
            input_data = {}
        
        # Check if a specific file path is provided
        specific_file = input_data.get('file_path')
        if specific_file:
            return self._read_specific_file(specific_file)
        
        # Look for JSON files in the simulated_data directory
        pattern = input_data.get('pattern', '*.json')
        json_files = self._find_json_files(pattern)
        
        if not json_files:
            return {
                "status": "no_data_found",
                "message": f"No JSON files found in {self.data_directory}",
                "data_directory": self.data_directory,
                "pattern_searched": pattern,
                "timestamp": datetime.now().isoformat() + 'Z'
            }
        
        # Process the first available file
        selected_file = json_files[0]
        return self._read_specific_file(selected_file)
    
    def _find_json_files(self, pattern: str) -> List[str]:
        """Find JSON files matching the specified pattern."""
        search_pattern = os.path.join(self.data_directory, pattern)
        return glob.glob(search_pattern)
    
    def _read_specific_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read a specific JSON file and return its sensor data.
        Enhanced with BigQuery logging.
        
        Args:
            file_path: Path to the JSON file to read
            
        Returns:
            Dictionary containing the sensor data and BigQuery logging status
        """
        try:
            # Handle both absolute and relative paths
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.data_directory, file_path)
            
            if not os.path.exists(file_path):
                return {
                    "status": "file_not_found",
                    "message": f"File not found: {file_path}",
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat() + 'Z'
                }
            
            # Read and parse the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Extract sensor data
            sensor_data = data.get('sensor_data', [])
            if not sensor_data:
                return {
                    "status": "no_sensor_data",
                    "message": "No sensor_data found in JSON file",
                    "file_path": file_path,
                    "raw_data": data,
                    "timestamp": datetime.now().isoformat() + 'Z'
                }
            
            # Log to BigQuery if enabled
            file_name = os.path.basename(file_path)
            bigquery_logging = self._log_to_bigquery(sensor_data, file_name)
            
            return {
                "status": "data_detected",
                "sensor_data": sensor_data,
                "detection_info": {
                    "file_name": file_name,
                    "file_path": file_path,
                    "total_readings": len(sensor_data),
                    "data_directory": self.data_directory
                },
                "bigquery_logging": bigquery_logging,
                "timestamp": datetime.now().isoformat() + 'Z'
            }
            
        except json.JSONDecodeError as e:
            return {
                "status": "json_parse_error",
                "message": f"Invalid JSON format: {e}",
                "file_path": file_path,
                "timestamp": datetime.now().isoformat() + 'Z'
            }
        except Exception as e:
            return {
                "status": "read_error",
                "message": f"Error reading file: {e}",
                "file_path": file_path,
                "timestamp": datetime.now().isoformat() + 'Z'
            }
    
    def get_bigquery_status(self) -> Dict[str, Any]:
        """
        Get the current BigQuery configuration and status.
        
        Returns:
            Dictionary with BigQuery status information
        """
        return {
            "bigquery_available": BIGQUERY_AVAILABLE,
            "bigquery_enabled": self.bigquery_enabled,
            "project_id": self.bigquery_config.get('project_id'),
            "dataset_id": self.bigquery_config.get('dataset_id', 'disaster_response'),
            "table_id": self.bigquery_config.get('table_id', 'sensor_readings'),
            "full_table_id": (
                f"{self.bigquery_config.get('project_id')}.{self.bigquery_config.get('dataset_id', 'disaster_response')}.{self.bigquery_config.get('table_id', 'sensor_readings')}"
                if self.bigquery_config.get('project_id') else None
            )
        }
    
    async def query_historical_data(self, location: Optional[str] = None, 
                                   hours_back: int = 24) -> Optional[List[Dict[str, Any]]]:
        """
        Query historical sensor data from BigQuery.
        
        Args:
            location: Optional location filter
            hours_back: Number of hours back to query (default: 24)
            
        Returns:
            List of historical readings or None if BigQuery not available
        """
        if not self.bigquery_enabled or not self.bigquery_client:
            return None
        
        try:
            # Build query
            table_id = f"{self.bigquery_table.project}.{self.bigquery_table.dataset_id}.{self.bigquery_table.table_id}"
            
            query = f"""
                SELECT 
                    sensor_timestamp,
                    location,
                    temperature,
                    smoke_level,
                    processed_timestamp,
                    file_source
                FROM `{table_id}`
                WHERE sensor_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {hours_back} HOUR)
            """
            
            if location:
                query += f" AND LOWER(location) LIKE LOWER('%{location}%')"
            
            query += " ORDER BY sensor_timestamp DESC LIMIT 100"
            
            # Execute query
            query_job = self.bigquery_client.query(query)
            results = query_job.result()
            
            # Convert results to list of dictionaries
            historical_data = []
            for row in results:
                historical_data.append({
                    "sensor_timestamp": row.sensor_timestamp.isoformat() if row.sensor_timestamp else None,
                    "location": row.location,
                    "temperature": row.temperature,
                    "smoke_level": row.smoke_level,
                    "processed_timestamp": row.processed_timestamp.isoformat() if row.processed_timestamp else None,
                    "file_source": row.file_source
                })
            
            return historical_data
            
        except Exception as e:
            print(f"❌ Error querying historical data: {e}")
            return None 