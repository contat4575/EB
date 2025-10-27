"""
Gerador HTML Avançado
Cria HTML perfeito com design premium e estruturas complexas
"""

from typing import List, Dict
from datetime import datetime


class AdvancedHTMLGenerator:
    """Gerador de HTML com suporte a estruturas complexas"""

    def __init__(self, theme="premium", responsive=True, animations=True):
        self.theme = theme
        self.responsive = responsive
        self.animations = animations

    def generate(self, pages_data: List[Dict]) -> str:
        """Gera HTML completo e otimizado"""

        html = self.build_html_head()

        html += '<body>\n'

        for page_data in pages_data:
            html += self.render_page(page_data)

        html += self.build_html_footer()
        html += '</body>\n</html>'

        return html

    def build_html_head(self) -> str:
        """Constrói cabeçalho HTML com CSS completo"""
        css = self.get_premium_css()

        return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documento Convertido</title>
    <style>
{css}
    </style>
</head>
'''

    def get_premium_css(self) -> str:
        """Retorna CSS premium completo"""
        return '''
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;500;600;700;800;900&display=swap');

:root {
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --secondary: #10b981;
    --accent: #f59e0b;
    --danger: #ef4444;
    --dark: #0f172a;
    --darker: #020617;
    --light: #f8fafc;
    --gray: #64748b;
    --border: #e2e8f0;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    color: #1e293b;
    background: #ffffff;
    font-size: 16px;
}

.page-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 40px 20px;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
    color: var(--dark);
}

h1 {
    font-size: 3rem;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2rem;
}

h2 {
    font-size: 2.25rem;
    color: var(--primary);
    border-bottom: 3px solid var(--primary);
    padding-bottom: 0.5rem;
    margin-top: 3rem;
    margin-bottom: 1.5rem;
}

h3 {
    font-size: 1.75rem;
    color: var(--primary-dark);
    margin-top: 2rem;
}

h4 {
    font-size: 1.25rem;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.hero-section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: relative;
    overflow: hidden;
    padding: 60px 20px;
}

.hero-section::before {
    content: '';
    position: absolute;
    width: 800px;
    height: 800px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    top: -200px;
    right: -200px;
    animation: float 20s infinite ease-in-out;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    50% { transform: translate(30px, 30px) rotate(180deg); }
}

.hero-content {
    text-align: center;
    z-index: 1;
    color: white;
}

.hero-title {
    font-size: 4rem;
    font-weight: 900;
    margin-bottom: 1rem;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.hero-subtitle {
    font-size: 1.5rem;
    opacity: 0.9;
    font-weight: 300;
}

.section {
    margin: 60px 0;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 32px;
    margin: 24px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 10px 15px rgba(0,0,0,0.1);
    border-left: 5px solid var(--primary);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

.card-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
}

.card-body {
    color: #475569;
    line-height: 1.8;
}

.info-card {
    background: linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 100%);
    border-left-color: var(--primary);
}

.warning-card {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-left-color: var(--accent);
}

.alert-card {
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
    border-left-color: var(--danger);
}

.success-card {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-left-color: var(--secondary);
}

table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 32px 0;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 10px 15px rgba(0,0,0,0.1);
}

thead {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
}

th {
    padding: 18px 16px;
    text-align: left;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.875rem;
    letter-spacing: 0.05em;
}

td {
    padding: 16px;
    border-bottom: 1px solid var(--border);
    color: #334155;
    font-size: 0.95rem;
}

tbody tr {
    transition: background 0.2s ease;
}

tbody tr:hover {
    background: #f8fafc;
}

tbody tr:last-child td {
    border-bottom: none;
}

.table-responsive {
    overflow-x: auto;
    margin: 32px 0;
}

.list {
    list-style: none;
    padding: 0;
    margin: 24px 0;
}

.list-item {
    padding: 16px 20px;
    margin: 8px 0;
    background: #f8fafc;
    border-radius: 8px;
    border-left: 4px solid var(--primary);
    display: flex;
    align-items: flex-start;
    gap: 12px;
    transition: all 0.2s ease;
}

.list-item:hover {
    background: #f1f5f9;
    transform: translateX(4px);
}

.list-item::before {
    content: '→';
    color: var(--primary);
    font-weight: 700;
    font-size: 1.25rem;
}

.text-block {
    margin: 24px 0;
    line-height: 1.8;
    color: #475569;
}

.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    margin: 32px 0;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin: 32px 0;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 600;
    margin: 4px;
}

.badge-primary { background: var(--primary); color: white; }
.badge-secondary { background: var(--secondary); color: white; }
.badge-accent { background: var(--accent); color: white; }

.divider {
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--primary) 50%, transparent 100%);
    margin: 60px 0;
}

.highlight {
    background: linear-gradient(120deg, #fef3c7 0%, #fde68a 100%);
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 500;
}

.diagram-container {
    margin: 40px 0;
    padding: 32px;
    background: #f8fafc;
    border-radius: 16px;
    text-align: center;
}

.diagram-container img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    h1 { font-size: 2rem; }
    h2 { font-size: 1.75rem; }
    h3 { font-size: 1.5rem; }

    .card { padding: 20px; }

    table { font-size: 0.875rem; }
    th, td { padding: 12px 8px; }

    .grid-2, .grid-3 {
        grid-template-columns: 1fr;
    }
}

