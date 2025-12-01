"""Main script for generating submittal documents."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from .config_loader import ConfigLoader
from .markdown_assembler import MarkdownAssembler
from .pdf_generator import PDFGenerator


def load_project_input(input_path: str) -> dict[str, Any]:
    """Load project input from a YAML or JSON file.
    
    Args:
        input_path: Path to the project input file.
        
    Returns:
        Dictionary containing project data.
        
    Raises:
        FileNotFoundError: If the input file doesn't exist.
        ValueError: If the file format is not supported.
    """
    path = Path(input_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Project input file not found: {input_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        if path.suffix in ('.yaml', '.yml'):
            return yaml.safe_load(f)
        elif path.suffix == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")


def generate_submittal(
    project_input: dict[str, Any],
    config_dir: str | None = None,
    output_path: str | None = None,
    custom_css: str | None = None
) -> str:
    """Generate a submittal document.
    
    Args:
        project_input: Dictionary containing project data and product list.
        config_dir: Path to configuration directory.
        output_path: Path for output PDF. If None, returns Markdown only.
        custom_css: Optional custom CSS for PDF styling.
        
    Returns:
        Generated Markdown content.
    """
    # Load configurations
    config = ConfigLoader(config_dir)
    products_config = config.load_products()
    templates_config = config.load_templates()
    sections_config = config.load_sections()
    
    # Get project info with defaults
    project = {
        "name": project_input.get("name", "Untitled Project"),
        "number": project_input.get("number", "N/A"),
        "client": project_input.get("client", "N/A"),
        "contractor": project_input.get("contractor", "N/A"),
        "date": project_input.get("date", date.today().isoformat()),
    }
    
    # Get product IDs from input
    product_ids = project_input.get("products", [])
    
    # Get sections - use custom sections from input or defaults
    product_sections = project_input.get(
        "sections",
        sections_config.get("default_product_sections", [])
    )
    
    # Create assembler and generate Markdown
    assembler = MarkdownAssembler(
        templates_config.get("templates", {}),
        products_config.get("products", {})
    )
    
    markdown_content = assembler.assemble_submittal(
        project,
        product_sections,
        product_ids
    )
    
    # Generate PDF if output path provided
    if output_path:
        generator = PDFGenerator(custom_css)
        generator.generate_pdf(markdown_content, output_path)
        print(f"PDF generated: {output_path}")
    
    return markdown_content


def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description="Generate submittal documents from project input"
    )
    parser.add_argument(
        "input",
        help="Path to project input file (YAML or JSON)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file path",
        default=None
    )
    parser.add_argument(
        "-c", "--config-dir",
        help="Path to configuration directory",
        default=None
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Output Markdown to stdout instead of PDF"
    )
    parser.add_argument(
        "--css",
        help="Path to custom CSS file for PDF styling",
        default=None
    )
    
    args = parser.parse_args()
    
    try:
        # Load project input
        project_input = load_project_input(args.input)
        
        # Load custom CSS if provided
        custom_css = None
        if args.css:
            with open(args.css, 'r', encoding='utf-8') as f:
                custom_css = f.read()
        
        # Determine output path
        if args.markdown_only:
            output_path = None
        elif args.output:
            output_path = args.output
        else:
            # Default to input filename with .pdf extension
            input_path = Path(args.input)
            output_path = str(input_path.with_suffix('.pdf'))
        
        # Generate submittal
        markdown_content = generate_submittal(
            project_input,
            config_dir=args.config_dir,
            output_path=output_path,
            custom_css=custom_css
        )
        
        if args.markdown_only:
            print(markdown_content)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
