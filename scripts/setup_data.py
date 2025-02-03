from pathlib import Path
import argparse
from rain_station.utils.path_manager import DataPathManager

def setup_data_directories(data_root: Path):
    """Create required data directories."""
    directories = ['raw', 'interim_Data', 'processed']
    
    for dir_name in directories:
        dir_path = data_root / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

def main():
    parser = argparse.ArgumentParser(description="Setup data directories")
    parser.add_argument('--data-root', type=Path, help='Path to data root directory')
    args = parser.parse_args()
    
    if args.data_root:
        setup_data_directories(args.data_root)
    else:
        # Use default from config
        path_mgr = DataPathManager()
        setup_data_directories(path_mgr.get_path('data_root'))

if __name__ == "__main__":
    main()