@media print {
    .hero-section { page-break-after: always; }
    .card { page-break-inside: avoid; }
    table { page-break-inside: avoid; }
}

.fadeIn {
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
'''

    def render_page(self, page_data: Dict) -> str:
        """Renderiza uma página completa"""
        structures = page_data.get('structures', {})

        html = '<div class="page-container">\n'

        if page_data['page'] == 1:
            html += self.render_hero(page_data)

        if structures.get('headers'):
            for header in structures['headers']:
                html += self.render_header(header)

        if structures.get('tables'):
            for table in structures['tables']:
                html += self.render_table(table)

        if structures.get('cards'):
            for card in structures['cards']:
                html += self.render_card(card)

        if structures.get('lists'):
            for lst in structures['lists']:
                html += self.render_list(lst)

        if structures.get('diagrams'):
            for diagram in structures['diagrams']:
                html += self.render_diagram(diagram, page_data)

        if structures.get('text_blocks'):
            for text_block in structures['text_blocks']:
                html += self.render_text_block(text_block)

        html += '</div>\n'

        return html

    def render_hero(self, page_data: Dict) -> str:
        """Renderiza seção hero"""
        text = page_data.get('text', '')
        lines = [l.strip() for l in text.split('\n') if l.strip()]

        title = lines[0] if lines else "Documento"
        subtitle = lines[1] if len(lines) > 1 else ""

        return f'''
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">{self.escape_html(title)}</h1>
        {f'<p class="hero-subtitle">{self.escape_html(subtitle)}</p>' if subtitle else ''}
    </div>
</div>
'''

    def render_header(self, header: Dict) -> str:
        """Renderiza cabeçalho"""
        level = header.get('level', 2)
        text = header.get('text', '')

        return f'<h{level} class="fadeIn">{self.escape_html(text)}</h{level}>\n'

    def render_table(self, table: Dict) -> str:
        """Renderiza tabela com design perfeito"""
        table_type = table.get('type', '')

        if table_type in ['structured_table', 'grid_table']:
            data = table.get('data', {})
            headers = data.get('headers', [])
            rows = data.get('rows', [])

            if not headers and not rows:
                return ''

            html = '<div class="table-responsive fadeIn">\n<table>\n'

            if headers:
                html += '<thead>\n<tr>\n'
                for header in headers:
                    html += f'<th>{self.escape_html(str(header))}</th>\n'
                html += '</tr>\n</thead>\n'

            if rows:
                html += '<tbody>\n'
                for row in rows:
                    html += '<tr>\n'
                    for cell in row:
                        html += f'<td>{self.escape_html(str(cell))}</td>\n'
                    html += '</tr>\n'
                html += '</tbody>\n'

            html += '</table>\n</div>\n'

            return html

        return ''

    def render_card(self, card: Dict) -> str:
        """Renderiza card de informação"""
        style = card.get('style', 'info')
        content = card.get('content', '')

        lines = content.split('\n')
        title = lines[0] if lines else ''
        body = '\n'.join(lines[1:]) if len(lines) > 1 else ''

        return f'''
<div class="card {style}-card fadeIn">
    <div class="card-header">{self.escape_html(title)}</div>
    <div class="card-body">{self.escape_html(body)}</div>
</div>
'''

    def render_list(self, lst: Dict) -> str:
        """Renderiza lista"""
        items = lst.get('items', [])

        if not items:
            return ''

        html = '<ul class="list fadeIn">\n'

        for item in items:
            text = item.get('text', '').lstrip('•-→▪◦∙ ')
            html += f'<li class="list-item">{self.escape_html(text)}</li>\n'

        html += '</ul>\n'

        return html

    def render_diagram(self, diagram: Dict, page_data: Dict) -> str:
        """Renderiza diagrama ou imagem"""
        diagram_type = diagram.get('type', '')

        if diagram_type == 'image':
            images = page_data.get('images', [])
            index = diagram.get('index', 0)

            if index < len(images):
                img_path = images[index]
                return f'''
<div class="diagram-container fadeIn">
    <img src="{img_path}" alt="Diagrama" loading="lazy">
</div>
'''

        return ''

    def render_text_block(self, text_block: Dict) -> str:
        """Renderiza bloco de texto"""
        content = text_block.get('content', '')

        if not content.strip():
            return ''

        paragraphs = content.split('\n\n')
        html = '<div class="text-block fadeIn">\n'

        for para in paragraphs:
            if para.strip():
                html += f'<p>{self.escape_html(para.strip())}</p>\n'

        html += '</div>\n'

        return html

    def build_html_footer(self) -> str:
        """Constrói rodapé HTML"""
        now = datetime.now().strftime("%d/%m/%Y %H:%M")

        return f'''
<div class="page-container" style="text-align: center; color: var(--gray); margin-top: 80px; padding: 40px 20px; border-top: 2px solid var(--border);">
    <p>Documento convertido em {now}</p>
</div>
'''

    def escape_html(self, text: str) -> str:
        """Escapa caracteres HTML"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
