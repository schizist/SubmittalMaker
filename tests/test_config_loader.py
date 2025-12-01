"""Tests for the config_loader module."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from src.config_loader import ConfigLoader


@pytest.fixture
def temp_config_dir():
    """Create a temporary config directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test config files
        products = {
            "products": {
                "test_product": {
                    "name": "Test Product",
                    "manufacturer": "Test Mfg",
                    "model": "TP-100",
                    "description": "A test product",
                    "specifications": {
                        "wattage": "10W"
                    },
                    "cut_sheet": "test.pdf",
                    "msds": None
                }
            }
        }
        
        templates = {
            "templates": {
                "test_template": "Hello {{ name }}"
            }
        }
        
        sections = {
            "section_order": ["cover", "content"],
            "default_product_sections": []
        }
        
        with open(Path(tmpdir) / "products.yaml", 'w') as f:
            yaml.dump(products, f)
        
        with open(Path(tmpdir) / "templates.yaml", 'w') as f:
            yaml.dump(templates, f)
        
        with open(Path(tmpdir) / "sections.yaml", 'w') as f:
            yaml.dump(sections, f)
        
        yield tmpdir


def test_load_products(temp_config_dir):
    """Test loading products configuration."""
    loader = ConfigLoader(temp_config_dir)
    products = loader.load_products()
    
    assert "products" in products
    assert "test_product" in products["products"]
    assert products["products"]["test_product"]["name"] == "Test Product"


def test_load_templates(temp_config_dir):
    """Test loading templates configuration."""
    loader = ConfigLoader(temp_config_dir)
    templates = loader.load_templates()
    
    assert "templates" in templates
    assert "test_template" in templates["templates"]


def test_load_sections(temp_config_dir):
    """Test loading sections configuration."""
    loader = ConfigLoader(temp_config_dir)
    sections = loader.load_sections()
    
    assert "section_order" in sections
    assert sections["section_order"] == ["cover", "content"]


def test_load_with_extension(temp_config_dir):
    """Test loading with explicit .yaml extension."""
    loader = ConfigLoader(temp_config_dir)
    products = loader.load("products.yaml")
    
    assert "products" in products


def test_load_without_extension(temp_config_dir):
    """Test loading without .yaml extension."""
    loader = ConfigLoader(temp_config_dir)
    products = loader.load("products")
    
    assert "products" in products


def test_load_nonexistent_file(temp_config_dir):
    """Test loading a file that doesn't exist."""
    loader = ConfigLoader(temp_config_dir)
    
    with pytest.raises(FileNotFoundError):
        loader.load("nonexistent")


def test_cache_behavior(temp_config_dir):
    """Test that files are cached after first load."""
    loader = ConfigLoader(temp_config_dir)
    
    # First load
    products1 = loader.load_products()
    
    # Modify the underlying file
    with open(Path(temp_config_dir) / "products.yaml", 'w') as f:
        yaml.dump({"products": {"new_product": {}}}, f)
    
    # Second load should return cached version
    products2 = loader.load_products()
    assert products1 == products2
    
    # Clear cache and reload
    loader.clear_cache()
    products3 = loader.load_products()
    assert "new_product" in products3["products"]
