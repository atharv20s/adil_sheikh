import os
from html2image import Html2Image

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
hti = Html2Image(browser_executable=edge_path, size=(1200, 700))

html = """<!DOCTYPE html>
<html>
<head>
<style>
body { font-family: 'Segoe UI', system-ui, sans-serif; background: #f8fafc; margin: 0; padding: 40px; }
.card { background: white; border-radius: 16px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; }
h1 { color: #0f172a; margin-top: 0; }
.badge { background: #dcfce7; color: #15803d; padding: 6px 12px; border-radius: 20px; font-weight: 600; display: inline-block; }
</style>
</head>
<body>
<div class="card">
  <span class="badge">IEEE Transactions Standard</span>
  <h1>Modern HTML + CSS Diagram Engine</h1>
  <p>Ultra-sleek typography, glassmorphism, zero overlapping labels, crystal clear high-resolution graphics.</p>
</div>
</body>
</html>"""

hti.screenshot(html_str=html, save_as="test_css_render.png")
print("test_css_render.png exists:", os.path.exists("test_css_render.png"))
