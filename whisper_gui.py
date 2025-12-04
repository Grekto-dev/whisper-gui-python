import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import shutil
import os
import sys
import re
import threading
import datetime
import json
import time
import importlib
import webbrowser

TEXTS = {
    "en_us": {
        "app_title": "Whisper GUI Launcher",
        "dep": {
            "title": "Missing Dependencies",
            "msg_start": "The following dependencies are missing for full functionality:\n\n",
            "msg_end": "\nDo you want to download and install them now?\nThe program will automatically restart after completion.",
            "installing_title": "Installing...",
            "installing_lbl": "Installing packages via pip...\nThis may take a few minutes.",
            "error_title": "Error",
            "error_msg": "Failed to install package: {pkg}.\nCheck your connection or try manual installation.",
            "success_title": "Success",
            "success_msg": "Dependencies installed successfully!\nThe program will restart.",
            "warning_title": "Warning",
            "warning_msg": "The program may not work correctly without dependencies."
        },
        "status": {
            "system": "System Status",
            "whisper_installed": "Installed",
            "whisper_not_found": "NOT FOUND (Install: pip install -U openai-whisper)",
            "pytorch_cuda": "PyTorch with CUDA (GPU: {gpu})",
            "pytorch_cpu": "PyTorch detected (CPU Only)",
            "pytorch_not_found": "PyTorch not detected"
        },
        "ui": {
            "reset": "Reset All",
            "start": "START TRANSCRIPTION",
            "processing": "PROCESSING...",
            "save_profile": "Save Profile",
            "load_profile": "Load Profile",
            "tab_general": "General",
            "tab_advanced": "Advanced",
            "tab_help": "Help",
            "monitor": "Resource Monitor",
            "terminal": "Terminal Log (Events)",
            "files_queue": "File Queue",
            "dnd_text": "Click to add files",
            "dnd_drag": " or Drag here",
            "clear": "Clear",
            "config": "Settings",
            "model": "Model:",
            "models_cache": "Cached Models:",
            "no_models": "No models in cache.",
            "language": "Language:",
            "auto_detect": "Auto (detect)",
            "output_fmt": "Output format:",
            "device": "Device:",
            "output_dir": "Output Directory",
            "custom_dir": "Custom directory",
            "custom_dir_tip": "Default: Output saved in input file's directory.\nIf multiple files from different locations are selected,\neach output stays with its source file.",
            "file_tip": "Supported formats:\nflac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav, webm",
            "app_lang": "App Language",
            "columns": {"file": "File", "status": "Status"},
            "waiting": "Waiting",
            "success_state": "Done ✅",
            "error_state": "Error ❌",
            "critical_state": "Critical Error ⚠️",
            "processing_state": "Processing...",
            "sobrescrever": "Overwrite",
            "info": "Information"
        },
        "help": {
            "about_section": "About",
            "desc": "Graphical Interface for OpenAI Whisper\nVersion 1.0.0",
            "dev_label": "Developed by:",
            "dev_info": "Pedro Nogueira\nEmail: pedrohcnogueira.dev@gmail.com",
            "credits_section": "Credits & License",
            "credits": "Transcription Engine: OpenAI Whisper (MIT License)\nThis application is just a facilitator interface.",
            "help_section": "Help & Documentation",
            "disclaimer": "This software is a graphical bridge (GUI) for the Whisper engine.\nQuestions about advanced parameters, model accuracy, or internal engine errors should be consulted directly in the official OpenAI documentation.",
            "link_label": "Access Official Repository (GitHub)",
            "link_url": "https://github.com/openai/whisper"
        },
        "msgs": {
            "overwrite": "A profile already exists. Do you want to overwrite it?",
            "profile_saved_title": "Success",
            "profile_saved": "Profile saved!",
            "profile_loaded_title": "Success",
            "profile_loaded": "Profile loaded!",
            "no_profile": "No profile found.",
            "select_files": "Select files",
            "files_added": "{count} files added to queue.",
            "list_cleared": "File list cleared.",
            "config_reset": "Settings reset.",
            "start_batch": "--- STARTING BATCH PROCESSING ---",
            "file_progress": "File {current}/{total}: {name}",
            "status_success": "Status: SUCCESS",
            "status_error": "Status: ERROR (Code {code})",
            "status_critical": "Critical Exception: {error}",
            "end_batch": "--- PROCESSING FINISHED ---",
            "finished_popup": "Queue processing finished.",
            "finished_title": "Finished",
            "install_psutil": "Install psutil",
            "empty_list": "The file list is empty.",
            "attention": "Attention",
            "whisper_404": "Whisper not found.",
            "error_save": "Error saving profile: {error}",
            "error_load": "Error loading profile: {error}",
            "profile_saved_log": "Profile saved: {file}",
            "profile_loaded_log": "Profile loaded.",
            "restart_title": "Restart Required",
            "restart_confirm": "Language changed. Restart now to apply?"
        },
        "advanced": {
            "model_dir": "The path to save model files; uses ~/.cache/whisper by default. (default: None)",
            "verbose": "Whether to print out the progress and debug messages. (default: True)",
            "task": "Whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate'). (default: transcribe)",
            "temperature": "Temperature to use for sampling. (default: 0)",
            "best_of": "Number of candidates when sampling with non-zero temperature. (default: 5)",
            "beam_size": "Number of beams in beam search, only applicable when temperature is zero. (default: 5)",
            "patience": "Optional patience value to use in beam decoding. (default: None)",
            "length_penalty": "Optional token length penalty coefficient (alpha). (default: None)",
            "suppress_tokens": "Comma-separated list of token ids to suppress during sampling; '-1' will suppress most special characters. (default: -1)",
            "initial_prompt": "Optional text to provide as a prompt for the first window. (default: None)",
            "carry_initial_prompt": "If True, prepend initial_prompt to every internal decode() call. May reduce the effectiveness of condition_on_previous_text. (default: False)",
            "condition_on_previous_text": "If True, provide the previous output of the model as a prompt for the next window. (default: True)",
            "fp16": "Whether to perform inference in fp16. (default: True)",
            "temperature_increment_on_fallback": "Temperature to increase when falling back when the decoding fails to meet either of the thresholds below. (default: 0.2)",
            "compression_ratio_threshold": "If the gzip compression ratio is higher than this value, treat the decoding as failed. (default: 2.4)",
            "logprob_threshold": "If the average log probability is lower than this value, treat the decoding as failed. (default: -1.0)",
            "no_speech_threshold": "If the probability of the <|nospeech|> token is higher than this value AND the decoding has failed, consider the segment as silence. (default: 0.6)",
            "word_timestamps": "(Experimental) Extract word-level timestamps and refine the results based on them. (default: False)",
            "prepend_punctuations": "If word_timestamps is True, merge these punctuation symbols with the next word. (default: \"'“¿([{-)\")",
            "append_punctuations": "If word_timestamps is True, merge these punctuation symbols with the previous word. (default: \"'.。,，!！?？:：”)]}、)\")",
            "highlight_words": "(Requires word_timestamps True) Underline each word as it is spoken in srt and vtt. (default: False)",
            "max_line_width": "(Requires word_timestamps True) The maximum number of characters in a line before breaking the line. (default: None)",
            "max_line_count": "(Requires word_timestamps True) The maximum number of lines in a segment. (default: None)",
            "max_words_per_line": "(Requires word_timestamps True) The maximum number of words in a segment. (default: None)",
            "threads": "Number of threads used by torch for CPU inference. (default: 0)",
            "clip_timestamps": "Comma-separated list start,end,... timestamps (in seconds) of clips to process. (default: 0)",
            "hallucination_silence_threshold": "(Requires word_timestamps True) Skip silent periods longer than this threshold (in seconds) when a possible hallucination is detected. (default: None)"
        }
    },
    "pt_br": {
        "app_title": "Whisper GUI Launcher",
        "dep": {
            "title": "Dependências Faltando",
            "msg_start": "As seguintes dependências estão faltando para o funcionamento completo:\n\n",
            "msg_end": "\nDeseja baixá-las e instalá-las agora?\nO programa será reiniciado automaticamente após a conclusão.",
            "installing_title": "Instalando...",
            "installing_lbl": "Instalando pacotes via pip...\nIsso pode demorar alguns minutos.",
            "error_title": "Erro",
            "error_msg": "Falha ao instalar o pacote: {pkg}.\nVerifique sua conexão ou tente instalar manualmente.",
            "success_title": "Sucesso",
            "success_msg": "Dependências instaladas com sucesso!\nO programa será reiniciado.",
            "warning_title": "Aviso",
            "warning_msg": "O programa pode não funcionar corretamente sem as dependências."
        },
        "status": {
            "system": "Status do Sistema",
            "whisper_installed": "Instalado",
            "whisper_not_found": "NÃO ENCONTRADO (Instale: pip install -U openai-whisper)",
            "pytorch_cuda": "PyTorch com CUDA (GPU: {gpu})",
            "pytorch_cpu": "PyTorch detectado (Apenas CPU)",
            "pytorch_not_found": "PyTorch não detectado"
        },
        "ui": {
            "reset": "Resetar Tudo",
            "start": "INICIAR TRANSCRIÇÃO",
            "processing": "PROCESSANDO...",
            "save_profile": "Salvar Perfil",
            "load_profile": "Carregar Perfil",
            "tab_general": "Geral",
            "tab_advanced": "Avançado",
            "tab_help": "Ajuda",
            "monitor": "Monitor de Recursos",
            "terminal": "Terminal Log (Eventos)",
            "files_queue": "Fila de Arquivos",
            "dnd_text": "Clique para adicionar arquivos",
            "dnd_drag": " ou Arraste aqui",
            "clear": "Limpar",
            "config": "Configurações",
            "model": "Modelo:",
            "models_cache": "Modelos no Cache:",
            "no_models": "Nenhum modelo no cache.",
            "language": "Idioma:",
            "auto_detect": "Auto (detectar)",
            "output_fmt": "Formato de saída:",
            "device": "Dispositivo:",
            "output_dir": "Diretório de Saída",
            "custom_dir": "Diretório personalizado",
            "custom_dir_tip": "Padrão: Output salvo no diretório do input.\nPara múltiplos arquivos de locais distintos,\ncada output fica com sua origem.",
            "file_tip": "Formatos suportados:\nflac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav, webm",
            "app_lang": "Idioma do App",
            "columns": {"file": "Arquivo", "status": "Status"},
            "waiting": "Aguardando",
            "success_state": "Concluído ✅",
            "error_state": "Erro ❌",
            "critical_state": "Erro Crítico ⚠️",
            "processing_state": "Processando...",
            "sobrescrever": "Sobrescrever",
            "info": "Informação"
        },
        "help": {
            "about_section": "Sobre",
            "desc": "Interface Gráfica para OpenAI Whisper\nVersão 1.0.0",
            "dev_label": "Desenvolvido por:",
            "dev_info": "Pedro Nogueira\nEmail: pedrohcnogueira.dev@gmail.com",
            "credits_section": "Créditos e Licença",
            "credits": "Motor de Transcrição: OpenAI Whisper (Licença MIT)\nEsta aplicação é apenas uma interface facilitadora.",
            "help_section": "Ajuda e Documentação",
            "disclaimer": "Este software é uma ponte gráfica (GUI) para o motor Whisper.\nDúvidas sobre parâmetros avançados, precisão do modelo ou erros internos do motor devem ser consultadas diretamente na documentação oficial da OpenAI.",
            "link_label": "Acessar Repositório Oficial (GitHub)",
            "link_url": "https://github.com/openai/whisper"
        },
        "msgs": {
            "overwrite": "Já existe um perfil salvo. Deseja sobrescrevê-lo?",
            "profile_saved_title": "Sucesso",
            "profile_saved": "Perfil salvo!",
            "profile_loaded_title": "Sucesso",
            "profile_loaded": "Perfil carregado!",
            "no_profile": "Nenhum perfil encontrado.",
            "select_files": "Selecione arquivos",
            "files_added": "{count} arquivos adicionados à fila.",
            "list_cleared": "Lista de arquivos limpa.",
            "config_reset": "Configurações resetadas.",
            "start_batch": "--- INICIANDO PROCESSAMENTO DE LOTE ---",
            "file_progress": "Arquivo {current}/{total}: {name}",
            "status_success": "Status: SUCESSO",
            "status_error": "Status: ERRO (Código {code})",
            "status_critical": "Exceção Crítica: {error}",
            "end_batch": "--- PROCESSAMENTO FINALIZADO ---",
            "finished_popup": "Processamento da fila finalizado.",
            "finished_title": "Fim",
            "install_psutil": "Instale psutil",
            "empty_list": "A lista de arquivos está vazia.",
            "attention": "Atenção",
            "whisper_404": "Whisper não encontrado.",
            "error_save": "Erro ao salvar perfil: {error}",
            "error_load": "Erro ao carregar perfil: {error}",
            "profile_saved_log": "Perfil salvo: {file}",
            "profile_loaded_log": "Perfil carregado.",
            "restart_title": "Reinicialização Necessária",
            "restart_confirm": "Idioma alterado. Reiniciar agora para aplicar?"
        },
        "advanced": {
            "model_dir": "O caminho para salvar arquivos de modelo; usa ~/.cache/whisper por padrão. (default: None)",
            "verbose": "Se deve imprimir mensagens de progresso e depuração. (default: True)",
            "task": "Se deve realizar reconhecimento de fala X->X ('transcribe') ou tradução X->Inglês ('translate'). (default: transcribe)",
            "temperature": "Temperatura a ser usada para amostragem. (default: 0)",
            "best_of": "Número de candidatos ao amostrar com temperatura diferente de zero. (default: 5)",
            "beam_size": "Número de feixes na busca em feixe (beam search), aplicável apenas quando a temperatura é zero. (default: 5)",
            "patience": "Valor de paciência opcional para usar na decodificação de feixe. (default: None)",
            "length_penalty": "Coeficiente de penalidade de comprimento de token opcional (alpha). (default: None)",
            "suppress_tokens": "Lista separada por vírgulas de IDs de token a serem suprimidos durante a amostragem; '-1' suprimirá a maioria dos caracteres especiais. (default: -1)",
            "initial_prompt": "Texto opcional para fornecer como prompt para a primeira janela. (default: None)",
            "carry_initial_prompt": "Se True, precede o initial_prompt em cada chamada interna de decode(). Pode reduzir a eficácia de condition_on_previous_text. (default: False)",
            "condition_on_previous_text": "Se True, fornece a saída anterior do modelo como um prompt para a próxima janela. (default: True)",
            "fp16": "Se deve realizar inferência em fp16. (default: True)",
            "temperature_increment_on_fallback": "Temperatura a aumentar ao recorrer (fallback) quando a decodificação falha em atingir os limites. (default: 0.2)",
            "compression_ratio_threshold": "Se a taxa de compressão gzip for maior que este valor, trata a decodificação como falha. (default: 2.4)",
            "logprob_threshold": "Se a probabilidade logarítmica média for menor que este valor, trata a decodificação como falha. (default: -1.0)",
            "no_speech_threshold": "Se a probabilidade do token <|nospeech|> for maior que este valor E a decodificação falhou, considera silêncio. (default: 0.6)",
            "word_timestamps": "(Experimental) Extrai carimbos de data/hora em nível de palavra. (default: False)",
            "prepend_punctuations": "Se word_timestamps for True, funde estes símbolos de pontuação com a próxima palavra. (default: \"'“¿([{-)\")",
            "append_punctuations": "Se word_timestamps for True, funde estes símbolos de pontuação com a palavra anterior. (default: \"'.。,，!！?？:：”)]}、)\")",
            "highlight_words": "(Requer word_timestamps True) Sublinha cada palavra conforme ela é falada em srt e vtt. (default: False)",
            "max_line_width": "(Requer word_timestamps True) O número máximo de caracteres em uma linha antes de quebrá-la. (default: None)",
            "max_line_count": "(Requer word_timestamps True) O número máximo de linhas em um segmento. (default: None)",
            "max_words_per_line": "(Requer word_timestamps True) O número máximo de palavras em um segmento. (default: None)",
            "threads": "Número de threads usadas pelo torch para inferência de CPU. (default: 0)",
            "clip_timestamps": "Lista separada por vírgulas start,end,... timestamps (em segundos) de clipes a serem processados. (default: 0)",
            "hallucination_silence_threshold": "(Requer word_timestamps True) Pula períodos de silêncio maiores que este limite (em segundos) quando detectada alucinação. (default: None)"
        }
    }
}

