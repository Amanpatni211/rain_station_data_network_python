import pandas as pd
from pathlib import Path
import logging
from typing import Dict
from tqdm import tqdm

class SimpleStationProcessor:
    """Simple processor to convert raw station data to interim format."""
    
    def __init__(self, raw_data_path: Path, interim_data_path: Path):
        self.raw_data_path = raw_data_path
        self.interim_data_path = interim_data_path
        
        # Create interim directory
        self.interim_data_path.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def process_station(self, filepath: Path) -> Dict:
        """Process a single station file."""
        # Read data
        df = pd.read_csv(filepath)
        
        # Get metadata from first row (since it's constant)
        metadata = df.iloc[0][['STATION', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'NAME']].to_dict()
        
        # Add temporal coverage info
        metadata.update({
            'start_date': df['DATE'].min(),
            'end_date': df['DATE'].max(),
            'total_records': len(df),
            'missing_records': df['PRCP'].isna().sum()
        })
        
        return {
            'metadata': metadata,
            'data': df[['DATE', 'PRCP']]  # Keep only date and precipitation
        }
    
    def save_station_data(self, station_id: str, data: pd.DataFrame) -> None:
        """Save station data as CSV."""
        output_file = self.interim_data_path / f"{station_id}.csv"
        data.to_csv(output_file, index=False)
    
    def process_all_stations(self) -> None:
        """Process all station files."""
        # Get list of files
        csv_files = list(self.raw_data_path.glob("*.csv"))
        self.logger.info(f"Found {len(csv_files)} station files")
        
        # Store metadata for all stations
        all_metadata = []
        
        # Process each file with progress bar
        for file in tqdm(csv_files, desc="Processing stations"):
            try:
                # Process station
                result = self.process_station(file)
                
                # Save data
                station_id = result['metadata']['STATION']
                self.save_station_data(station_id, result['data'])
                
                # Collect metadata
                all_metadata.append(result['metadata'])
                
            except Exception as e:
                self.logger.error(f"Error processing {file.name}: {str(e)}")
                continue
        
        # Save metadata summary
        if all_metadata:
            metadata_df = pd.DataFrame(all_metadata)
            metadata_df.to_csv(self.interim_data_path / "station_metadata.csv", index=False)
            self.logger.info("Saved station metadata summary")