"""
Script de Conversão Simples
Converte PDF para HTML usando o sistema avançado
"""

import sys
from pathlib import Path
from advanced_pdf_extractor import AdvancedPDFExtractor
from advanced_html_generator import AdvancedHTMLGenerator


def convert_pdf_to_html(pdf_path: str, output_path: str = None):
    """
    Converte PDF para HTML com design perfeito

    Args:
        pdf_path: Caminho para o arquivo PDF
        output_path: Caminho de saída (opcional)
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"❌ Erro: Arquivo não encontrado: {pdf_path}")
        return False

    if output_path is None:
        output_path = pdf_file.parent / f"{pdf_file.stem}_converted.html"
    else:
        output_path = Path(output_path)

    print("🚀 Iniciando conversão avançada de PDF para HTML...")
    print(f"📄 Arquivo: {pdf_file.name}")
    print()

    try:
        extractor = AdvancedPDFExtractor(log_callback=lambda msg, level='info': print(f"  {msg}"))

        pages_data = extractor.extract(pdf_file)

        if not pages_data:
            print("❌ Nenhum dado extraído do PDF")
            return False

        print()
        print("🎨 Gerando HTML com design premium...")

        generator = AdvancedHTMLGenerator(
            theme="premium",
            responsive=True,
            animations=True
        )

        html_content = generator.generate(pages_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print()
        print(f"✅ Conversão concluída com sucesso!")
        print(f"📁 Arquivo salvo: {output_path}")
        print()
        print(f"Para visualizar, abra: {output_path.absolute()}")

        return True

    except Exception as e:
        print(f"❌ Erro durante a conversão: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""

    if len(sys.argv) < 2:
        print("Uso: python convert_pdf.py <arquivo.pdf> [saida.html]")
        print()
        print("Exemplo:")
        print("  python convert_pdf.py documento.pdf")
        print("  python convert_pdf.py documento.pdf meu_documento.html")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    success = convert_pdf_to_html(pdf_path, output_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
