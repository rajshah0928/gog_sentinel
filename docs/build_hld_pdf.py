"""
Renders docs/HLD.md into a properly formatted PDF for submission
(Technical Proposal — High-Level Design). Markdown -> styled HTML ->
headless-Chromium print-to-PDF, so headings, tables, code blocks, and
bold/italic all render as a real document rather than raw markdown text.

Run from repo root:
    python docs/build_hld_pdf.py
"""
import sys
from pathlib import Path

import markdown

DOCS_DIR = Path(__file__).resolve().parent
MD_PATH = DOCS_DIR / "HLD.md"
HTML_PATH = DOCS_DIR / "_hld_render.html"
PDF_PATH = DOCS_DIR / "Sentinel_HLD.pdf"
RUVISION_LOGO = DOCS_DIR / "evidence" / "ruvision_logo_small.png"


def main():
    md_text = MD_PATH.read_text()
    body_html = markdown.markdown(
        md_text, extensions=["tables", "fenced_code", "toc"]
    )

    logo_tag = ""
    if RUVISION_LOGO.exists():
        import base64
        b64 = base64.b64encode(RUVISION_LOGO.read_bytes()).decode()
        logo_tag = f'<img src="data:image/png;base64,{b64}" class="brand-logo">'

    html = f"""<!doctype html><html><head><meta charset="utf-8">
    <style>
        @page {{
            size: A4;
            margin: 22mm 18mm 18mm 18mm;
            @bottom-right {{ content: "Page " counter(page); }}
        }}
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #1a1a1a;
            font-size: 11px;
            line-height: 1.55;
        }}
        .brand-logo {{
            position: fixed; top: 6mm; right: 18mm; height: 9mm;
        }}
        .doc-title {{
            font-size: 10px; color: #888; text-transform: uppercase;
            letter-spacing: 0.06em; margin-bottom: 4px;
        }}
        h1 {{
            font-size: 22px; color: #0a0e14; margin-bottom: 2px;
            border-bottom: 2px solid #3b82f6; padding-bottom: 8px;
        }}
        h1 + h2 {{ font-size: 13px; color: #3b82f6; font-weight: 500; margin-top: 6px; margin-bottom: 22px; }}
        h2 {{
            font-size: 15px; color: #0a0e14; margin-top: 26px; margin-bottom: 8px;
            border-bottom: 1px solid #ddd; padding-bottom: 4px;
        }}
        h3 {{ font-size: 12.5px; color: #1e293b; margin-top: 16px; margin-bottom: 6px; }}
        p {{ margin: 6px 0; text-align: justify; }}
        ul, ol {{ margin: 6px 0; padding-left: 20px; }}
        li {{ margin: 3px 0; }}
        strong {{ color: #0a0e14; }}
        code {{
            background: #f1f5f9; padding: 1px 5px; border-radius: 3px;
            font-family: 'SF Mono', Consolas, monospace; font-size: 9.5px; color: #1e40af;
        }}
        pre {{
            background: #0a0e14; color: #e6edf5; padding: 12px 14px;
            border-radius: 6px; overflow-x: auto; font-size: 9px;
            font-family: 'SF Mono', Consolas, monospace; line-height: 1.5;
        }}
        pre code {{ background: none; color: inherit; padding: 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5px; }}
        th {{ background: #0a0e14; color: white; text-align: left; padding: 5px 8px; }}
        td {{ padding: 4px 8px; border-bottom: 1px solid #eee; }}
        tr:nth-child(even) {{ background: #fafafa; }}
        .cover {{
            page-break-after: always; display: flex; flex-direction: column;
            justify-content: center; align-items: center; height: 240mm; text-align: center;
        }}
        .cover h1 {{ border: none; font-size: 34px; margin-bottom: 8px; }}
        .cover .subtitle {{ font-size: 15px; color: #3b82f6; margin-bottom: 30px; }}
        .cover .meta {{ font-size: 11px; color: #666; }}
        .cover .company {{ font-size: 12px; color: #888; margin-top: 60px; }}
    </style></head><body>
    {logo_tag}
    <div class="cover">
        <h1>Sentinel</h1>
        <div class="subtitle">Unified Viewing &amp; Metadata Analytics — Model 2</div>
        <div class="meta">Technical Proposal — High-Level Design (HLD)<br>
        Gujarat Police Innovation Challenge 2026</div>
        <div class="company">Prepared by RuVision Thinking Labs</div>
    </div>
    {body_html}
    </body></html>"""

    HTML_PATH.write_text(html)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{HTML_PATH}")
        page.pdf(
            path=str(PDF_PATH), format="A4",
            print_background=True,
            margin={"top": "22mm", "bottom": "18mm", "left": "18mm", "right": "18mm"},
            display_header_footer=False,
        )
        browser.close()
    HTML_PATH.unlink()
    print(f"Wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
