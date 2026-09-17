##  Coded by Yashvir Gaming
##  Subscribe on YouTube - https://youtube.com/@yashvirgaming
##  Release version 1.0 on Github & Telegram -> https://t.me/@YashvirGamingX


import sys
import os
import time
import html
import json
import asyncio
import subprocess
import httpx
import markdown
from pathlib import Path
from pygments.formatters import HtmlFormatter
from PySide6.QtCore import Qt, QThread, Signal, Slot, QSize
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextBrowser,
    QTextEdit,
    QPushButton,
    QLabel,
    QFrame,
    QSplitter,
    QComboBox,
    QFileDialog,
)

SERVER_PORT = 8080
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}"
PYGMENTS_CSS = HtmlFormatter(style="monokai").get_style_defs(".codehilite")

# ----------------------------------------------------------------------
# DYNAMIC GRADIENT THEME ENGINE
# ----------------------------------------------------------------------
THEMES = {
    "Cyberpunk Neon": {
        "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f0c1b, stop:0.5 #1a0933, stop:1 #2d0b4e)",
        "sidebar_bg": "#120824",
        "chat_bg": "#0c0717",
        "input_bg": "#1c0d38",
        "user_bubble": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7928ca, stop:1 #ff0080)",
        "text_color": "#00f0ff",
        "accent": "#ff007f",
        "border": "#7928ca",
        "pygments": "monokai"
    },
    "Matrix Hacker": {
        "main_bg": "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #020d04, stop:1 #001a05)",
        "sidebar_bg": "#011204",
        "chat_bg": "#000a02",
        "input_bg": "#032108",
        "user_bubble": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #005511, stop:1 #00aa22)",
        "text_color": "#00ff66",
        "accent": "#00ff44",
        "border": "#00ff33",
        "pygments": "vim"  # <-- Changed from 'terminal' to 'vim'
    },
    "Midnight Purple": {
        "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #130f40, stop:1 #000000)",
        "sidebar_bg": "#0c0926",
        "chat_bg": "#08061a",
        "input_bg": "#1a1554",
        "user_bubble": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4834d4, stop:1 #686de0)",
        "text_color": "#f1f2f6",
        "accent": "#be2edd",
        "border": "#4834d4",
        "pygments": "dracula"
    },
    "Pure Dark Metal": {
        "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1c20, stop:1 #0f1012)",
        "sidebar_bg": "#141518",
        "chat_bg": "#111215",
        "input_bg": "#22252b",
        "user_bubble": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a3d45, stop:1 #525763)",
        "text_color": "#ececf1",
        "accent": "#ffffff",
        "border": "#3a3d45",
        "pygments": "monokai"
    },
    "Light Pearl": {
        "main_bg": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f5f7fa, stop:1 #c3cfe2)",
        "sidebar_bg": "#e4e8f0",
        "chat_bg": "#ffffff",
        "input_bg": "#f0f3f8",
        "user_bubble": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0072ff, stop:1 #00c6ff)",
        "text_color": "#1a1a2e",
        "accent": "#0072ff",
        "border": "#0072ff",
        "pygments": "default"
    }
}


def get_app_directory() -> Path:
    """Returns the true directory where YashvirIntelligence.exe lives (where .gguf is located)."""
    if getattr(sys, "frozen", False) or hasattr(sys, "__compiled__"):
        # sys.argv[0] gives the actual location of the .exe on the user's disk
        exe_path = Path(sys.argv[0]).resolve()
        if exe_path.is_file():
            return exe_path.parent
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def get_runtime_directory() -> Path:
    """Returns the unpacked runtime path inside Nuitka onefile or local folder."""
    # 1. Check Nuitka onefile temporary unpacked directory
    if hasattr(sys, "_MEIPASS"):
        onefile_runtime = Path(sys._MEIPASS) / "runtime"
        if (onefile_runtime / "llama-server.exe").exists():
            return onefile_runtime

    # 2. Check local script execution path
    script_runtime = Path(__file__).resolve().parent / "runtime"
    if (script_runtime / "llama-server.exe").exists():
        return script_runtime

    # 3. Fallback to external runtime folder next to the EXE
    return get_app_directory() / "runtime"


