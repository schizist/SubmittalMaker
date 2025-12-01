# SubmittalMaker

A data-driven submittal generator that takes simple project input and automatically creates a full PDF with cut sheets, MSDS, intro text, and sections. All rules live in YAML files—products, templates, and section order—so updates don't require code changes.

## Features

- **YAML-driven configuration**: Products, templates, and section order are all defined in easy-to-edit YAML files
- **Template-based generation**: Uses Jinja2 templates for flexible content formatting
- **Markdown intermediate format**: Content is assembled as Markdown before PDF conversion
- **Clean PDF output**: Professional-looking submittals with consistent styling
- **CLI interface**: Easy command-line usage for automation
- **Extensible**: Add new products, templates, or sections without code changes

## Installation

```bash
# Clone the repository
git clone https://github.com/schizist/SubmittalMaker.git
cd SubmittalMaker

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

1. Create a project input file (YAML or JSON):

```yaml
name: "Office Building Lighting Upgrade"
number: "2024-001"
client: "ABC Commercial Properties"
contractor: "XYZ Electrical Contractors"
date: "2024-01-15"

products:
  - led_panel_1
  - led_downlight_1
  - emergency_exit_1
  - wire_12awg
  - conduit_emt
```

2. Generate a submittal:

```bash
python -m src.submittal_maker my_project.yaml -o submittal.pdf
```

## Usage

```bash
# Generate PDF (default output name based on input file)
python -m src.submittal_maker project.yaml

# Specify output file
python -m src.submittal_maker project.yaml -o output.pdf

# Output Markdown only (for preview or debugging)
python -m src.submittal_maker project.yaml --markdown-only

# Use custom config directory
python -m src.submittal_maker project.yaml -c /path/to/config

# Use custom CSS for PDF styling
python -m src.submittal_maker project.yaml --css custom_style.css
```

## Configuration Files

### `config/products.yaml`

Defines the product catalog with specifications, cut sheets, and MSDS references:

```yaml
products:
  led_panel_1:
    name: "LED Panel Light 2x4"
    manufacturer: "LumiTech"
    model: "LT-2440"
    description: "High-efficiency 2x4 LED panel"
    specifications:
      wattage: "40W"
      lumens: "4800lm"
    cut_sheet: "cut_sheets/lt_2440.pdf"
    msds: "msds/lt_2440_msds.pdf"
```

### `config/templates.yaml`

Defines Jinja2 templates for document sections:

```yaml
templates:
  cover_page: |
    # {{ project.name }}
    **Project Number:** {{ project.number }}
    
  product_entry: |
    ### {{ product.name }}
    **Manufacturer:** {{ product.manufacturer }}
    {% for key, value in product.specifications.items() %}
    - **{{ key | title }}:** {{ value }}
    {% endfor %}
```

### `config/sections.yaml`

Defines the document structure and section order:

```yaml
section_order:
  - cover_page
  - intro_text
  - table_of_contents
  - product_sections
  - closing_text

default_product_sections:
  - id: lighting
    title: "Lighting Fixtures"
    description: "LED panels and downlights"
    product_categories:
      - led_panel
      - led_downlight
```

## Project Input Format

Project input files can be YAML or JSON format:

```yaml
name: "Project Name"           # Required
number: "2024-001"             # Project number
client: "Client Name"          # Client/owner
contractor: "Contractor Name"  # Submitting contractor
date: "2024-01-15"            # Submission date

products:                      # List of product IDs to include
  - led_panel_1
  - wire_12awg

sections:                      # Optional: override default sections
  - id: custom_section
    title: "Custom Section"
    description: "Custom description"
    product_ids:
      - led_panel_1
```

## Project Structure

```
SubmittalMaker/
├── config/
│   ├── products.yaml      # Product catalog
│   ├── templates.yaml     # Document templates
│   └── sections.yaml      # Section order and structure
├── src/
│   ├── __init__.py
│   ├── config_loader.py   # YAML configuration loader
│   ├── markdown_assembler.py  # Content assembly
│   ├── pdf_generator.py   # PDF output
│   └── submittal_maker.py # Main script/CLI
├── tests/                 # Test suite
├── examples/              # Example project files
├── requirements.txt
└── README.md
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## License

MIT License