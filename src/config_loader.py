"""Configuration loader for YAML files."""

import os
from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    """Loads and manages YAML configuration files."""

    def __init__(self, config_dir: str | None = None):
        """Initialize the config loader.
        
        Args:
            config_dir: Path to the configuration directory.
                       Defaults to 'config' in the project root.
        """
        if config_dir is None:
            # Default to config directory relative to this file's parent
            config_dir = Path(__file__).parent.parent / "config"
        self.config_dir = Path(config_dir)
        self._cache: dict[str, Any] = {}

    def load(self, filename: str) -> dict[str, Any]:
        """Load a YAML configuration file.
        
        Args:
            filename: Name of the YAML file to load (with or without .yaml extension).
            
        Returns:
            Dictionary containing the configuration data.
            
        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the file contains invalid YAML.
        """
        if not filename.endswith(('.yaml', '.yml')):
            filename = f"{filename}.yaml"
        
        filepath = self.config_dir / filename
        
        if filename in self._cache:
            return self._cache[filename]
        
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        self._cache[filename] = data
        return data

    def load_products(self) -> dict[str, Any]:
        """Load the products configuration.
        
        Returns:
            Dictionary containing product definitions.
        """
        return self.load("products")

    def load_templates(self) -> dict[str, Any]:
        """Load the templates configuration.
        
        Returns:
            Dictionary containing template definitions.
        """
        return self.load("templates")

    def load_sections(self) -> dict[str, Any]:
        """Load the sections configuration.
        
        Returns:
            Dictionary containing section order and structure.
        """
        return self.load("sections")

    def clear_cache(self) -> None:
        """Clear the configuration cache."""
        self._cache.clear()


def get_default_loader() -> ConfigLoader:
    """Get a ConfigLoader with the default configuration directory.
    
    Returns:
        ConfigLoader instance configured for the default config directory.
    """
    return ConfigLoader()
