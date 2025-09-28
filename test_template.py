#!/usr/bin/env python3
"""Test script to validate Jinja2 template syntax"""

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
import os

def test_template(template_path):
    """Test if a Jinja2 template has valid syntax"""
    try:
        # Get the directory and filename
        template_dir = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(template_dir or '.'))
        
        # Try to load and parse the template
        template = env.get_template(template_name)
        print(f"✅ Template {template_path} has valid syntax")
        return True
        
    except TemplateSyntaxError as e:
        print(f"❌ Syntax error in {template_path}:")
        print(f"   Line {e.lineno}: {e.message}")
        return False
    except Exception as e:
        print(f"❌ Error testing {template_path}: {e}")
        return False

if __name__ == "__main__":
    # Test the reports.html template
    template_path = "templates/admin/reports.html"
    test_template(template_path)