PROFILE_FILENAME = "whisper_profile.json"
LANG_MAP = {"English (US)": "en_us", "Português (Brasil)": "pt_br"}

def get_initial_language():
    if os.path.exists(PROFILE_FILENAME):
        try:
            with open(PROFILE_FILENAME, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "app_language" in data:
                    saved = data["app_language"]
                    if saved in LANG_MAP:
                        return LANG_MAP[saved]
        except:
            pass
    return "en_us"

def check_and_install_dependencies():
    required_packages = [
        ("torch", "torch"),
        ("psutil", "psutil"),
        ("tkinterdnd2", "tkinterdnd2"),
        ("openai-whisper", "whisper")
    ]
    
    missing_packages = []
    
    for pip_name, import_name in required_packages:
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_packages.append(pip_name)
            
    if missing_packages:
        root = tk.Tk()
        root.withdraw()
        
        current_lang = get_initial_language()
        txt = TEXTS[current_lang]["dep"]
        
        msg = txt["msg_start"]
        for pkg in missing_packages:
            msg += f"• {pkg}\n"
        msg += txt["msg_end"]
        
        if messagebox.askyesno(txt["title"], msg):
            progress_win = tk.Toplevel(root)
            progress_win.title(txt["installing_title"])
            progress_win.geometry("300x100")
            lbl = tk.Label(progress_win, text=txt["installing_lbl"], padx=20, pady=20)
            lbl.pack()
            progress_win.update()
            
            success = True
            for pkg in missing_packages:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                except subprocess.CalledProcessError:
                    success = False
                    messagebox.showerror(txt["error_title"], txt["error_msg"].format(pkg=pkg))
                    break
            
            if success:
                messagebox.showinfo(txt["success_title"], txt["success_msg"])
                root.destroy()
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                root.destroy()
                sys.exit(1)
        else:
            messagebox.showwarning(txt["warning_title"], txt["warning_msg"])
            root.destroy()

if __name__ == "__main__":
    check_and_install_dependencies()

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 400
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffe0", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class WhisperApp:
    def __init__(self, root):
        self.root = root
        
        self.current_lang_code = get_initial_language()
        self.txt = TEXTS[self.current_lang_code]
        
        self.root.title(self.txt["app_title"])
        self.root.geometry("1120x665")
        
        self.output_dir_var = tk.StringVar()
        self.use_custom_output = tk.BooleanVar(value=False)
        self.app_lang_var = tk.StringVar()
        
        current_lang_name = {v: k for k, v in LANG_MAP.items()}.get(self.current_lang_code, "English (US)")
        self.app_lang_var.set(current_lang_name)
        self.last_app_lang = current_lang_name
        
        self.whisper_installed = False
        self.is_processing = False
        self.stop_monitoring = False
        
        self.configs = {}

        auto_txt = self.txt["ui"].get("auto_detect", "Auto")
        self.formatted_languages = [auto_txt]
        
        raw_langs = {
            "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "as": "Assamese", "az": "Azerbaijani",
            "ba": "Bashkir", "be": "Belarusian", "bg": "Bulgarian", "bn": "Bengali", "bo": "Tibetan",
            "br": "Breton", "bs": "Bosnian", "ca": "Catalan", "cs": "Czech", "cy": "Welsh",
            "da": "Danish", "de": "German", "el": "Greek", "en": "English", "es": "Spanish",
            "et": "Estonian", "eu": "Basque", "fa": "Persian", "fi": "Finnish", "fo": "Faroese",
            "fr": "French", "gl": "Galician", "gu": "Gujarati", "ha": "Hausa", "haw": "Hawaiian",
            "he": "Hebrew", "hi": "Hindi", "hr": "Croatian", "ht": "Haitian Creole", "hu": "Hungarian",
            "hy": "Armenian", "id": "Indonesian", "is": "Icelandic", "it": "Italian", "ja": "Japanese",
            "jw": "Javanese", "ka": "Georgian", "kk": "Kazakh", "km": "Khmer", "kn": "Kannada",
            "ko": "Korean", "la": "Latin", "lb": "Luxembourgish", "ln": "Lingala", "lo": "Lao",
            "lt": "Lithuanian", "lv": "Latvian", "mg": "Malagasy", "mi": "Maori", "mk": "Macedonian",
            "ml": "Malayalam", "mn": "Mongolian", "mr": "Marathi", "ms": "Malay", "mt": "Maltese",
            "my": "Myanmar", "ne": "Nepali", "nl": "Dutch", "nn": "Nynorsk", "no": "Norwegian",
            "oc": "Occitan", "pa": "Punjabi", "pl": "Polish", "ps": "Pashto", "pt": "Portuguese",
            "ro": "Romanian", "ru": "Russian", "sa": "Sanskrit", "sd": "Sindhi", "si": "Sinhala",
            "sk": "Slovak", "sl": "Slovenian", "sn": "Shona", "so": "Somali", "sq": "Albanian",
            "sr": "Serbian", "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", "ta": "Tamil",
            "te": "Telugu", "tg": "Tajik", "th": "Thai", "tk": "Turkmen", "tl": "Tagalog",
            "tr": "Turkish", "tt": "Tatar", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek",
            "vi": "Vietnamese", "yi": "Yiddish", "yo": "Yoruba", "yue": "Cantonese", "zh": "Chinese"
        }
        
        sorted_langs = sorted(raw_langs.items(), key=lambda x: x[1])
        for code, name in sorted_langs:
            self.formatted_languages.append(f"{name} ({code})")

        self._system_check()
        self._setup_ui()
        
        self.load_profile(silent=True)
        self.start_monitor_thread()
        
        if DND_AVAILABLE:
            try:
                self.root.drop_target_register(DND_FILES)
                self.root.dnd_bind('<<Drop>>', self.drop_files)
            except Exception as e:
                print(f"Error DND: {e}")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _system_check(self):
        self.whisper_path = shutil.which("whisper")
        if self.whisper_path:
            self.whisper_installed = True
            self.whisper_status = self.txt["status"]["whisper_installed"]
            self.whisper_color = "green"
        else:
            self.whisper_installed = False
            self.whisper_status = self.txt["status"]["whisper_not_found"]
            self.whisper_color = "red"

        self.device_options = ["cpu"]
        if TORCH_AVAILABLE:
            if torch.cuda.is_available():
                try:
                    gpu_name = torch.cuda.get_device_name(0)
                except:
                    gpu_name = "N/A"
                self.torch_status = self.txt["status"]["pytorch_cuda"].format(gpu=gpu_name)
                self.torch_color = "green"
                self.device_options = ["cuda (gpu)", "cpu"]
            else:
                self.torch_status = self.txt["status"]["pytorch_cpu"]
                self.torch_color = "orange"
                self.device_options = ["cpu"]
        else:
            self.torch_status = self.txt["status"]["pytorch_not_found"]
            self.torch_color = "red"
            
        self.nvidia_smi_path = shutil.which("nvidia-smi")

    def _get_installed_models_list(self):
        cache_dir = os.path.expanduser(os.path.join("~", ".cache", "whisper"))
        models_info = []
        if os.path.exists(cache_dir):
            try:
                files = os.listdir(cache_dir)
                for f in files:
                    if f.endswith(".pt"):
                        path = os.path.join(cache_dir, f)
                        size_mb = os.path.getsize(path) / (1024**2)
                        size_str = f"{size_mb/1024:.2f} GB" if size_mb > 1024 else f"{size_mb:.2f} MB"
                        models_info.append(f"{f} ({size_str})")
            except Exception:
                pass
        return models_info if models_info else [self.txt["ui"]["no_models"]]

    def _setup_ui(self):
        ui_txt = self.txt["ui"]
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        left_pane = tk.Frame(main_container)
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 5))

        status_frame = tk.LabelFrame(left_pane, text=self.txt["status"]["system"], padx=10, pady=5)
        status_frame.pack(side="top", fill="x", padx=5, pady=5)
        tk.Label(status_frame, text=f"Whisper: {self.whisper_status}", fg=self.whisper_color, font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(status_frame, text=f"Dispositivo: {self.torch_status}", fg=self.torch_color, font=("Arial", 9)).pack(anchor="w")

        action_frame = tk.Frame(left_pane, pady=10)
        action_frame.pack(side="bottom", fill="x")

        profile_btns_frame = tk.Frame(action_frame)
        profile_btns_frame.pack(side="left", padx=10)
        
        tk.Button(profile_btns_frame, text=ui_txt["save_profile"], command=self.save_profile, bg="#e1bee7", font=("Arial", 8)).pack(side="left", padx=2)
        tk.Button(profile_btns_frame, text=ui_txt["load_profile"], command=self.load_profile, bg="#d1c4e9", font=("Arial", 8)).pack(side="left", padx=2)

        tk.Button(action_frame, text=ui_txt["reset"], command=self.reset_all, bg="#ffcccc").pack(side="left", padx=10)

        self.btn_generate = tk.Button(action_frame, text=ui_txt["start"], command=self.start_processing_thread, 
                                 bg="#ccffcc", font=("Arial", 12, "bold"), height=2)
        self.btn_generate.pack(side="right", padx=10, fill="x", expand=True)

        self.notebook = ttk.Notebook(left_pane)
        self.notebook.pack(side="top", expand=True, fill="both", padx=5, pady=5)

        self.tab_general = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_general, text=ui_txt["tab_general"])
        
        self.tab_advanced = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_advanced, text=ui_txt["tab_advanced"])

        self.tab_help = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_help, text=ui_txt["tab_help"])

        self._build_general_tab()
        self._build_advanced_tab()
        self._build_help_tab()

        right_pane = tk.Frame(main_container)
        right_pane.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        top_right_container = tk.Frame(right_pane)
        top_right_container.pack(side="top", fill="x", pady=(0, 5))

        monitor_frame = tk.LabelFrame(top_right_container, text=ui_txt["monitor"], padx=5, pady=5)
        monitor_frame.pack(side="left", fill="both", expand=True)
        
        self.lbl_cpu = tk.Label(monitor_frame, text="CPU: ...", font=("Consolas", 9), width=15, anchor="w")
        self.lbl_cpu.grid(row=0, column=0, sticky="w", padx=2)
        
        self.lbl_ram = tk.Label(monitor_frame, text="RAM: ...", font=("Consolas", 9), width=18, anchor="w")
        self.lbl_ram.grid(row=0, column=1, sticky="w", padx=2)
        
        self.lbl_gpu = tk.Label(monitor_frame, text="GPU: ...", font=("Consolas", 9), width=15, anchor="w")
        self.lbl_gpu.grid(row=1, column=0, sticky="w", padx=2)
        
        self.lbl_vram = tk.Label(monitor_frame, text="VRAM: ...", font=("Consolas", 9), width=18, anchor="w")
        self.lbl_vram.grid(row=1, column=1, sticky="w", padx=2)

        lang_frame = tk.LabelFrame(top_right_container, text=ui_txt["app_lang"], padx=5, pady=5)
        lang_frame.pack(side="right", fill="y", padx=(5, 0))
        
        cb_lang = ttk.Combobox(lang_frame, textvariable=self.app_lang_var, values=["English (US)", "Português (Brasil)"], state="readonly", width=18)
        cb_lang.pack(side="left", padx=5, pady=5)
        cb_lang.bind("<<ComboboxSelected>>", self.on_app_lang_change)

        terminal_frame = tk.LabelFrame(right_pane, text=ui_txt["terminal"], padx=5, pady=5)
        terminal_frame.pack(side="bottom", fill="both", expand=True)

        self.terminal_log = scrolledtext.ScrolledText(terminal_frame, state='disabled', bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.terminal_log.pack(fill="both", expand=True)

    def _build_general_tab(self):
        ui_txt = self.txt["ui"]
        file_frame = tk.LabelFrame(self.tab_general, text=ui_txt["files_queue"], padx=10, pady=5)
        file_frame.pack(fill="both", expand=True, padx=10, pady=5)

        dnd_str = ui_txt["dnd_text"] + ui_txt["dnd_drag"] if DND_AVAILABLE else ui_txt["dnd_text"]
        self.btn_files = tk.Button(file_frame, text=dnd_str, command=self.select_files, bg="#f0f0f0", cursor="hand2", pady=2)
        self.btn_files.pack(fill="x", pady=(0, 5))
        ToolTip(self.btn_files, ui_txt["file_tip"])

        if DND_AVAILABLE:
            self.btn_files.drop_target_register(DND_FILES)
            self.btn_files.dnd_bind('<<Drop>>', self.drop_files)

        columns = ("file", "status")
        self.tree = ttk.Treeview(file_frame, columns=columns, show="headings", height=3)
        self.tree.heading("file", text=ui_txt["columns"]["file"])
        self.tree.heading("status", text=ui_txt["columns"]["status"])
        self.tree.column("file", width=250)
        self.tree.column("status", width=100)
        
        vsb = ttk.Scrollbar(file_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        
        tk.Button(file_frame, text=ui_txt["clear"], command=self.clear_list, font=("Arial", 8)).pack(side="bottom", anchor="e", pady=1)

        config_frame = tk.LabelFrame(self.tab_general, text=ui_txt["config"], padx=10, pady=5)
        config_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(config_frame, text=ui_txt["model"]).grid(row=0, column=0, sticky="w")
        self.configs["model"] = tk.StringVar()
        models = [
            "",
            "tiny (~1 GB VRAM, ~10x speed)",
            "base (~1 GB VRAM, ~7x speed)",
            "small (~2 GB VRAM, ~4x speed)",
            "medium (~5 GB VRAM, ~2x speed)",
            "large (~10 GB VRAM, 1x speed)",
            "turbo (~6 GB VRAM, ~8x speed)"
        ]
        ttk.Combobox(config_frame, textvariable=self.configs["model"], values=models, state="readonly", width=35).grid(row=0, column=1, sticky="ew", padx=5)
        
        lbl_inst = tk.Label(config_frame, text=ui_txt["models_cache"], font=("Arial", 8))
        lbl_inst.grid(row=1, column=0, sticky="nw", pady=(5,0))
        
        models_frame = tk.Frame(config_frame)
        models_frame.grid(row=1, column=1, sticky="ew", pady=(5,10), padx=5)
        
        sb_models = tk.Scrollbar(models_frame)
        sb_models.pack(side="right", fill="y")
        
        lb_models = tk.Listbox(models_frame, height=3, width=40, yscrollcommand=sb_models.set, font=("Consolas", 8), bg="#f4f4f4", activestyle="none")
        lb_models.pack(side="left", fill="both", expand=True)
        sb_models.config(command=lb_models.yview)
        
        for m in self._get_installed_models_list():
            lb_models.insert(tk.END, m)

        tk.Label(config_frame, text=ui_txt["language"]).grid(row=2, column=0, sticky="w")
        self.configs["language"] = tk.StringVar(value=self.formatted_languages[0])
        ttk.Combobox(config_frame, textvariable=self.configs["language"], values=self.formatted_languages, state="readonly").grid(row=2, column=1, sticky="ew", padx=5)

        tk.Label(config_frame, text=ui_txt["output_fmt"]).grid(row=3, column=0, sticky="w")
        self.configs["output_format"] = tk.StringVar(value="all")
        ttk.Combobox(config_frame, textvariable=self.configs["output_format"], values=["txt", "vtt", "srt", "tsv", "json", "all"], state="readonly").grid(row=3, column=1, sticky="ew", padx=5)

        tk.Label(config_frame, text=ui_txt["device"]).grid(row=4, column=0, sticky="w")
        self.configs["device"] = tk.StringVar(value=self.device_options[0] if self.device_options else "")
        ttk.Combobox(config_frame, textvariable=self.configs["device"], values=self.device_options, state="readonly").grid(row=4, column=1, sticky="ew", padx=5)
        
        config_frame.columnconfigure(1, weight=1)

        out_frame = tk.LabelFrame(self.tab_general, text=ui_txt["output_dir"], padx=10, pady=5)
        out_frame.pack(fill="x", padx=10, pady=5)
        
        chk = tk.Checkbutton(out_frame, text=ui_txt["custom_dir"], variable=self.use_custom_output, command=self.toggle_output_dir)
        chk.pack(anchor="w")
        ToolTip(chk, ui_txt["custom_dir_tip"])

        self.entry_out_dir = tk.Entry(out_frame, textvariable=self.output_dir_var, state="disabled")
        self.entry_out_dir.pack(fill="x", side="left", expand=True)
        self.btn_out_dir = tk.Button(out_frame, text="...", command=self.select_output_dir, state="disabled")
        self.btn_out_dir.pack(side="right")

    def _build_advanced_tab(self):
        canvas = tk.Canvas(self.tab_advanced)
        scrollbar = ttk.Scrollbar(self.tab_advanced, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        r = 0
        def add_field(label, key, widget_type="entry", values=None):
            nonlocal r
            lbl_widget = tk.Label(scrollable_frame, text=label, cursor="question_arrow")
            lbl_widget.grid(row=r, column=0, sticky="w", padx=5, pady=2)
            
            clean_key = key.replace("--", "")
            if clean_key in self.txt["advanced"]:
                ToolTip(lbl_widget, self.txt["advanced"][clean_key])
            
            self.configs[key] = tk.StringVar()
            if widget_type == "combo":
                ttk.Combobox(scrollable_frame, textvariable=self.configs[key], values=values, width=28, state="readonly").grid(row=r, column=1, sticky="w")
            else:
                tk.Entry(scrollable_frame, textvariable=self.configs[key], width=30).grid(row=r, column=1, sticky="w")
            r += 1

        bools = ["", "True", "False"]
        add_field("--model_dir", "model_dir")
        add_field("--verbose", "verbose", "combo", bools)
        add_field("--task", "task", "combo", ["", "transcribe", "translate"])
        add_field("--temperature", "temperature")
        add_field("--best_of", "best_of")
        add_field("--beam_size", "beam_size")
        add_field("--patience", "patience")
        add_field("--length_penalty", "length_penalty")
        add_field("--suppress_tokens", "suppress_tokens")
        add_field("--initial_prompt", "initial_prompt")
        add_field("--condition_on_previous_text", "condition_on_previous_text", "combo", bools)
        add_field("--fp16", "fp16", "combo", bools)
        add_field("--temperature_increment_on_fallback", "temperature_increment_on_fallback")
        add_field("--compression_ratio_threshold", "compression_ratio_threshold")
        add_field("--logprob_threshold", "logprob_threshold")
        add_field("--no_speech_threshold", "no_speech_threshold")
        add_field("--word_timestamps", "word_timestamps", "combo", bools)
        add_field("--prepend_punctuations", "prepend_punctuations")
        add_field("--append_punctuations", "append_punctuations")
        add_field("--highlight_words", "highlight_words", "combo", bools)
        add_field("--max_line_width", "max_line_width")
        add_field("--max_line_count", "max_line_count")
        add_field("--max_words_per_line", "max_words_per_line")
        add_field("--threads", "threads")
        add_field("--clip_timestamps", "clip_timestamps")
        add_field("--hallucination_silence_threshold", "hallucination_silence_threshold")

    def _build_help_tab(self):
        txt = self.txt["help"]
        frame = ttk.Frame(self.tab_help)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text=txt["about_section"], font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
        tk.Label(frame, text=txt["desc"], justify="left").pack(anchor="w", pady=(0, 10))
        
        tk.Label(frame, text=txt["dev_label"], font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(frame, text=txt["dev_info"], justify="left").pack(anchor="w", pady=(0, 20))

        tk.Label(frame, text=txt["credits_section"], font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        tk.Label(frame, text=txt["credits"], justify="left").pack(anchor="w", pady=(0, 20))

        tk.Label(frame, text=txt["help_section"], font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
        tk.Label(frame, text=txt["disclaimer"], justify="left", wraplength=500).pack(anchor="w", pady=(0, 15))

        link = tk.Label(frame, text=txt["link_label"], fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        link.pack(anchor="w")
        link.bind("<Button-1>", lambda e: webbrowser.open(txt["link_url"]))

    def on_app_lang_change(self, event):
        new_lang = self.app_lang_var.get()
        if new_lang == self.last_app_lang:
            return
            
        msg = self.txt["msgs"]["restart_confirm"]
        title = self.txt["msgs"]["restart_title"]
        
        if messagebox.askyesno(title, msg):
            self.save_profile(restart_mode=True)
            self.root.destroy()
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            self.app_lang_var.set(self.last_app_lang)

    def start_monitor_thread(self):
        threading.Thread(target=self.monitor_loop, daemon=True).start()

    def monitor_loop(self):
        while not self.stop_monitoring:
            cpu_usage = "N/A"
            ram_usage = "N/A"
            gpu_usage = "N/A"
            vram_usage = "N/A"
            
            if PSUTIL_AVAILABLE:
                try:
                    cpu_usage = f"{psutil.cpu_percent()}%"
                    ram = psutil.virtual_memory()
                    used_gb = ram.used / (1024**3)
                    total_gb = ram.total / (1024**3)
                    ram_usage = f"{used_gb:.1f}/{total_gb:.1f} GB"
                except: pass
            else:
                cpu_usage = self.txt["msgs"]["install_psutil"]
                ram_usage = self.txt["msgs"]["install_psutil"]

            if self.nvidia_smi_path:
                try:
                    cmd = [
                        self.nvidia_smi_path, 
                        "--query-gpu=utilization.gpu,memory.used,memory.total", 
                        "--format=csv,noheader,nounits"
                    ]
                    creation_flags = 0x08000000 if sys.platform == "win32" else 0
                    result = subprocess.run(cmd, capture_output=True, text=True, creationflags=creation_flags)
                    
                    if result.returncode == 0:
                        parts = result.stdout.strip().split(',')
                        if len(parts) >= 3:
                            gpu_usage = f"{parts[0].strip()}%"
                            used_mib = float(parts[1].strip())
                            total_mib = float(parts[2].strip())
                            used_gb = used_mib / 1024
                            total_gb = total_mib / 1024
                            vram_usage = f"{used_gb:.1f}/{total_gb:.1f} GB"
                except: pass

            self.root.after(0, lambda: self.update_monitor_labels(cpu_usage, ram_usage, gpu_usage, vram_usage))
            time.sleep(2)

    def update_monitor_labels(self, cpu, ram, gpu, vram):
        self.lbl_cpu.config(text=f"CPU: {cpu}")
        self.lbl_ram.config(text=f"RAM: {ram}")
        self.lbl_gpu.config(text=f"GPU: {gpu}")
        self.lbl_vram.config(text=f"VRAM: {vram}")

    def save_profile(self, restart_mode=False):
        msg_txt = self.txt["msgs"]
        data = {
            "output_dir": self.output_dir_var.get(),
            "use_custom_output": self.use_custom_output.get(),
            "app_language": self.app_lang_var.get(),
            "configs": {k: v.get() for k, v in self.configs.items()}
        }
        
        path = os.path.join(os.getcwd(), PROFILE_FILENAME)
        
        if os.path.exists(path) and not restart_mode:
            if not messagebox.askyesno(self.txt["ui"]["sobrescrever"], msg_txt["overwrite"]):
                return
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            if not restart_mode:
                self.log_to_terminal(msg_txt["profile_saved_log"].format(file=PROFILE_FILENAME))
                messagebox.showinfo(msg_txt["profile_saved_title"], msg_txt["profile_saved"])
        except Exception as e:
            if not restart_mode:
                messagebox.showerror(self.txt["dep"]["error_title"], msg_txt["error_save"].format(error=e))

    def load_profile(self, silent=False):
        msg_txt = self.txt["msgs"]
        path = os.path.join(os.getcwd(), PROFILE_FILENAME)
        if not os.path.exists(path):
            if not silent:
                messagebox.showinfo(self.txt["ui"]["info"], msg_txt["no_profile"])
            return
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "output_dir" in data:
                self.output_dir_var.set(data["output_dir"])
            if "use_custom_output" in data:
                self.use_custom_output.set(data["use_custom_output"])
                self.toggle_output_dir()
                
            if "configs" in data:
                for k, v in data["configs"].items():
                    if k in self.configs:
                        self.configs[k].set(v)
            
            if not silent:
                self.log_to_terminal(msg_txt["profile_loaded_log"])
                messagebox.showinfo(msg_txt["profile_loaded_title"], msg_txt["profile_loaded"])
        except Exception as e:
            if not silent:
                messagebox.showerror(self.txt["dep"]["error_title"], msg_txt["error_load"].format(error=e))

    def log_to_terminal(self, message):
        timestamp = datetime.datetime.now().strftime("(%H:%M:%S) ")
        full_msg = f"{timestamp}{message}\n"
        def _write():
            self.terminal_log.config(state='normal')
            self.terminal_log.insert(tk.END, full_msg)
            self.terminal_log.see(tk.END)
            self.terminal_log.config(state='disabled')
        self.root.after(0, _write)
    
    def log_raw(self, text):
        def _write():
            self.terminal_log.config(state='normal')
            self.terminal_log.insert(tk.END, text)
            self.terminal_log.see(tk.END)
            self.terminal_log.config(state='disabled')
        self.root.after(0, _write)

    def select_files(self):
        filetypes = [("Audio/Video", "*.flac *.m4a *.mp3 *.mp4 *.mpeg *.mpga *.oga *.oga *.ogg *.wav *.webm")]
        files = filedialog.askopenfilenames(title=self.txt["msgs"]["select_files"], filetypes=filetypes)
        self.add_files_to_list(files)

    def drop_files(self, event):
        data = event.data
        files = []
        if '{' in data:
            parts = re.findall(r'\{(.+?)\}|(\S+)', data)
            for p in parts:
                files.append(p[0] if p[0] else p[1])
        else:
            files = data.split()
        self.add_files_to_list(files)

    def add_files_to_list(self, files):
        existing = [self.tree.item(i)['values'][0] for i in self.tree.get_children()]
        for f in files:
            if f not in existing:
                self.tree.insert("", "end", values=(f, self.txt["ui"]["waiting"]))
        self.log_to_terminal(self.txt["msgs"]["files_added"].format(count=len(files)))

    def clear_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.log_to_terminal(self.txt["msgs"]["list_cleared"])

    def toggle_output_dir(self):
        state = "normal" if self.use_custom_output.get() else "disabled"
        self.entry_out_dir.config(state=state)
        self.btn_out_dir.config(state=state)

    def select_output_dir(self):
        d = filedialog.askdirectory()
        if d: self.output_dir_var.set(d)

    def reset_all(self):
        self.clear_list()
        self.use_custom_output.set(False)
        self.toggle_output_dir()
        self.output_dir_var.set("")
        
        for key, var in self.configs.items():
            if key == "device": var.set(self.device_options[0])
            elif key == "language": var.set(self.formatted_languages[0])
            elif key == "output_format": var.set("all")
            else: var.set("")
        self.log_to_terminal(self.txt["msgs"]["config_reset"])

    def start_processing_thread(self):
        if self.is_processing: return
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning(self.txt["msgs"]["attention"], self.txt["msgs"]["empty_list"])
            return
        if not self.whisper_installed:
             messagebox.showerror(self.txt["dep"]["error_title"], self.txt["msgs"]["whisper_404"])
             return

        self.is_processing = True
        self.btn_generate.config(state="disabled", text=self.txt["ui"]["processing"], bg="#ffffcc")
        self.log_to_terminal(self.txt["msgs"]["start_batch"])
        
        threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        msg_txt = self.txt["msgs"]
        ui_txt = self.txt["ui"]
        items = self.tree.get_children()
        base_flags = []
        for key, var in self.configs.items():
            val = var.get().strip()
            if not val: continue
            
            if key == "model":
                val = val.split()[0]
                
            if key == "language":
                if val == self.txt["ui"]["auto_detect"]:
                    continue
                match = re.search(r'\((.*?)\)', val)
                if match:
                    code = match.group(1)
                    if code.lower() in ['detect', 'detectar', 'auto']:
                        continue
                    val = code
            if key == "device" and "cuda" in val: val = "cuda"
            base_flags.append(f"--{key}")
            base_flags.append(val)

        custom_out_dir = self.output_dir_var.get().strip()
        use_custom = self.use_custom_output.get()
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONUTF8"] = "1"

        for i, item_id in enumerate(items):
            file_path = self.tree.item(item_id)['values'][0]
            self.update_status(item_id, ui_txt["processing_state"])
            self.log_to_terminal(msg_txt["file_progress"].format(current=i+1, total=len(items), name=os.path.basename(file_path)))
            
            current_out_dir = custom_out_dir if use_custom else os.path.dirname(file_path)
            cmd = ["whisper", file_path, "--output_dir", current_out_dir] + base_flags
            
            cmd_str = " ".join([f'"{c}"' if " " in c else c for c in cmd])
            self.log_to_terminal(f"CMD >> {cmd_str}")
            
            try:
                creation_flags = 0x08000000 if sys.platform == "win32" else 0
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace', bufsize=1,
                    creationflags=creation_flags, env=env
                )
                
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None: break
                    if line: self.log_raw(line)
                
                return_code = process.poll()
                if return_code == 0:
                    self.update_status(item_id, ui_txt["success_state"])
                    self.log_to_terminal(msg_txt["status_success"])
                else:
                    self.update_status(item_id, ui_txt["error_state"])
                    self.log_to_terminal(msg_txt["status_error"].format(code=return_code))
            except Exception as e:
                self.log_to_terminal(msg_txt["status_critical"].format(error=e))
                self.update_status(item_id, ui_txt["critical_state"])
            
            self.log_to_terminal("-" * 30)

        self.root.after(0, self.finish_processing)

    def update_status(self, item_id, status):
        self.root.after(0, lambda: self.tree.set(item_id, "status", status))

    def finish_processing(self):
        self.is_processing = False
        self.btn_generate.config(state="normal", text=self.txt["ui"]["start"], bg="#ccffcc")
        self.log_to_terminal(self.txt["msgs"]["end_batch"])
        messagebox.showinfo(self.txt["msgs"]["finished_title"], self.txt["msgs"]["finished_popup"])

    def on_close(self):
        self.stop_monitoring = True
        self.root.destroy()

if __name__ == "__main__":
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = WhisperApp(root)
    root.mainloop()
