"""Tests for the submittal_maker module."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from src.submittal_maker import load_project_input, generate_submittal


@pytest.fixture
def sample_project():
    """Sample project data."""
    return {
        "name": "Test Project",
        "number": "TP-001",
        "client": "Test Client",
        "contractor": "Test Contractor",
        "date": "2024-01-01",
        "products": ["anode_magnesium_17lb", "cable_hmwpe_8awg"],
        "sections": [
            {
                "title": "Anodes",
                "description": "Cathodic protection anodes",
                "product_ids": ["anode_magnesium_17lb"]
            },
            {
                "title": "Cables",
                "description": "CP system cables",
                "product_ids": ["cable_hmwpe_8awg"]
            }
        ]
    }


def test_load_project_input_yaml(sample_project):
    """Test loading project input from YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "project.yaml"
        with open(filepath, 'w') as f:
            yaml.dump(sample_project, f)
        
        loaded = load_project_input(str(filepath))
        
        assert loaded["name"] == "Test Project"
        assert loaded["number"] == "TP-001"


def test_load_project_input_json(sample_project):
    """Test loading project input from JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "project.json"
        with open(filepath, 'w') as f:
            json.dump(sample_project, f)
        
        loaded = load_project_input(str(filepath))
        
        assert loaded["name"] == "Test Project"


def test_load_project_input_not_found():
    """Test loading a project file that doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_project_input("/nonexistent/path/project.yaml")


def test_load_project_input_unsupported_format():
    """Test loading a file with unsupported format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "project.txt"
        filepath.write_text("some content")
        
        with pytest.raises(ValueError):
            load_project_input(str(filepath))


def test_generate_submittal_markdown_only(sample_project):
    """Test generating a submittal without PDF output."""
    # Use the actual config directory
    config_dir = Path(__file__).parent.parent / "config"
    
    markdown = generate_submittal(
        sample_project,
        config_dir=str(config_dir),
        output_path=None
    )
    
    assert "# Test Project" in markdown
    assert "TP-001" in markdown
    assert "Test Client" in markdown


def test_generate_submittal_with_pdf(sample_project):
    """Test generating a submittal with PDF output."""
    config_dir = Path(__file__).parent.parent / "config"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "output.pdf"
        
        markdown = generate_submittal(
            sample_project,
            config_dir=str(config_dir),
            output_path=str(output_path)
        )
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        assert "# Test Project" in markdown


def test_generate_submittal_default_values():
    """Test generating a submittal with minimal input."""
    config_dir = Path(__file__).parent.parent / "config"
    
    minimal_project = {
        "products": []
    }
    
    markdown = generate_submittal(
        minimal_project,
        config_dir=str(config_dir),
        output_path=None
    )
    
    assert "# Untitled Project" in markdown
