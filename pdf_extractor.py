"""
Módulo de Extração de PDFs
Suporta múltiplos métodos de extração
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Callable, Optional


try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


class PDFExtractor:
    """Extrator de PDFs com múltiplos métodos"""
    
    def __init__(self, method: str = "auto", log_callback: Optional[Callable] = None):
        self.method = method
        self.log = log_callback or print
        
        # Verificar bibliotecas disponíveis
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Verifica dependências instaladas"""
        if self.method == "camelot" and not CAMELOT_AVAILABLE:
            self.log("⚠️ Camelot não instalado. Usando PyMuPDF.", "warning")
            self.method = "pymupdf"
        
        if self.method == "pdfplumber" and not PDFPLUMBER_AVAILABLE:
            self.log("⚠️ PDFPlumber não instalado. Usando PyMuPDF.", "warning")
            self.method = "pymupdf"
    
    def extract(self, pdf_path: Path) -> List[Dict]:
        """Extrai dados do PDF usando o método configurado"""
        
        if self.method == "auto":
            return self._auto_extract(pdf_path)
        elif self.method == "camelot":
            return self._camelot_extract(pdf_path)
        elif self.method == "pdfplumber":
            return self._pdfplumber_extract(pdf_path)
        else:  # pymupdf
            return self._pymupdf_extract(pdf_path)
    
    def _auto_extract(self, pdf_path: Path) -> List[Dict]:
        """Método automático: tenta o melhor método disponível"""
        
        # Primeiro, extrair com PyMuPDF para análise
        pages = self._pymupdf_extract(pdf_path)
        
        # Detectar se há tabelas
        has_tables = self._detect_tables(pages)
        
        if has_tables:
            self.log("Tabelas detectadas. Usando método avançado...", "info")
            
            if CAMELOT_AVAILABLE:
                pages = self._camelot_extract(pdf_path)
            elif PDFPLUMBER_AVAILABLE:
                pages = self._pdfplumber_extract(pdf_path)
        
        return pages
    
    def _detect_tables(self, pages: List[Dict]) -> bool:
        """Detecta se há tabelas no documento"""
        keywords = ['tabela', 'equivalência', 'efeitos adversos', '|', '─']
        
        for page in pages:
            text = page['text'].lower()
            if any(kw in text for kw in keywords):
                return True
        
        return False
    
    def _pymupdf_extract(self, pdf_path: Path) -> List[Dict]:
        """Extração básica com PyMuPDF"""
        self.log("Extraindo com PyMuPDF...", "info")
        
        doc = fitz.open(pdf_path)
        pages = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Tentar detectar tabelas manualmente
            tables = self._detect_tables_pymupdf(page)
            
            pages.append({
                'page': page_num + 1,
                'text': text,
                'has_table': len(tables) > 0,
                'tables': tables,
                'method': 'pymupdf'
            })
        
        doc.close()
        return pages
    
    def _detect_tables_pymupdf(self, page) -> List[Dict]:
        """Detecção manual de tabelas com PyMuPDF"""
        tables = []
        
        # Procurar por linhas horizontais e verticais
        drawings = page.get_drawings()
        
        h_lines = []
        v_lines = []
        
        for drawing in drawings:
            for item in drawing['items']:
                if item[0] == 'l':  # linha
                    # Verificar se 'item' tem pelo menos 5 elementos antes de acessar índices
                    if len(item) >= 5:
                        x1, y1, x2, y2 = item[1], item[2], item[3], item[4]
                        
                        if abs(y1 - y2) < 2:  # linha horizontal
                            h_lines.append((x1, y1, x2, y2))
                        elif abs(x1 - x2) < 2:  # linha vertical
                            v_lines.append((x1, y1, x2, y2))
                    # Se o item não tiver 5 elementos, ignora (evita IndexError)
        
        # Se há linhas suficientes, provavelmente é uma tabela
        if len(h_lines) >= 2 and len(v_lines) >= 2:
            tables.append({
                'type': 'detected',
                'h_lines': len(h_lines),
                'v_lines': len(v_lines)
            })
        
        return tables
    
    def _camelot_extract(self, pdf_path: Path) -> List[Dict]:
        """Extração com Camelot (melhor para tabelas)"""
        self.log("Extraindo com Camelot...", "info")
        
        # Primeiro extrair texto base
        pages = self._pymupdf_extract(pdf_path)
        
        try:
            # Extrair tabelas com Camelot
            tables = camelot.read_pdf(str(pdf_path), pages='all', flavor='lattice')
            
            if not tables:
                self.log("Tentando modo 'stream'...", "info")
                tables = camelot.read_pdf(str(pdf_path), pages='all', flavor='stream')
            
            self.log(f"✓ {len(tables)} tabela(s) detectada(s)", "success")
            
            # Associar tabelas às páginas
            for table in tables:
                page_num = table.page - 1
                
                if 0 <= page_num < len(pages):
                    df = table.df
                    
                    # Converter DataFrame para estrutura útil
                    headers = df.iloc[0].tolist() if len(df) > 0 else []
                    rows = df.iloc[1:].values.tolist() if len(df) > 1 else []
                    
                    pages[page_num]['has_table'] = True
                    pages[page_num]['tables'].append({
                        'type': 'camelot',
                        'headers': headers,
                        'rows': rows,
                        'accuracy': table.accuracy
                    })
        
        except Exception as e:
            self.log(f"Erro com Camelot: {e}", "warning")
        
        return pages
    
    def _pdfplumber_extract(self, pdf_path: Path) -> List[Dict]:
        """Extração com PDFPlumber"""
        self.log("Extraindo com PDFPlumber...", "info")
        
        pages = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extrair texto
                text = page.extract_text() or ""
                
                # Extrair tabelas
                tables = page.extract_tables()
                
                processed_tables = []
                for table in tables:
                    if table and len(table) > 1:
                        # Corrigido: Verificar se a linha tem elementos antes de acessar
                        headers = table[0] if len(table) > 0 else []
                        rows = table[1:] if len(table) > 1 else []
                        
                        processed_tables.append({
                            'type': 'pdfplumber',
                            'headers': headers,
                            'rows': rows
                        })
                
                pages.append({
                    'page': page_num + 1,
                    'text': text,
                    'has_table': len(processed_tables) > 0,
                    'tables': processed_tables,
                    'method': 'pdfplumber'
                })
        
        return pages
    
    def parse_drug_info(self, text: str) -> tuple:
        """Parseia informações de medicamento"""
        lines = text.split('\n')
        drug_name = None
        fields = []
        current_label = None
        current_value = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detectar nome do medicamento
            if not drug_name and line.isupper() and 3 < len(line) < 50:
                drug_name = line
                continue
            
            # Detectar campos (começam com •)
            if line.startswith('•'):
                if current_label:
                    fields.append({
                        'label': current_label,
                        'value': ' '.join(current_value).strip()
                    })
                current_label = line[1:].strip()
                current_value = []
            else:
                current_value.append(line)
        
        # Adicionar último campo
        if current_label:
            fields.append({
                'label': current_label,
                'value': ' '.join(current_value).strip()
            })
        
        return drug_name, fields
    
    def detect_content_type(self, text: str, has_table: bool) -> str:
        """Detecta tipo de conteúdo da página"""
        text_clean = text.strip().lower()
        
        # Índice
        if 'índice' in text_clean[:100] or 'consulta rápida' in text_clean[:100]:
            return 'index'
        
        # Nota
        if text_clean.startswith('nota'):
            return 'note'
        
        # Seção
        section_keywords = [
            'antidepressivos', 'antipsicóticos', 'estabilizadores',
            'benzodiazepínicos', 'opioides', 'canabinoides', 'parkinson',
            'hipnóticos', 'psicoestimulantes', 'tricíclicos'
        ]
        if len(text) < 200 and any(kw in text_clean for kw in section_keywords):
            return 'section'
        
        # Tabela
        if has_table or 'tabela' in text_clean:
            return 'table'
        
        # Medicamento
        if '•' in text and any(line.strip().isupper() for line in text.split('\n')[:3]):
            return 'drug'
        
        return 'content'