"""Tests for the pdf_generator module."""

import os
import tempfile
from pathlib import Path

import pytest

from src.pdf_generator import PDFGenerator


@pytest.fixture
def generator():
    """Create a PDFGenerator instance."""
    return PDFGenerator()


def test_markdown_to_html_basic(generator):
    """Test converting basic Markdown to HTML."""
    md = "# Title\n\nThis is a paragraph."
    html = generator.markdown_to_html(md)
    
    assert "<h1>Title</h1>" in html
    assert "<p>This is a paragraph.</p>" in html


def test_markdown_to_html_lists(generator):
    """Test converting Markdown lists to HTML."""
    md = "- Item 1\n- Item 2\n- Item 3"
    html = generator.markdown_to_html(md)
    
    assert "<ul>" in html
    assert "<li>Item 1</li>" in html


def test_markdown_to_html_bold(generator):
    """Test converting bold text."""
    md = "This is **bold** text."
    html = generator.markdown_to_html(md)
    
    assert "<strong>bold</strong>" in html


def test_generate_pdf(generator):
    """Test generating a PDF file."""
    md = """# Test Document

This is a test document with some content.

## Section 1

- Item A
- Item B

## Section 2

**Bold text** and *italic text*.

---

End of document.
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_output.pdf"
        generator.generate_pdf(md, str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0


def test_generate_pdf_with_custom_css():
    """Test generating a PDF with custom CSS."""
    custom_css = """
    body { font-size: 14pt; }
    h1 { color: blue; }
    """
    generator = PDFGenerator(custom_css)
    
    md = "# Blue Title\n\nContent here."
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "custom_style.pdf"
        generator.generate_pdf(md, str(output_path))
        
        assert output_path.exists()


def test_default_css_exists(generator):
    """Test that default CSS is defined."""
    assert generator.css is not None
    assert len(generator.css) > 0
    assert "body" in generator.css
