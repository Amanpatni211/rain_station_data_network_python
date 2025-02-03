from pathlib import Path
import yaml

class DataPathManager:
    """Manages data paths for the project."""
    
    def __init__(self, config_path=None):
        """Initialize path manager."""
        if config_path is None:
            # Default to looking for config.yaml in configs directory
            config_path = self._get_project_root() / "configs" / "config.yaml"
        
        self.config = self._load_config(config_path)
        self._validate_paths()
    
    def _get_project_root(self) -> Path:
        """Get project root directory."""
        # Assuming this file is in src/rain_station/utils/
        return Path(__file__).parents[3]
    
    def _load_config(self, config_path: Path) -> dict:
        """Load configuration from yaml file."""
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found at {config_path}")
            return {
                'paths': {
                    'data_root': '../../data',
                    'raw_data': '../../data/raw',
                    'interim_data': '../../data/interim_Data',
                    'processed_data': '../../data/processed'
                }
            }
    
    def _validate_paths(self):
        """Validate that required paths exist."""
        paths = self.config['paths']
        for key, path in paths.items():
            full_path = self._get_project_root() / Path(path)
            if not full_path.exists():
                print(f"Warning: Path {key} does not exist: {full_path}")
    
    def get_path(self, path_type: str) -> Path:
        """Get full path for specified path type."""
        if path_type not in self.config['paths']:
            raise ValueError(f"Unknown path type: {path_type}")
            
        relative_path = Path(self.config['paths'][path_type])
        return self._get_project_root() / relative_path