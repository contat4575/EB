"""
Gerador de HTML com múltiplos temas
"""

from typing import List, Dict
from datetime import datetime


class HTMLGenerator:
    """Gerador de HTML premium com múltiplos temas"""
    
    def __init__(self, theme="premium", include_toc=True, responsive=True, 
                 animations=True, dark_mode=True):
        self.theme = theme
        self.include_toc = include_toc
        self.responsive = responsive
        self.animations = animations
        self.dark_mode = dark_mode
    
    def generate(self, pages_data: List[Dict]) -> str:
        """Gera HTML completo"""
        
        # Selecionar CSS baseado no tema
        css = self._get_theme_css()
        
        # Construir HTML
        html = self._build_html_structure(pages_data, css)
        
        return html
    
    def _get_theme_css(self) -> str:
        """Retorna CSS do tema selecionado"""
        
        if self.theme == "premium":
            return self._premium_theme()
        elif self.theme == "medical":
            return self._medical_theme()
        elif self.theme == "modern":
            return self._modern_theme()
        else:  # classic
            return self._classic_theme()
    
    def _premium_theme(self) -> str:
        """Tema premium dark"""
        return '''
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
        
        :root {
            --primary: #00d4ff;
            --primary-dark: #0099cc;
            --secondary: #1e3a8a;
            --dark: #0f172a;
            --darker: #020617;
            --accent: #10b981;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--darker);
            color: #fff;
            overflow-x: hidden;
        }
        
        .hero {
            min-height: 100vh;
            background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
            position: relative;
            padding: 60px 40px;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(0,212,255,0.15) 0%, transparent 70%);
            top: -200px;
            right: -200px;
            animation: float 20s infinite ease-in-out;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            50% { transform: translate(50px, 50px) rotate(180deg); }
        }
        
        .hero-title {
            font-family: 'Poppins', sans-serif;
            font-size: 64px;
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #fff 0%, #00d4ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .drug-card {
            background: linear-gradient(135deg, rgba(30,58,138,0.1) 0%, rgba(15,23,42,0.1) 100%);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 6px solid var(--primary);
            border-radius: 24px;
            padding: 60px;
            margin-bottom: 40px;
            transition: all 0.4s ease;
        }
        
        .drug-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 30px 80px rgba(0,212,255,0.2);
        }
        
        .data-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: rgba(255,255,255,0.03);
            border-radius: 20px;
            overflow: hidden;
        }
        
        .data-table thead {
            background: linear-gradient(135deg, rgba(0,212,255,0.3) 0%, rgba(0,153,204,0.3) 100%);
        }
        
        .data-table th {
            padding: 20px 15px;
            text-align: left;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            color: #fff;
        }
        
        .data-table td {
            padding: 18px 15px;
            font-size: 14px;
            color: rgba(255,255,255,0.85);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .data-table tbody tr:hover {
            background: rgba(0,212,255,0.08);
        }
        '''
    
    def _medical_theme(self) -> str:
        """Tema médico clean"""
        return '''
        @import url('  https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@400;600;700&display=swap');
        
        :root {
            --primary: #0066cc;
            --secondary: #2ecc71;
            --dark: #2c3e50;
            --light: #ecf0f1;
            --white: #ffffff;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Open Sans', sans-serif;
            background: var(--light);
            color: var(--dark);
            line-height: 1.6;
        }
        
        .hero {
            background: linear-gradient(135deg, #0066cc 0%, #004d99 100%);
            color: white;
            padding: 80px 40px;
            text-align: center;
        }
        
        .hero-title {
            font-family: 'Roboto', sans-serif;
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 20px;
        }
        
        .drug-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-left: 6px solid var(--primary);
            border-radius: 8px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .drug-name {
            color: var(--primary);
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 30px;
            border-bottom: 2px solid var(--secondary);
            padding-bottom: 15px;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            margin: 20px 0;
        }
        
        .data-table th {
            background: var(--primary);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .data-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .data-table tbody tr:hover {
            background: #f5f5f5;
        }
        '''
    
    def _modern_theme(self) -> str:
        """Tema moderno com gradientes"""
        return '''
        @import url('  https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&display=swap');
        
        :root {
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        
        .hero {
            min-height: 100vh;
            background: var(--gradient-1);
            padding: 80px 40px;
            color: white;
        }
        
        .hero-title {
            font-size: 72px;
            font-weight: 900;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .drug-card {
            background: white;
            border-radius: 30px;
            padding: 50px;
            margin-bottom: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }
        
        .drug-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 6px;
            background: var(--gradient-2);
        }
        
        .drug-name {
            font-size: 42px;
            font-weight: 900;
            background: var(--gradient-3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
        }
        '''
    
    def _classic_theme(self) -> str:
        """Tema clássico profissional"""
        return '''
        @import url('  https://fonts.googleapis.com/css2?family=Georgia&family=Arial:wght@400;700&display=swap');
        
        :root {
            --primary: #003366;
            --secondary: #666666;
            --accent: #cc0000;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: Georgia, serif;
            background: #ffffff;
            color: #333;
            line-height: 1.8;
        }
        
        .hero {
            background: var(--primary);
            color: white;
            padding: 60px 40px;
            border-bottom: 5px solid var(--accent);
        }
        
        .hero-title {
            font-family: Arial, sans-serif;
            font-size: 42px;
            font-weight: 700;
            text-align: center;
        }
        
        .drug-card {
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-left: 5px solid var(--primary);
            padding: 40px;
            margin-bottom: 30px;
        }
        
        .drug-name {
            color: var(--primary);
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 25px;
            text-transform: uppercase;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .data-table th {
            background: var(--primary);
            color: white;
            padding: 12px;
            text-align: left;
            border: 1px solid #ddd;
        }
        
        .data-table td {
            padding: 10px 12px;
            border: 1px solid #ddd;
        }
        '''
    
    def _build_html_structure(self, pages_data: List[Dict], css: str) -> str:
        """Constrói estrutura HTML completa"""
        
        # Construir CSS adicional condicional
        additional_css_parts = []
        
        if self.responsive:
            additional_css_parts.append('''
@media (max-width: 768px) {
    .hero-title { font-size: 32px; }
    .drug-card { padding: 30px; }
    .data-table { font-size: 12px; overflow-x: auto; }
}
''')
        
        if self.animations:
            additional_css_parts.append('''
.fadeInUp {
    animation: fadeInUp 0.8s ease;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}
''')
        
        full_css = css + "\n" + "\n".join(additional_css_parts)
        
        html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Psicofármacos na Prática | Guia Completo</title>
    <style>
        {full_css}
    </style>
