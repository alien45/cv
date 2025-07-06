import markdown
from weasyprint import HTML
import re

# 📄 Header block to show only in PDF
pdf_header = """
# Toufiqur R. Chowdhury

📧 Email: htr.letun@gmail.com  
📱 Phone: +90 535 508 6931  
🔗 [linkedin.com/in/toufiq](https://linkedin.com/in/toufiq)  
💻 [github.com/alien45](https://github.com/alien45)
"""

# Load README.md
with open("README.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Remove blocks marked for exclusion
md_content = re.sub(r'<!-- PDF-IGNORE-START -->.*?<!-- PDF-IGNORE-END -->', '', md_content, flags=re.DOTALL)

# Remove single-line ignores
md_content = "\n".join(
    line for line in md_content.splitlines()
    if "<!-- PDF-IGNORE -->" not in line
)

# Prepend PDF header
md_content = pdf_header.strip() + "\n\n" + md_content

# Convert to HTML
html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

# Optional: Basic styling
style = """
<style>
  body { font-family: sans-serif; padding: 30px; max-width: 800px; margin: auto; }
  h1, h2, h3 { color: #2c3e50; margin-top: 1.4em; }
  a { color: #0366d6; text-decoration: none; }
  code { background: #f6f8fa; padding: 2px 4px; font-size: 90%; }
  ul, ol { margin-left: 1.5em; }
  pre { background: #f0f0f0; padding: 10px; overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; margin-top: 1em; }
  th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
</style>
"""

# Wrap and export
html_page = f"<!DOCTYPE html><html><head>{style}</head><body>{html_content}</body></html>"
HTML(string=html_page).write_pdf("Toufiqur_Chowdhury_CV.pdf")
