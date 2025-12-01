"""Tests for the markdown_assembler module."""

import pytest

from src.markdown_assembler import MarkdownAssembler


@pytest.fixture
def sample_templates():
    """Sample templates for testing."""
    return {
        "cover_page": "# {{ project.name }}\n**Number:** {{ project.number }}",
        "intro_text": "## Introduction\nProject: {{ project.name }}",
        "table_of_contents": "## TOC\n{% for s in sections %}{{ s.number }}. {{ s.title }}\n{% endfor %}",
        "section_header": "## Section {{ section.number }}: {{ section.title }}\n{{ section.description }}",
        "product_entry": "### {{ product.name }}\n**Model:** {{ product.model }}",
        "closing_text": "## Closing\nProject {{ project.name }} complete."
    }


@pytest.fixture
def sample_products():
    """Sample products for testing."""
    return {
        "product_a": {
            "name": "Product A",
            "manufacturer": "Mfg A",
            "model": "PA-100",
            "description": "Description A",
            "specifications": {"power": "10W"},
            "cut_sheet": "a.pdf",
            "msds": None
        },
        "product_b": {
            "name": "Product B",
            "manufacturer": "Mfg B",
            "model": "PB-200",
            "description": "Description B",
            "specifications": {"power": "20W"},
            "cut_sheet": "b.pdf",
            "msds": "b_msds.pdf"
        }
    }


@pytest.fixture
def assembler(sample_templates, sample_products):
    """Create a MarkdownAssembler instance."""
    return MarkdownAssembler(sample_templates, sample_products)


def test_render_cover_page(assembler):
    """Test rendering the cover page."""
    project = {"name": "Test Project", "number": "TP-001"}
    result = assembler.render_cover_page(project)
    
    assert "# Test Project" in result
    assert "**Number:** TP-001" in result


def test_render_intro(assembler):
    """Test rendering the introduction."""
    project = {"name": "Test Project"}
    result = assembler.render_intro(project)
    
    assert "## Introduction" in result
    assert "Project: Test Project" in result


def test_render_toc(assembler):
    """Test rendering the table of contents."""
    sections = [
        {"number": 1, "title": "Section One"},
        {"number": 2, "title": "Section Two"}
    ]
    result = assembler.render_toc(sections)
    
    assert "1. Section One" in result
    assert "2. Section Two" in result


def test_render_section_header(assembler):
    """Test rendering a section header."""
    section = {"number": 1, "title": "Lighting", "description": "LED fixtures"}
    result = assembler.render_section_header(section)
    
    assert "## Section 1: Lighting" in result
    assert "LED fixtures" in result


def test_render_product(assembler):
    """Test rendering a product entry."""
    result = assembler.render_product("product_a")
    
    assert "### Product A" in result
    assert "**Model:** PA-100" in result


def test_render_product_not_found(assembler):
    """Test rendering a product that doesn't exist."""
    with pytest.raises(KeyError):
        assembler.render_product("nonexistent")


def test_render_closing(assembler):
    """Test rendering the closing text."""
    project = {"name": "Test Project"}
    result = assembler.render_closing(project)
    
    assert "## Closing" in result
    assert "Project Test Project complete" in result


def test_assemble_submittal(assembler):
    """Test assembling a complete submittal."""
    project = {
        "name": "Full Test",
        "number": "FT-001",
        "client": "Client",
        "contractor": "Contractor",
        "date": "2024-01-01"
    }
    
    sections = [
        {
            "title": "Products",
            "description": "All products",
            "product_ids": ["product_a", "product_b"]
        }
    ]
    
    product_ids = ["product_a", "product_b"]
    
    result = assembler.assemble_submittal(project, sections, product_ids)
    
    # Check all parts are present
    assert "# Full Test" in result
    assert "## Introduction" in result
    assert "## TOC" in result
    assert "## Section 1: Products" in result
    assert "### Product A" in result
    assert "### Product B" in result
    assert "## Closing" in result


def test_get_section_products_by_ids(assembler):
    """Test getting products by explicit IDs."""
    section = {"product_ids": ["product_a"]}
    all_ids = ["product_a", "product_b"]
    
    result = assembler._get_section_products(section, all_ids)
    
    assert result == ["product_a"]


def test_get_section_products_by_category(assembler):
    """Test getting products by category prefix."""
    section = {"product_categories": ["product"]}
    all_ids = ["product_a", "product_b", "other_c"]
    
    result = assembler._get_section_products(section, all_ids)
    
    assert "product_a" in result
    assert "product_b" in result
    assert "other_c" not in result