</head>
<body>
'''
        
        # Processar páginas
        for page_data in pages_data:
            html += self._process_page(page_data)
        
        html += '''
</body>
</html>
'''
        
        return html
    
    def _process_page(self, page_data: Dict) -> str:
        """Processa uma página individual"""
        
        text = page_data['text'].strip()
        if not text or len(text) < 15:
            return ""
        
        # Detectar tipo de conteúdo
        content_type = self._detect_type(text, page_data.get('has_table', False))
        
        if content_type == 'index':
            return self._build_index(text)
        elif content_type == 'note':
            return self._build_note(text)
        elif content_type == 'section':
            return self._build_section(text)
        elif content_type == 'table':
            return self._build_table(page_data)
        elif content_type == 'drug':
            return self._build_drug_card(text)
        else:
            return self._build_content(text)
    
    def _detect_type(self, text: str, has_table: bool) -> str:
        """Detecta tipo de conteúdo"""
        text_lower = text.lower()
        
        if 'índice' in text_lower[:100]:
            return 'index'
        if text_lower.startswith('nota'):
            return 'note'
        if has_table or 'tabela' in text_lower:
            return 'table'
        if '•' in text and len(text.split('\n')[0]) < 50:
            return 'drug'
        if len(text) < 200 and any(kw in text_lower for kw in ['antidepressivos', 'antipsicóticos']):
            return 'section'
        
        return 'content'
    
    def _build_index(self, text: str) -> str:
        """Constrói índice"""
        lines = [l.strip() for l in text.split('\n') if l.strip() and '–' in l]
        
        html = '''
