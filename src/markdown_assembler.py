"""Markdown assembler for generating submittal content."""

from typing import Any

from jinja2 import Template


class MarkdownAssembler:
    """Assembles Markdown content from templates and data."""

    def __init__(self, templates: dict[str, str], products: dict[str, Any]):
        """Initialize the Markdown assembler.
        
        Args:
            templates: Dictionary of template name to template string.
            products: Dictionary of product definitions.
        """
        self.templates = templates
        self.products = products
        self._compiled_templates: dict[str, Template] = {}

    def _get_template(self, template_name: str) -> Template:
        """Get a compiled Jinja2 template.
        
        Args:
            template_name: Name of the template to retrieve.
            
        Returns:
            Compiled Jinja2 Template object.
            
        Raises:
            KeyError: If the template doesn't exist.
        """
        if template_name not in self._compiled_templates:
            template_str = self.templates.get(template_name)
            if template_str is None:
                raise KeyError(f"Template not found: {template_name}")
            self._compiled_templates[template_name] = Template(template_str)
        return self._compiled_templates[template_name]

    def render_template(self, template_name: str, **context: Any) -> str:
        """Render a template with the given context.
        
        Args:
            template_name: Name of the template to render.
            **context: Variables to pass to the template.
            
        Returns:
            Rendered Markdown string.
        """
        template = self._get_template(template_name)
        return template.render(**context)

    def render_cover_page(self, project: dict[str, Any]) -> str:
        """Render the cover page.
        
        Args:
            project: Project information dictionary.
            
        Returns:
            Rendered cover page Markdown.
        """
        return self.render_template("cover_page", project=project)

    def render_intro(self, project: dict[str, Any]) -> str:
        """Render the introduction text.
        
        Args:
            project: Project information dictionary.
            
        Returns:
            Rendered introduction Markdown.
        """
        return self.render_template("intro_text", project=project)

    def render_toc(self, sections: list[dict[str, Any]]) -> str:
        """Render the table of contents.
        
        Args:
            sections: List of section dictionaries with title and number.
            
        Returns:
            Rendered table of contents Markdown.
        """
        return self.render_template("table_of_contents", sections=sections)

    def render_section_header(self, section: dict[str, Any]) -> str:
        """Render a section header.
        
        Args:
            section: Section dictionary with number, title, and description.
            
        Returns:
            Rendered section header Markdown.
        """
        return self.render_template("section_header", section=section)

    def render_product(self, product_id: str) -> str:
        """Render a product entry.
        
        Args:
            product_id: ID of the product in the products dictionary.
            
        Returns:
            Rendered product entry Markdown.
            
        Raises:
            KeyError: If the product doesn't exist.
        """
        product = self.products.get(product_id)
        if product is None:
            raise KeyError(f"Product not found: {product_id}")
        return self.render_template("product_entry", product=product)

    def render_closing(self, project: dict[str, Any]) -> str:
        """Render the closing text.
        
        Args:
            project: Project information dictionary.
            
        Returns:
            Rendered closing text Markdown.
        """
        return self.render_template("closing_text", project=project)

    def assemble_submittal(
        self,
        project: dict[str, Any],
        product_sections: list[dict[str, Any]],
        product_ids: list[str]
    ) -> str:
        """Assemble a complete submittal document.
        
        Args:
            project: Project information dictionary.
            product_sections: List of section definitions.
            product_ids: List of product IDs to include.
            
        Returns:
            Complete assembled Markdown document.
        """
        parts = []
        
        # Cover page
        parts.append(self.render_cover_page(project))
        
        # Introduction
        parts.append(self.render_intro(project))
        
        # Prepare sections for TOC
        toc_sections = []
        for i, section in enumerate(product_sections, start=1):
            toc_sections.append({
                "number": i,
                "title": section.get("title", f"Section {i}")
            })
        
        # Table of contents
        parts.append(self.render_toc(toc_sections))
        
        # Product sections
        for i, section in enumerate(product_sections, start=1):
            section_data = {
                "number": i,
                "title": section.get("title", f"Section {i}"),
                "description": section.get("description", "")
            }
            parts.append(self.render_section_header(section_data))
            
            # Get products for this section
            section_product_ids = self._get_section_products(
                section, product_ids
            )
            
            for product_id in section_product_ids:
                try:
                    parts.append(self.render_product(product_id))
                except KeyError:
                    # Skip products that don't exist
                    pass
        
        # Closing
        parts.append(self.render_closing(project))
        
        return "\n".join(parts)

    def _get_section_products(
        self,
        section: dict[str, Any],
        all_product_ids: list[str]
    ) -> list[str]:
        """Get product IDs that belong to a section.
        
        Args:
            section: Section definition with product_categories or product_ids.
            all_product_ids: List of all product IDs in the project.
            
        Returns:
            List of product IDs for this section.
        """
        # If section has explicit product_ids, use those
        if "product_ids" in section:
            return [pid for pid in section["product_ids"] if pid in all_product_ids]
        
        # Otherwise, filter by category prefixes
        categories = section.get("product_categories", [])
        if not categories:
            return []
        
        matching = []
        for product_id in all_product_ids:
            for category in categories:
                if product_id.startswith(category):
                    matching.append(product_id)
                    break
        
        return matching
