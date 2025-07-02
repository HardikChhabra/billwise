import markdown
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.utils.safestring import mark_safe
from pathlib import Path

@require_GET
def readme_view(request):
    readme_path = Path(__file__).resolve().parent.parent / "README.md"
    if not readme_path.exists():
        return HttpResponse("README.md not found.", status=404)

    # Read the markdown content
    with open(readme_path, encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML with syntax highlighting
    html = markdown.markdown(
        md_content,
        extensions=["fenced_code", "codehilite", "tables"]
    )

    # Wrap with GitHub-like styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>README</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pygments/2.10.0/styles/github.min.css">
        <style>
            body {{
                background: #f6f8fa;
                padding: 2rem;
                display: flex;
                justify-content: center;
            }}
            .markdown-body {{
                background: white;
                padding: 2rem;
                border-radius: 10px;
                max-width: 800px;
                width: 100%;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <article class="markdown-body">
            {html}
        </article>
    </body>
    </html>
    """
    return HttpResponse(mark_safe(full_html))  # safe because we control the source