<div class="hero">
    <h1 class="hero-title">PSICOFÁRMACOS<br>NA PRÁTICA</h1>
    <p style="text-align: center; font-size: 24px; margin-bottom: 40px;">Guia Completo de Prescrição</p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto;">
'''
        
        for line in lines:
            html += f'<div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 12px;">{line}</div>\n'
        
        html += '</div></div>\n'
        return html
    
    def _build_note(self, text: str) -> str:
        """Constrói caixa de nota"""
        clean = text.replace('Nota', '').strip()
        
        return f'''
<div style="padding: 80px 40px; background: #f0f4f8;">
    <div style="max-width: 1000px; margin: 0 auto; background: white; padding: 50px; border-left: 6px solid #ff9800; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
        <h2 style="color: #ff9800; margin-bottom: 30px; font-size: 32px;">⚠️ Nota Importante</h2>
        <p style="font-size: 16px; line-height: 1.8; color: #333;">{clean}</p>
    </div>
</div>
'''
    
    def _build_section(self, text: str) -> str:
        """Constrói divisor de seção"""
        return f'''
<div style="padding: 150px 40px; text-align: center; background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);">
    <h2 style="font-size: 56px; font-weight: 900; color: white; text-transform: uppercase;">{text}</h2>
</div>
'''
    
    def _build_table(self, page_data: Dict) -> str:
        """Constrói tabela"""
        tables = page_data.get('tables', [])
        
        if not tables:
            return ""
        
        html = '<div style="padding: 80px 40px; background: #0f172a;">\n'
        
        for table in tables:
            if table['type'] in ['camelot', 'pdfplumber']:
                html += '<table class="data-table" style="margin: 0 auto; max-width: 1200px;">\n<thead>\n<tr>\n'
                
                for header in table['headers']:
                    html += f'<th>{header}</th>\n'
                
                html += '</tr>\n</thead>\n<tbody>\n'
                
                for row in table['rows']:
                    html += '<tr>\n'
                    for cell in row:
                        html += f'<td>{cell}</td>\n'
                    html += '</tr>\n'
                
                html += '</tbody>\n</table>\n'
        
        html += '</div>\n'
        return html
    
    def _build_drug_card(self, text: str) -> str:
        """Constrói card de medicamento"""
        lines = text.split('\n')
        drug_name = lines[0].strip() if lines else "MEDICAMENTO"
        
        html = f'''
<div style="padding: 80px 40px; background: #0f172a;">
    <div class="drug-card {'fadeInUp' if self.animations else ''}" style="max-width: 1200px; margin: 0 auto;">
        <h3 class="drug-name">{drug_name}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
'''
        
        # Processar campos
        for line in lines[1:]:
            if line.startswith('•'):
                label = line[1:].strip()
                html += f'''
            <div style="background: rgba(0,212,255,0.05); border: 1px solid rgba(0,212,255,0.2); border-radius: 12px; padding: 20px;">
                <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #00d4ff; margin-bottom: 10px;">{label}</div>
                <div style="font-size: 15px; color: rgba(255,255,255,0.9);">-</div>
            </div>
'''
        
        html += '</div>\n</div>\n</div>\n'
        return html
    
    def _build_content(self, text: str) -> str:
        """Constrói conteúdo genérico"""
        return f'''
<div style="padding: 60px 40px; background: #0f172a;">
    <div style="max-width: 1200px; margin: 0 auto; color: rgba(255,255,255,0.8); font-size: 16px; line-height: 1.8;">
        {text.replace(chr(10), '<br>')}
    </div>
</div>
'''