def find_gguf_model() -> Path:
    app_dir = get_app_directory()
    models = list(app_dir.glob("*.gguf"))
    if not models:
        raise FileNotFoundError("No .gguf model found in application folder.")
    if len(models) > 1:
        raise RuntimeError("Multiple .gguf models found. Keep only one .gguf file.")
    return models[0]


class ServerManager:
    def __init__(self):
        self.process = None

    def start_server(self, model_path: Path):
        runtime_dir = get_runtime_directory()
        exe_path = runtime_dir / "llama-server.exe"

        if not exe_path.exists():
            raise FileNotFoundError(f"llama-server.exe not found at: {exe_path}")

        cmd = [
            str(exe_path),
            "-m", str(model_path),
            "-c", "4096",
            "--port", str(SERVER_PORT),
            "-ngl", "99"
        ]

        creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

        self.process = subprocess.Popen(
            cmd,
            cwd=str(runtime_dir),
            creationflags=creation_flags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        health_endpoint = f"{SERVER_URL}/health"
        for _ in range(30):
            try:
                with httpx.Client(timeout=1.0) as client:
                    r = client.get(health_endpoint)
                    if r.status_code == 200:
                        return
            except httpx.RequestError:
                pass
            time.sleep(1)

        raise RuntimeError("llama-server timed out during startup.")

    def stop_server(self):
        if self.process:
            pid = self.process.pid
            try:
                if os.name == "nt":
                    # Forcefully kill llama-server.exe AND all sub-threads on Windows
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                else:
                    self.process.kill()
            except Exception as e:
                print(f"Error terminating server process tree: {e}")
            finally:
                self.process = None


class AsyncLlamaStreamWorker(QThread):
    chunk_received = Signal(str)
    stream_complete = Signal(str)
    stream_failed = Signal(str)

    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.history = list(history)
        self.accumulated_text = ""

    def run(self):
        asyncio.run(self.stream_inference())

    async def stream_inference(self):
        try:
            url = f"{SERVER_URL}/v1/chat/completions"
            headers = {"Content-Type": "application/json"}
            payload = {
                "messages": self.history,
                "stream": True,
                "temperature": 0.7
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    if response.status_code != 200:
                        error_bytes = await response.aread()
                        raise RuntimeError(f"HTTP Error {response.status_code}: {error_bytes.decode('utf-8')}")

                    async for line in response.aiter_lines():
                        if self.isInterruptionRequested():
                            return

                        if line and line.startswith("data: "):
                            data_content = line[6:].strip()
                            if data_content == "[DONE]":
                                break

                            try:
                                json_obj = json.loads(data_content)
                                delta = json_obj.get("choices", [{}])[0].get("delta", {})
                                token = delta.get("content", "")
                                if token:
                                    self.accumulated_text += token
                                    self.chunk_received.emit(self.accumulated_text)
                            except json.JSONDecodeError:
                                pass

            self.stream_complete.emit(self.accumulated_text)

        except Exception as error:
            self.stream_failed.emit(str(error))


class YashvirIntelligenceApp(QMainWindow):
    def __init__(self, server_manager):
        super().__init__()
        self.server_manager = server_manager

        self.setWindowTitle("Yashvir Intelligence Core v1.0")
        self.setMinimumSize(1100, 780)

        self.chat_history = []
        self.attached_files = []
        self.processing_thread = None
        self.current_theme_name = "Cyberpunk Neon"

        self.init_interface_components()
        self.apply_theme(self.current_theme_name)

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        theme = THEMES.get(theme_name, THEMES["Cyberpunk Neon"])

        style_sheet = f"""
            QMainWindow {{
                background: {theme['main_bg']};
            }}
            QWidget {{
                color: {theme['text_color']};
                font-family: "Segoe UI", sans-serif;
                font-size: 14px;
            }}
            QFrame#SidebarPanel {{
                background-color: {theme['sidebar_bg']};
                border-right: 1px solid {theme['border']};
            }}
            QPushButton#NewChatBtn, QPushButton#AttachBtn {{
                background-color: transparent;
                border: 1px solid {theme['border']};
                border-radius: 8px;
                color: {theme['text_color']};
                padding: 10px;
                font-weight: bold;
                text-align: left;
            }}
            QPushButton#NewChatBtn:hover, QPushButton#AttachBtn:hover {{
                background-color: {theme['border']};
                color: #FFFFFF;
            }}
            QComboBox#ThemeDropdown {{
                background-color: {theme['input_bg']};
                border: 1px solid {theme['border']};
                border-radius: 6px;
                padding: 5px;
                color: {theme['text_color']};
            }}
            QTextBrowser#ChatConsole {{
                background-color: {theme['chat_bg']};
                border: none;
                padding: 20px;
            }}
            QFrame#InputContainerFrame {{
                background-color: {theme['input_bg']};
                border: 2px solid {theme['border']};
                border-radius: 14px;
            }}
            QTextEdit#PromptTextEditor {{
                background-color: transparent;
                border: none;
                color: {theme['text_color']};
                font-size: 15px;
            }}
            QPushButton#ActionSubmitBtn {{
                background-color: {theme['accent']};
                color: #FFFFFF;
                border: none;
                border-radius: 18px;
                font-weight: bold;
            }}
            QPushButton#ActionSubmitBtn:hover {{
                opacity: 0.8;
            }}
            QSplitter::handle {{
                background-color: {theme['border']};
            }}
        """
        self.setStyleSheet(style_sheet)
        self.refresh_html_rendering("")

    def init_interface_components(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        base_layout = QHBoxLayout(central_widget)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        base_layout.addWidget(splitter)

        # ------------------ SIDEBAR ------------------
        sidebar = QFrame()
        sidebar.setObjectName("SidebarPanel")
        sidebar.setMinimumWidth(220)
        sidebar.setMaximumWidth(320)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 18, 14, 18)

        new_chat_button = QPushButton("＋  New Session")
        new_chat_button.setObjectName("NewChatBtn")
        new_chat_button.clicked.connect(self.clear_chat_matrix)

        theme_label = QLabel("Theme Engine:")
        theme_label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        self.theme_dropdown = QComboBox()
        self.theme_dropdown.setObjectName("ThemeDropdown")
        self.theme_dropdown.addItems(list(THEMES.keys()))
        self.theme_dropdown.currentTextChanged.connect(self.apply_theme)

        sidebar_layout.addWidget(new_chat_button)
        sidebar_layout.addWidget(theme_label)
        sidebar_layout.addWidget(self.theme_dropdown)
        sidebar_layout.addStretch()

        system_status = QLabel("● Engine Active\nllama.cpp + Async HTTPX")
        system_status.setStyleSheet("opacity: 0.7; font-size: 12px;")
        sidebar_layout.addWidget(system_status)

        splitter.addWidget(sidebar)

        # ------------------ MAIN CANVAS ------------------
        canvas_window = QWidget()
        canvas_layout = QVBoxLayout(canvas_window)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.setSpacing(0)

        self.browser_display = QTextBrowser()
        self.browser_display.setObjectName("ChatConsole")
        self.browser_display.setOpenExternalLinks(True)
        canvas_layout.addWidget(self.browser_display)

        # File Attachment Display Frame
        self.file_label = QLabel("")
        self.file_label.setStyleSheet("padding: 4px 40px; color: #ff007f; font-weight: bold;")
        canvas_layout.addWidget(self.file_label)

        # Input Wrapper
        input_alignment_wrapper = QHBoxLayout()
        input_alignment_wrapper.setContentsMargins(40, 0, 40, 25)

        input_container_box = QFrame()
        input_container_box.setObjectName("InputContainerFrame")
        input_container_box.setMinimumHeight(56)

        input_box_layout = QHBoxLayout(input_container_box)
        input_box_layout.setContentsMargins(12, 8, 12, 8)
        input_box_layout.setSpacing(8)

        # Attach File Button
        self.btn_attach = QPushButton("📎")
        self.btn_attach.setObjectName("AttachBtn")
        self.btn_attach.setFixedSize(QSize(36, 36))
        self.btn_attach.clicked.connect(self.handle_file_attachment)
        input_box_layout.addWidget(self.btn_attach)

        self.input_editor = QTextEdit()
        self.input_editor.setObjectName("PromptTextEditor")
        self.input_editor.setPlaceholderText("Message Yashvir Intelligence or attach code/files...")
        self.input_editor.setMinimumHeight(36)
        self.input_editor.setMaximumHeight(120)
        self.input_editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        input_box_layout.addWidget(self.input_editor)

        self.btn_submit = QPushButton("↑")
        self.btn_submit.setObjectName("ActionSubmitBtn")
        self.btn_submit.setFixedSize(QSize(36, 36))
        self.btn_submit.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.btn_submit.clicked.connect(self.trigger_generation_pipeline)

        input_box_layout.addWidget(self.btn_submit)
        input_alignment_wrapper.addWidget(input_container_box)
        canvas_layout.addLayout(input_alignment_wrapper)

        splitter.addWidget(canvas_window)
        splitter.setSizes([240, 860])

    def handle_file_attachment(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Attach Files", "", "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
        )
        if file_paths:
            for path_str in file_paths:
                p = Path(path_str)
                try:
                    content = p.read_text(encoding="utf-8", errors="ignore")
                    self.attached_files.append({"filename": p.name, "content": content})
                except Exception as e:
                    print(f"Failed to read file {p.name}: {e}")

            names = ", ".join([f['filename'] for f in self.attached_files])
            self.file_label.setText(f"📎 Attached ({len(self.attached_files)}): {names}")

    def clear_chat_matrix(self):
        if self.processing_thread and self.processing_thread.isRunning():
            return
        self.chat_history.clear()
        self.attached_files.clear()
        self.file_label.setText("")
        self.refresh_html_rendering("")

    def transform_markdown_to_rich_html(self, raw_markdown_text):
        if not raw_markdown_text:
            return ""
        try:
            return markdown.markdown(
                raw_markdown_text,
                extensions=["extra", "codehilite", "fenced_code", "tables"],
                extension_configs={"codehilite": {"guess_lang": False, "css_class": "codehilite"}},
            )
        except Exception:
            escaped_text = html.escape(raw_markdown_text)
            return escaped_text.replace("\n", "<br>")

    def build_document_html(self):
        theme = THEMES.get(self.current_theme_name, THEMES["Cyberpunk Neon"])

        try:
            pyg_css = HtmlFormatter(style=theme["pygments"]).get_style_defs(".codehilite")
        except Exception:
            pyg_css = HtmlFormatter(style="monokai").get_style_defs(".codehilite")

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ background-color: transparent; color: {theme['text_color']}; font-family: "Segoe UI", sans-serif; font-size: 14px; line-height: 1.6; padding: 15px; }}
                h1, h2, h3 {{ color: {theme['accent']}; }}
                .user-bubble {{ background: {theme['user_bubble']}; border-radius: 12px; padding: 12px 16px; color: #FFFFFF; display: inline-block; max-width: 85%; }}
                .assistant-bubble {{ padding: 12px 0; color: {theme['text_color']}; }}
                pre {{ background-color: {theme['input_bg']}; border-radius: 8px; border: 1px solid {theme['border']}; padding: 14px; white-space: pre-wrap; word-wrap: break-word; }}
                code {{ font-family: "Consolas", monospace; }}
                hr {{ border: 0; border-top: 1px solid {theme['border']}; margin: 15px 0; }}
                {pyg_css}
            </style>
        </head>
        <body>
        """

    def refresh_html_rendering(self, transient_stream_buffer):
        dynamic_html_body = self.build_document_html()

        for message in self.chat_history:
            role = message.get("role", "")
            content = message.get("content", "")
            formatted_content = self.transform_markdown_to_rich_html(content)

            if role == "user":
                dynamic_html_body += f"""
                <div style="text-align: right; margin: 12px 0;">
                    <div class="user-bubble">{formatted_content}</div>
                </div>
                """
            elif role == "assistant":
                dynamic_html_body += f"""
                <div class="assistant-bubble">
                    <b>Yashvir Intelligence</b><br>
                    {formatted_content}
                </div>
                <hr>
                """

        if transient_stream_buffer:
            active_html = self.transform_markdown_to_rich_html(transient_stream_buffer)
            dynamic_html_body += f"""
            <div class="assistant-bubble">
                <b>Yashvir Intelligence</b><br>
                {active_html}
            </div>
            """

        dynamic_html_body += "</body></html>"
        self.browser_display.setHtml(dynamic_html_body)
        self.browser_display.moveCursor(QTextCursor.End)

    def trigger_generation_pipeline(self):
        raw_prompt = self.input_editor.toPlainText().strip()
        if (not raw_prompt and not self.attached_files) or (self.processing_thread and self.processing_thread.isRunning()):
            return

        final_prompt = raw_prompt

        # Inject attached files into context
        if self.attached_files:
            file_context = "\n\n--- ATTACHED FILES ---\n"
            for f in self.attached_files:
                file_context += f"\nFile: {f['filename']}\n```\n{f['content']}\n```\n"
            final_prompt = f"{raw_prompt}{file_context}"

        self.input_editor.clear()
        self.attached_files.clear()
        self.file_label.setText("")

        self.chat_history.append({"role": "user", "content": final_prompt})
        self.refresh_html_rendering("")

        self.input_editor.setDisabled(True)
        self.btn_submit.setDisabled(True)

        self.processing_thread = AsyncLlamaStreamWorker(self.chat_history, self)
        self.processing_thread.chunk_received.connect(self.handle_stream_delta)
        self.processing_thread.stream_complete.connect(self.handle_stream_resolution)
        self.processing_thread.stream_failed.connect(self.handle_processing_failure)
        self.processing_thread.finished.connect(self.handle_thread_finished)
        self.processing_thread.start()

    @Slot(str)
    def handle_stream_delta(self, running_buffer_string):
        self.refresh_html_rendering(running_buffer_string)

    @Slot(str)
    def handle_stream_resolution(self, comprehensive_response_string):
        self.chat_history.append({"role": "assistant", "content": comprehensive_response_string})
        self.refresh_html_rendering("")
        self.unlock_user_controls()

    @Slot(str)
    def handle_processing_failure(self, error_trace):
        error_message = f"⚠️ **Inference Failure:**\n\n`{error_trace}`"
        self.chat_history.append({"role": "assistant", "content": error_message})
        self.refresh_html_rendering("")
        self.unlock_user_controls()

    @Slot()
    def handle_thread_finished(self):
        self.processing_thread = None

    def unlock_user_controls(self):
        self.input_editor.setEnabled(True)
        self.btn_submit.setEnabled(True)
        self.input_editor.setFocus()

    def closeEvent(self, event):
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.requestInterruption()
            self.processing_thread.wait(3000)
        self.server_manager.stop_server()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    server_manager = ServerManager()

    try:
        model_path = find_gguf_model()
        server_manager.start_server(model_path)
    except Exception as e:
        import traceback
        error_msg = f"Startup Failed!\n\nError: {e}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Yashvir Intelligence Core - Startup Error", error_msg)
        
        server_manager.stop_server()
        sys.exit(1)

    main_window = YashvirIntelligenceApp(server_manager)
    main_window.show()

    exit_code = app.exec()
    server_manager.stop_server()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()



##  Coded by Yashvir Gaming
##  Subscribe on YouTube - https://youtube.com/@yashvirgaming
##  Release version 1.0 on Github & Telegram -> https://t.me/@YashvirGamingX