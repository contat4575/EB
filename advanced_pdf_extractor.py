"""
Extrator Avançado de PDF
Integra detecção de estruturas complexas
"""

import fitz
from pathlib import Path
from typing import List, Dict, Callable, Optional
from structure_detector import StructureDetector


class AdvancedPDFExtractor:
    """Extrator de PDF com reconhecimento avançado de estruturas"""

    def __init__(self, log_callback: Optional[Callable] = None):
        self.log = log_callback or print
        self.detector = StructureDetector()

    def extract(self, pdf_path: Path) -> List[Dict]:
        """Extrai dados completos do PDF"""
        self.log("Iniciando extração avançada...", "info")

        doc = fitz.open(pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            self.log(f"Analisando página {page_num + 1}/{len(doc)}...", "info")

            structures = self.detector.analyze_page(page)

            page_data = {
                'page': page_num + 1,
                'text': page.get_text(),
                'structures': structures,
                'metadata': {
                    'width': page.rect.width,
                    'height': page.rect.height,
                    'rotation': page.rotation
                }
            }

            pages.append(page_data)

        doc.close()

        self.log(f"✓ Extração completa: {len(pages)} páginas", "success")

        return pages

    def extract_with_images(self, pdf_path: Path, output_dir: Path) -> List[Dict]:
        """Extrai PDF incluindo extração de imagens"""
        output_dir.mkdir(exist_ok=True)

        doc = fitz.open(pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            structures = self.detector.analyze_page(page)

            image_paths = self.extract_page_images(page, page_num, output_dir)

            page_data = {
                'page': page_num + 1,
                'text': page.get_text(),
                'structures': structures,
                'images': image_paths,
                'metadata': {
                    'width': page.rect.width,
                    'height': page.rect.height,
                    'rotation': page.rotation
                }
            }

            pages.append(page_data)

        doc.close()

        return pages

    def extract_page_images(self, page: fitz.Page, page_num: int,
                           output_dir: Path) -> List[str]:
        """Extrai imagens de uma página"""
        image_paths = []
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]

            try:
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                image_path = output_dir / image_filename

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                image_paths.append(image_filename)

            except Exception as e:
                self.log(f"Erro ao extrair imagem {img_index}: {e}", "warning")

        return image_paths

    def analyze_document_structure(self, pdf_path: Path) -> Dict:
        """Analisa estrutura geral do documento"""
        doc = fitz.open(pdf_path)

        analysis = {
            'total_pages': len(doc),
            'has_tables': False,
            'has_images': False,
            'has_diagrams': False,
            'layout_types': [],
            'sections': []
        }

        for page_num in range(len(doc)):
            page = doc[page_num]
            structures = self.detector.analyze_page(page)

            if structures['tables']:
                analysis['has_tables'] = True

            if structures['diagrams']:
                analysis['has_images'] = True
                analysis['has_diagrams'] = True

            layout_type = structures['layout_type']
            if layout_type not in analysis['layout_types']:
                analysis['layout_types'].append(layout_type)

            for header in structures['headers']:
                if header['level'] <= 2:
                    analysis['sections'].append({
                        'page': page_num + 1,
                        'title': header['text'],
                        'level': header['level']
                    })

        doc.close()

        return analysis
