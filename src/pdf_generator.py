"""PDF generator for creating submittal documents."""

import markdown
from weasyprint import HTML, CSS


class PDFGenerator:
    """Generates PDF documents from Markdown content."""

    DEFAULT_CSS = """
    @page {
        size: letter;
        margin: 1in;
    }
    
    body {
        font-family: 'Helvetica', 'Arial', sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #333;
    }
    
    h1 {
        font-size: 24pt;
        color: #1a1a1a;
        border-bottom: 2px solid #1a1a1a;
        padding-bottom: 10pt;
        margin-top: 0;
    }
    
    h2 {
        font-size: 18pt;
        color: #333;
        margin-top: 24pt;
        page-break-before: auto;
    }
    
    h3 {
        font-size: 14pt;
        color: #444;
        margin-top: 18pt;
    }
    
    h4 {
        font-size: 12pt;
        color: #555;
        margin-top: 12pt;
    }
    
    p {
        margin: 6pt 0;
    }
    
    ul, ol {
        margin: 6pt 0;
        padding-left: 20pt;
    }
    
    li {
        margin: 3pt 0;
    }
    
    hr {
        border: none;
        border-top: 1px solid #ccc;
        margin: 18pt 0;
    }
    
    strong {
        font-weight: bold;
    }
    
    em {
        font-style: italic;
        color: #666;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 12pt 0;
    }
    
    th, td {
        border: 1px solid #ccc;
        padding: 6pt 12pt;
        text-align: left;
    }
    
    th {
        background-color: #f5f5f5;
        font-weight: bold;
    }
    
    .cover-page {
        text-align: center;
        padding-top: 2in;
    }
    
    .page-break {
        page-break-after: always;
    }
    """

    def __init__(self, custom_css: str | None = None):
        """Initialize the PDF generator.
        
        Args:
            custom_css: Optional custom CSS to use instead of default.
        """
        self.css = custom_css if custom_css else self.DEFAULT_CSS

    def markdown_to_html(self, md_content: str) -> str:
        """Convert Markdown content to HTML.
        
        Args:
            md_content: Markdown content string.
            
        Returns:
            HTML string.
        """
        html_body = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code']
        )
        
        html_document = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Submittal Package</title>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        
        return html_document

    def generate_pdf(self, md_content: str, output_path: str) -> None:
        """Generate a PDF from Markdown content.
        
        Args:
            md_content: Markdown content string.
            output_path: Path to save the PDF file.
        """
        html_content = self.markdown_to_html(md_content)
        
        html = HTML(string=html_content)
        css = CSS(string=self.css)
        
        html.write_pdf(output_path, stylesheets=[css])

    def generate_pdf_from_html(self, html_content: str, output_path: str) -> None:
        """Generate a PDF from HTML content.
        
        Args:
            html_content: HTML content string.
            output_path: Path to save the PDF file.
        """
        html = HTML(string=html_content)
        css = CSS(string=self.css)
        
        html.write_pdf(output_path, stylesheets=[css])
