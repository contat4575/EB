"""
PDF to HTML Converter - Sistema Robusto
Versão: 2.0
Autor: Sistema Avançado de Conversão

INSTALAÇÃO:
pip install PyMuPDF camelot-py[cv] pdfplumber opencv-python pandas pillow tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
import json
from datetime import datetime

# Importar módulos do sistema
from pdf_extractor import PDFExtractor
from html_generator import HTMLGenerator
from config_manager import ConfigManager


class PDFConverterApp:
    """Aplicação principal com interface gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to HTML Converter Pro 2.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configurações
        self.config = ConfigManager()
        self.pdf_file = None
        self.output_file = None
        self.is_processing = False
        
        self.setup_ui()
        self.load_saved_settings()
        
    def setup_ui(self):
        """Configura interface do usuário"""
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'))
        style.configure('Action.TButton', font=('Segoe UI', 10, 'bold'))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title = ttk.Label(
            main_frame, 
            text="🧠 PDF to HTML Converter Pro", 
            style='Title.TLabel'
        )
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seleção de arquivo
        file_frame = ttk.LabelFrame(main_frame, text="Arquivo PDF", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.file_label = ttk.Label(file_frame, text="Nenhum arquivo selecionado")
        self.file_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        ttk.Button(
            file_frame, 
            text="Selecionar PDF", 
            command=self.select_pdf,
            style='Action.TButton'
        ).grid(row=0, column=1, padx=5)
        
        # Opções de extração
        extraction_frame = ttk.LabelFrame(
            main_frame, 
            text="Método de Extração", 
            padding="10"
        )
        extraction_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.extraction_method = tk.StringVar(value="auto")
        
        methods = [
            ("Auto (Recomendado)", "auto"),
            ("Camelot (Tabelas complexas)", "camelot"),
            ("PDFPlumber (Tabelas simples)", "pdfplumber"),
            ("PyMuPDF (Texto puro)", "pymupdf")
        ]
        
        for i, (text, value) in enumerate(methods):
            ttk.Radiobutton(
                extraction_frame,
                text=text,
                variable=self.extraction_method,
                value=value
            ).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Opções de design
        design_frame = ttk.LabelFrame(main_frame, text="Design HTML", padding="10")
        design_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.design_theme = tk.StringVar(value="premium")
        
        themes = [
            ("Premium Dark (Padrão)", "premium"),
            ("Medical Clean", "medical"),
            ("Modern Gradient", "modern"),
            ("Classic Professional", "classic")
        ]
        
        for i, (text, value) in enumerate(themes):
            ttk.Radiobutton(
                design_frame,
                text=text,
                variable=self.design_theme,
                value=value
            ).grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=2)
        
        # Opções adicionais
        options_frame = ttk.LabelFrame(main_frame, text="Opções", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.include_toc = tk.BooleanVar(value=True)
        self.responsive_design = tk.BooleanVar(value=True)
        self.animations = tk.BooleanVar(value=True)
        self.dark_mode = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(
            options_frame, 
            text="Incluir índice navegável", 
            variable=self.include_toc
        ).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        ttk.Checkbutton(
            options_frame, 
            text="Design responsivo (mobile)", 
            variable=self.responsive_design
        ).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Checkbutton(
            options_frame, 
            text="Animações e transições", 
            variable=self.animations
        ).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        ttk.Checkbutton(
            options_frame, 
            text="Modo escuro", 
            variable=self.dark_mode
        ).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=400
        )
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Status
        self.status_label = ttk.Label(
            main_frame, 
            text="Aguardando arquivo...", 
            foreground="gray"
        )
        self.status_label.grid(row=6, column=0, columnspan=3)
        
        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        self.convert_btn = ttk.Button(
            button_frame,
            text="🚀 Converter",
            command=self.start_conversion,
            style='Action.TButton',
            state='disabled'
        )
        self.convert_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(
            button_frame,
            text="💾 Salvar Configurações",
            command=self.save_settings
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            button_frame,
            text="📂 Abrir Última Conversão",
            command=self.open_last_conversion
        ).grid(row=0, column=2, padx=5)
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, width=80, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar grid weights para responsividade
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def log(self, message, level="info"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        color_map = {
            "info": "black",
            "success": "green",
            "warning": "orange",
            "error": "red"
        }
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
        # Atualizar status
        self.status_label.config(text=message, foreground=color_map.get(level, "black"))
        self.root.update()
    
    def select_pdf(self):
        """Seleciona arquivo PDF"""
        filename = filedialog.askopenfilename(
            title="Selecionar PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            self.pdf_file = Path(filename)
            self.file_label.config(text=self.pdf_file.name)
            self.convert_btn.config(state='normal')
            self.log(f"Arquivo selecionado: {self.pdf_file.name}", "success")
    
    def start_conversion(self):
        """Inicia conversão em thread separada"""
        if self.is_processing:
            messagebox.showwarning("Aviso", "Uma conversão já está em andamento!")
            return
        
        if not self.pdf_file:
            messagebox.showerror("Erro", "Selecione um arquivo PDF primeiro!")
            return
        
        self.is_processing = True
        self.convert_btn.config(state='disabled')
        self.progress.start(10)
        
        # Thread para não travar a UI
        thread = threading.Thread(target=self.convert_pdf)
        thread.daemon = True
        thread.start()
    
    def convert_pdf(self):
        """Realiza conversão do PDF"""
        try:
            self.log("Iniciando conversão...", "info")
            
            # Configurar extrator
            extractor = PDFExtractor(
                method=self.extraction_method.get(),
                log_callback=self.log
            )
            
            # Extrair dados
            self.log(f"Extraindo dados usando método: {self.extraction_method.get()}", "info")
            pages_data = extractor.extract(self.pdf_file)
            
            if not pages_data:
                raise Exception("Nenhum dado extraído do PDF")
            
            self.log(f"✓ {len(pages_data)} páginas extraídas com sucesso", "success")
            
            # Gerar HTML
            self.log("Gerando HTML...", "info")
            generator = HTMLGenerator(
                theme=self.design_theme.get(),
                include_toc=self.include_toc.get(),
                responsive=self.responsive_design.get(),
                animations=self.animations.get(),
                dark_mode=self.dark_mode.get()
            )
            
            html_content = generator.generate(pages_data)
            
            # Salvar arquivo
            output_path = self.pdf_file.parent / f"{self.pdf_file.stem}_converted.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.output_file = output_path
            
            # Salvar no histórico
            self.config.save_to_history({
                'input': str(self.pdf_file),
                'output': str(output_path),
                'timestamp': datetime.now().isoformat(),
                'method': self.extraction_method.get(),
                'theme': self.design_theme.get()
            })
            
            self.log(f"✓ Conversão concluída: {output_path.name}", "success")
            
            # Mostrar resultado
            self.root.after(0, lambda: self.show_completion_dialog(output_path))
            
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}", "error")
            # Corrigido: captura 'e' como argumento da lambda
            self.root.after(0, lambda error=e: messagebox.showerror("Erro", f"Falha na conversão:\n{str(error)}"))
        
        finally:
            self.is_processing = False
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.convert_btn.config(state='normal'))
    
    def show_completion_dialog(self, output_path):
        """Mostra diálogo de conclusão"""
        result = messagebox.askquestion(
            "Sucesso!",
            f"Conversão concluída com sucesso!\n\n"
            f"Arquivo: {output_path.name}\n\n"
            f"Deseja abrir o arquivo agora?",
            icon='info'
        )
        
        if result == 'yes':
            import webbrowser
            webbrowser.open(str(output_path))
    
    def save_settings(self):
        """Salva configurações atuais"""
        settings = {
            'extraction_method': self.extraction_method.get(),
            'design_theme': self.design_theme.get(),
            'include_toc': self.include_toc.get(),
            'responsive_design': self.responsive_design.get(),
            'animations': self.animations.get(),
            'dark_mode': self.dark_mode.get()
        }
        
        self.config.save_settings(settings)
        self.log("Configurações salvas", "success")
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
    
    def load_saved_settings(self):
        """Carrega configurações salvas"""
        settings = self.config.load_settings()
        
        if settings:
            self.extraction_method.set(settings.get('extraction_method', 'auto'))
            self.design_theme.set(settings.get('design_theme', 'premium'))
            self.include_toc.set(settings.get('include_toc', True))
            self.responsive_design.set(settings.get('responsive_design', True))
            self.animations.set(settings.get('animations', True))
            self.dark_mode.set(settings.get('dark_mode', True))
            
            self.log("Configurações anteriores carregadas", "info")
    
    def open_last_conversion(self):
        """Abre última conversão realizada"""
        history = self.config.get_history()
        
        if not history:
            messagebox.showinfo("Info", "Nenhuma conversão anterior encontrada")
            return
        
        last = history[-1]
        output_path = Path(last['output'])
        
        if output_path.exists():
            import webbrowser
            webbrowser.open(str(output_path))
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado")


def main():
    """Função principal"""
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()