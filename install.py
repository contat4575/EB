"""
Script de Instalação Automatizada
PDF Converter Pro 2.0
"""

import subprocess
import sys
import platform
from pathlib import Path


def print_banner():
    """Banner de boas-vindas"""
    print("=" * 70)
    print("  🧠 PDF to HTML Converter Pro 2.0 - Instalação")
    print("=" * 70)
    print()


def check_python_version():
    """Verifica versão do Python"""
    print("🔍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True


def check_pip():
    """Verifica se pip está instalado"""
    print("\n🔍 Verificando pip...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip não encontrado!")
        return False


def create_venv():
    """Cria ambiente virtual"""
    print("\n🔨 Criando ambiente virtual...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        response = input("   Ambiente virtual já existe. Recriar? (s/N): ")
        if response.lower() != 's':
            print("   Usando ambiente existente.")
            return True
        
        print("   Removendo ambiente antigo...")
        import shutil
        shutil.rmtree(venv_path)
    
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            check=True
        )
        print("✓ Ambiente virtual criado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False


def get_pip_command():
    """Retorna comando pip baseado no sistema operacional"""
    if platform.system() == "Windows":
        return str(Path("venv/Scripts/pip.exe"))
    else:
        return str(Path("venv/bin/pip"))


def install_requirements():
    """Instala dependências"""
    print("\n📦 Instalando dependências...")
    print("   (Isso pode levar alguns minutos)")
    
    pip_cmd = get_pip_command()
    
    # Atualizar pip
    print("\n   Atualizando pip...")
    try:
        subprocess.run(
            [pip_cmd, "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        print("   ✓ pip atualizado")
    except subprocess.CalledProcessError:
        print("   ⚠️ Não foi possível atualizar pip, continuando...")
    
    # Instalar dependências essenciais
    essential = [
        "PyMuPDF==1.23.8",
        "pillow",
        "pandas",
        "numpy"
    ]
    
    print("\n   Instalando pacotes essenciais...")
    for package in essential:
        try:
            print(f"     - {package.split('==')[0]}...", end=" ")
            subprocess.run(
                [pip_cmd, "install", package],
                check=True,
                capture_output=True
            )
            print("✓")
        except subprocess.CalledProcessError as e:
            print("❌")
            print(f"      Erro: {e}")
    
    # Instalar pacotes opcionais
    optional = [
        ("camelot-py[cv]", "Camelot (tabelas avançadas)"),
        ("pdfplumber", "PDFPlumber (tabelas simples)"),
        ("opencv-python", "OpenCV (processamento de imagem)")
    ]
    
    print("\n   Instalando pacotes opcionais...")
    for package, description in optional:
        try:
            print(f"     - {description}...", end=" ")
            subprocess.run(
                [pip_cmd, "install", package],
                check=True,
                capture_output=True,
                timeout=300  # 5 minutos timeout
            )
            print("✓")
        except subprocess.CalledProcessError:
            print("⚠️ (falhou, mas não é crítico)")
        except subprocess.TimeoutExpired:
            print("⚠️ (timeout, mas não é crítico)")
    
    print("\n✓ Instalação de dependências concluída")
    return True


def check_system_dependencies():
    """Verifica dependências do sistema"""
    print("\n🔍 Verificando dependências do sistema...")
    
    system = platform.system()
    
    if system == "Linux":
        print("   Linux detectado. Verificando pacotes...")
        
        # Verificar ghostscript
        try:
            subprocess.run(
                ["which", "gs"],
                capture_output=True,
                check=True
            )
            print("   ✓ Ghostscript instalado")
        except subprocess.CalledProcessError:
            print("   ⚠️ Ghostscript não encontrado")
            print("      Instale com: sudo apt-get install ghostscript")
        
        # Verificar tkinter
        try:
            import tkinter
            print("   ✓ Tkinter disponível")
        except ImportError:
            print("   ⚠️ Tkinter não encontrado")
            print("      Instale com: sudo apt-get install python3-tk")
    
    elif system == "Windows":
        print("   Windows detectado.")
        print("   ℹ️ Para melhor suporte a tabelas, instale Ghostscript:")
        print("      https://ghostscript.com/releases/gsdnld.html")
    
    elif system == "Darwin":  # macOS
        print("   macOS detectado.")
        print("   ℹ️ Para melhor suporte a tabelas, instale Ghostscript:")
        print("      brew install ghostscript")


def create_desktop_shortcut():
    """Cria atalho na área de trabalho"""
    response = input("\n🔗 Criar atalho na área de trabalho? (s/N): ")
    
    if response.lower() != 's':
        return
    
    system = platform.system()
    
    if system == "Windows":
        try:
            import win32com.client
            
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "PDF Converter Pro.lnk"
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.TargetPath = str(Path.cwd() / "venv/Scripts/python.exe")
            shortcut.Arguments = str(Path.cwd() / "main.py")
            shortcut.WorkingDirectory = str(Path.cwd())
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print(f"✓ Atalho criado: {shortcut_path}")
        except ImportError:
            print("⚠️ pywin32 não instalado. Atalho não criado.")
        except Exception as e:
            print(f"⚠️ Erro ao criar atalho: {e}")
    
    else:
        print("ℹ️ Criação de atalho disponível apenas no Windows")


def test_installation():
    """Testa a instalação"""
    print("\n🧪 Testando instalação...")
    
    try:
        # Testar imports essenciais
        print("   Testando PyMuPDF...", end=" ")
        import fitz
        print("✓")
        
        print("   Testando Tkinter...", end=" ")
        import tkinter
        print("✓")
        
        print("   Testando Pandas...", end=" ")
        import pandas
        print("✓")
        
        # Testar imports opcionais
        try:
            print("   Testando Camelot...", end=" ")
            import camelot
            print("✓")
        except ImportError:
            print("⚠️ (opcional)")
        
        try:
            print("   Testando PDFPlumber...", end=" ")
            import pdfplumber
            print("✓")
        except ImportError:
            print("⚠️ (opcional)")
        
        print("\n✓ Instalação testada com sucesso!")
        return True
    
    except ImportError as e:
        print(f"\n❌ Erro no teste: {e}")
        return False


def print_next_steps():
    """Imprime próximos passos"""
    system = platform.system()
    
    print("\n" + "=" * 70)
    print("  ✅ INSTALAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print("\n📝 Próximos passos:")
    print("\n1. Ativar ambiente virtual:")
    
    if system == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Executar aplicação:")
    print("   python main.py")
    
    print("\n3. Para desativar ambiente virtual:")
    print("   deactivate")
    
    print("\n💡 Dica: Execute 'python main.py' sempre de dentro do ambiente virtual")
    print()


def main():
    """Função principal"""
    print_banner()
    
    # Verificações
    if not check_python_version():
        input("\nPressione ENTER para sair...")
        return
    
    if not check_pip():
        input("\nPressione ENTER para sair...")
        return
    
    # Criar ambiente virtual
    if not create_venv():
        input("\nPressione ENTER para sair...")
        return
    
    # Instalar dependências
    if not install_requirements():
        input("\nPressione ENTER para sair...")
        return
    
    # Verificar sistema
    check_system_dependencies()
    
    # Testar instalação
    # test_installation()  # Desabilitado pois precisa do venv ativado
    
    # Criar atalho
    create_desktop_shortcut()
    
    # Próximos passos
    print_next_steps()
    
    input("Pressione ENTER para sair...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para sair...")
