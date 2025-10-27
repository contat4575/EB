"""
Módulo Avançado de Detecção de Estruturas
Reconhece tabelas, cards, diagramas e layouts complexos
"""

import fitz
from typing import List, Dict, Tuple, Optional
import re


class StructureDetector:
    """Detecta estruturas complexas em PDFs"""

    def __init__(self):
        self.min_table_lines = 3
        self.min_card_elements = 2
        self.diagram_keywords = ['diagrama', 'fluxo', 'esquema', 'figura']

    def analyze_page(self, page: fitz.Page) -> Dict:
        """Analisa estrutura completa de uma página"""

        page_dict = page.get_text("dict")
        blocks = page_dict.get("blocks", [])

        structures = {
            'tables': self.detect_tables(page, blocks),
            'cards': self.detect_cards(blocks),
            'diagrams': self.detect_diagrams(page, blocks),
            'lists': self.detect_lists(blocks),
            'headers': self.detect_headers(blocks),
            'text_blocks': self.detect_text_blocks(blocks),
            'layout_type': self.classify_layout(blocks)
        }

        return structures

    def detect_tables(self, page: fitz.Page, blocks: List[Dict]) -> List[Dict]:
        """Detecta tabelas com precisão"""
        tables = []

        drawings = page.get_drawings()
        h_lines = []
        v_lines = []

        for drawing in drawings:
            for item in drawing.get('items', []):
                if item[0] == 'l' and len(item) >= 5:
                    x1, y1, x2, y2 = item[1:5]

                    if abs(y1 - y2) < 2:
                        h_lines.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})
                    elif abs(x1 - x2) < 2:
                        v_lines.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

        if len(h_lines) >= self.min_table_lines and len(v_lines) >= 2:
            cells = self.extract_table_cells(page, h_lines, v_lines)

            if cells:
                table_data = self.parse_table_structure(cells)
                tables.append({
                    'type': 'structured_table',
                    'cells': cells,
                    'data': table_data,
                    'h_lines': len(h_lines),
                    'v_lines': len(v_lines),
                    'bbox': self.get_table_bbox(h_lines, v_lines)
                })

        grid_tables = self.detect_grid_tables(blocks)
        tables.extend(grid_tables)

        return tables

    def extract_table_cells(self, page: fitz.Page, h_lines: List[Dict],
                           v_lines: List[Dict]) -> List[Dict]:
        """Extrai células de uma tabela"""
        cells = []

        h_lines_sorted = sorted(h_lines, key=lambda l: l['y1'])
        v_lines_sorted = sorted(v_lines, key=lambda l: l['x1'])

        for i in range(len(h_lines_sorted) - 1):
            for j in range(len(v_lines_sorted) - 1):
                x0 = v_lines_sorted[j]['x1']
                y0 = h_lines_sorted[i]['y1']
                x1 = v_lines_sorted[j + 1]['x1']
                y1 = h_lines_sorted[i + 1]['y1']

                rect = fitz.Rect(x0, y0, x1, y1)
                text = page.get_textbox(rect).strip()

                cells.append({
                    'row': i,
                    'col': j,
                    'text': text,
                    'bbox': (x0, y0, x1, y1)
                })

        return cells

    def parse_table_structure(self, cells: List[Dict]) -> Dict:
        """Parse estrutura da tabela em headers e rows"""
        if not cells:
            return {'headers': [], 'rows': []}

        max_row = max(cell['row'] for cell in cells)
        max_col = max(cell['col'] for cell in cells)

        grid = [['' for _ in range(max_col + 1)] for _ in range(max_row + 1)]

        for cell in cells:
            grid[cell['row']][cell['col']] = cell['text']

        headers = grid[0] if grid else []
        rows = grid[1:] if len(grid) > 1 else []

        return {'headers': headers, 'rows': rows}

    def get_table_bbox(self, h_lines: List[Dict], v_lines: List[Dict]) -> Tuple:
        """Obtém bounding box da tabela"""
        if not h_lines or not v_lines:
            return (0, 0, 0, 0)

        x_coords = [l['x1'] for l in v_lines] + [l['x2'] for l in v_lines]
        y_coords = [l['y1'] for l in h_lines] + [l['y2'] for l in h_lines]

        return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))

    def detect_grid_tables(self, blocks: List[Dict]) -> List[Dict]:
        """Detecta tabelas sem bordas (grid baseado em alinhamento)"""
        tables = []

        text_blocks = [b for b in blocks if b.get('type') == 0]

        aligned_groups = self.find_aligned_text(text_blocks)

        for group in aligned_groups:
            if len(group) >= self.min_table_lines:
                table_data = self.parse_aligned_table(group)
                tables.append({
                    'type': 'grid_table',
                    'data': table_data,
                    'blocks': group
                })

        return tables

    def find_aligned_text(self, blocks: List[Dict]) -> List[List[Dict]]:
        """Encontra texto alinhado que pode formar tabela"""
        groups = []

        y_tolerance = 5
        blocks_by_y = {}

        for block in blocks:
            bbox = block.get('bbox', [0, 0, 0, 0])
            y = round(bbox[1] / y_tolerance) * y_tolerance

            if y not in blocks_by_y:
                blocks_by_y[y] = []
            blocks_by_y[y].append(block)

        for y, line_blocks in blocks_by_y.items():
            if len(line_blocks) >= 3:
                groups.append(sorted(line_blocks, key=lambda b: b['bbox'][0]))

        return groups

    def parse_aligned_table(self, blocks: List[Dict]) -> Dict:
        """Parse tabela alinhada"""
        rows = []
        current_row = []
        current_y = None

        for block in blocks:
            bbox = block.get('bbox', [0, 0, 0, 0])
            y = bbox[1]

            if current_y is None or abs(y - current_y) < 5:
                current_row.append(self.extract_text_from_block(block))
                current_y = y
            else:
                if current_row:
                    rows.append(current_row)
                current_row = [self.extract_text_from_block(block)]
                current_y = y

        if current_row:
            rows.append(current_row)

        headers = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else []

        return {'headers': headers, 'rows': data_rows}

    def detect_cards(self, blocks: List[Dict]) -> List[Dict]:
        """Detecta cards ou caixas de informação"""
        cards = []

        for block in blocks:
            if block.get('type') != 0:
                continue

            text = self.extract_text_from_block(block)

            if self.is_card_content(text):
                bbox = block.get('bbox', [0, 0, 0, 0])
                cards.append({
                    'type': 'info_card',
                    'content': text,
                    'bbox': bbox,
                    'style': self.detect_card_style(text)
                })

        return cards

    def is_card_content(self, text: str) -> bool:
        """Verifica se texto parece conteúdo de card"""
        card_indicators = [
            text.startswith('•'),
            text.startswith('-'),
            text.startswith('→'),
            text.startswith('▪'),
            ':' in text and len(text.split('\n')) <= 5,
            re.search(r'^[A-Z][^.!?]*:', text)
        ]

        return any(card_indicators)

    def detect_card_style(self, text: str) -> str:
        """Detecta estilo do card"""
        if 'nota' in text.lower() or 'importante' in text.lower():
            return 'warning'
        elif 'atenção' in text.lower() or 'cuidado' in text.lower():
            return 'alert'
        elif 'sucesso' in text.lower() or 'correto' in text.lower():
            return 'success'
        else:
            return 'info'

    def detect_diagrams(self, page: fitz.Page, blocks: List[Dict]) -> List[Dict]:
        """Detecta diagramas e imagens"""
        diagrams = []

        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            bbox = page.get_image_bbox(img[7])

            diagrams.append({
                'type': 'image',
                'xref': xref,
                'bbox': (bbox.x0, bbox.y0, bbox.x1, bbox.y1),
                'index': img_index
            })

        text = page.get_text().lower()
        for keyword in self.diagram_keywords:
            if keyword in text:
                diagrams.append({
                    'type': 'referenced_diagram',
                    'keyword': keyword
                })

        return diagrams

    def detect_lists(self, blocks: List[Dict]) -> List[Dict]:
        """Detecta listas"""
        lists = []
        current_list = []

        list_markers = ['•', '-', '→', '▪', '◦', '∙']

        for block in blocks:
            if block.get('type') != 0:
                continue

            text = self.extract_text_from_block(block)
            lines = text.split('\n')

            for line in lines:
                line_stripped = line.strip()

                if any(line_stripped.startswith(marker) for marker in list_markers):
                    current_list.append({
                        'text': line_stripped,
                        'marker': line_stripped[0]
                    })
                elif current_list and len(current_list) >= 2:
                    lists.append({
                        'type': 'bulleted_list',
                        'items': current_list.copy()
                    })
                    current_list = []

        if current_list and len(current_list) >= 2:
            lists.append({
                'type': 'bulleted_list',
                'items': current_list.copy()
            })

        return lists

    def detect_headers(self, blocks: List[Dict]) -> List[Dict]:
        """Detecta cabeçalhos e títulos"""
        headers = []

        for block in blocks:
            if block.get('type') != 0:
                continue

            text = self.extract_text_from_block(block)

            if self.is_header(text, block):
                level = self.detect_header_level(text, block)
                headers.append({
                    'type': 'header',
                    'text': text,
                    'level': level,
                    'bbox': block.get('bbox', [0, 0, 0, 0])
                })

        return headers

    def is_header(self, text: str, block: Dict) -> bool:
        """Verifica se é cabeçalho"""
        if not text or len(text) > 200:
            return False

        lines = block.get('lines', [])
        if not lines:
            return False

        first_span = lines[0].get('spans', [{}])[0]
        font_size = first_span.get('size', 0)
        font_flags = first_span.get('flags', 0)

        is_bold = bool(font_flags & 2**4)
        is_large = font_size > 14
        is_short = len(text) < 100
        is_uppercase = text.isupper()

        return (is_bold and is_short) or (is_large and is_short) or is_uppercase

    def detect_header_level(self, text: str, block: Dict) -> int:
        """Detecta nível do cabeçalho (h1, h2, h3...)"""
        lines = block.get('lines', [])
        if not lines:
            return 3

        first_span = lines[0].get('spans', [{}])[0]
        font_size = first_span.get('size', 12)

        if font_size >= 24:
            return 1
        elif font_size >= 18:
            return 2
        elif font_size >= 14:
            return 3
        else:
            return 4

    def detect_text_blocks(self, blocks: List[Dict]) -> List[Dict]:
        """Detecta blocos de texto normal"""
        text_blocks = []

        for block in blocks:
            if block.get('type') != 0:
                continue

            text = self.extract_text_from_block(block)

            if len(text.strip()) > 20 and not self.is_header(text, block):
                text_blocks.append({
                    'type': 'text',
                    'content': text,
                    'bbox': block.get('bbox', [0, 0, 0, 0])
                })

        return text_blocks

    def classify_layout(self, blocks: List[Dict]) -> str:
        """Classifica tipo geral de layout da página"""
        text_blocks = [b for b in blocks if b.get('type') == 0]

        if not text_blocks:
            return 'empty'

        avg_width = sum(b['bbox'][2] - b['bbox'][0] for b in text_blocks) / len(text_blocks)

        page_width = 595

        if avg_width < page_width * 0.4:
            return 'multi_column'
        elif len(text_blocks) <= 3:
            return 'sparse'
        else:
            return 'standard'

    def extract_text_from_block(self, block: Dict) -> str:
        """Extrai texto de um bloco preservando formatação"""
        text_parts = []

        for line in block.get('lines', []):
            line_text = []
            for span in line.get('spans', []):
                line_text.append(span.get('text', ''))
            text_parts.append(''.join(line_text))

        return '\n'.join(text_parts)
