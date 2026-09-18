<div align="center">

  <h1>🔥 Yashvir Intelligence Core v1.0 🔥</h1>
  <p><b>Next-Generation Local Desktop AI Workspace Powered by llama.cpp & PySide6</b></p>

  <p>
    <a href="https://youtube.com/@yashvirgaming" target="_blank">
      <img src="https://img.shields.io/badge/YouTube-Yashvir_Gaming-red?style=for-the-badge&logo=youtube" alt="YouTube">
    </a>
    <a href="https://t.me/@YashvirGamingX" target="_blank">
      <img src="https://img.shields.io/badge/Telegram-Join_Community-blue?style=for-the-badge&logo=telegram" alt="Telegram">
    </a>
    <img src="https://img.shields.io/badge/Version-1.0-brightgreen?style=for-the-badge" alt="Version 1.0">
    <img src="https://img.shields.io/badge/Platform-Windows_x64-0078D6?style=for-the-badge&logo=windows" alt="Platform">
  </p>

</div>

<hr>

<h2>🚀 Overview</h2>
<p>
  <b>Yashvir Intelligence Core v1.0</b> is a fully self-contained, high-performance desktop LLM chat interface designed for total privacy and raw GPU acceleration.
</p>
<p>
  By bypassing third-party orchestration tools, this application natively embeds a custom <code>llama-server.exe</code> backend alongside a sleek <b>PySide6</b> GUI. It dynamically offloads model layers to your NVIDIA GPU (CUDA 12.x / 13.x) while streaming tokens in real time via an asynchronous <code>httpx</code> engine.
</p>

<hr>

<h2>⚠️ CRITICAL: Required External Downloads (Must Read!)</h2>
<p>
  Due to GitHub's file size restrictions, the <b><code>runtime/</code></b> binaries folder and the <b><code>YashvirIntelligence.gguf</code></b> model weights are <b>NOT</b> included directly in this repository. 
  <br><br>
  <b>The application WILL NOT RUN without these two components manually placed inside your <code>dist/hacker_chat.dist/</code> folder.</b>
</p>

<h3>📥 Download Links:</h3>
<ul>
  <li>
    <b>📦 Download Runtime Engine (<code>runtime/</code> folder):</b><br>
    <a href="https://drive.google.com/drive/folders/1ShYgzeFQ8npQV7XExJHpykWTDEehBq-u?usp=drive_link" target="_blank">👉 Direct Google Drive Link (llama-server & CUDA DLLs)</a>
  </li>
  <br>
  <li>
    <b>🧠 Download Model Weights (<code>YashvirIntelligence.gguf</code>):</b><br>
    <a href="https://drive.google.com/file/d/1TMpQmH0Zx3uniqXoKQUw_IEHA1bbCgZN/view?usp=sharing" target="_blank">👉 Direct Google Drive Link (8.2 GB GGUF Model)</a>
  </li>
</ul>

<h3>⚙️ Quick Setup Instructions for End Users:</h3>
<ol>
  <li>Download the <b><code>runtime/</code></b> folder and place it directly inside <code>dist/hacker_chat.dist/</code>.</li>
  <li>Download <b><code>YashvirIntelligence.gguf</code></b> and place it directly inside <code>dist/hacker_chat.dist/</code> alongside <code>YashvirIntelligence.exe</code>.</li>
  <li>Launch <b><code>YashvirIntelligence.exe</code></b> to start using the app!</li>
</ol>

<hr>

<h2>📂 Executable Directory Layout</h2>
<p>Your <code>dist/hacker_chat.dist/</code> folder must strictly match this structure to run:</p>

<pre><code>dist/hacker_chat.dist/
├── YashvirIntelligence.exe     # Standalone Executable
├── YashvirIntelligence.gguf    # 🧠 Downloaded from Google Drive
├── runtime/                    # 📦 Downloaded from Google Drive
│   ├── llama-server.exe        # Native llama.cpp Server
│   ├── llama.dll               # Core LLM Engine Library
│   ├── ggml.dll                # Tensor Library
│   └── cudart64_13.dll         # NVIDIA CUDA Libraries
└── ... (Qt & Python Binaries)</code></pre>

<hr>

<h2>🔥 Key Features</h2>
<ul>
  <li><b>📦 Fully Portable Executable:</b> Runs natively without requiring Python, Pip, PySide6, or external model managers installed on the host machine.</li>
  <li><b>⚡ Native GPU Offloading:</b> Auto-configured <code>llama.cpp</code> binary offloading (<code>-ngl 99</code>) for maximum inference speed on NVIDIA RTX GPUs.</li>
  <li><b>🎨 Dynamic Gradient Theme Engine:</b> Swap styles on the fly via the sidebar dropdown:
    <ul>
      <li>🌌 <b>Cyberpunk Neon</b> (Cyan & Magenta Gradients)</li>
      <li>🟢 <b>Matrix Hacker</b> (Terminal Green Aesthetics)</li>
      <li>🍇 <b>Midnight Purple</b> (Velvet Violet Gradients)</li>
      <li>🌑 <b>Pure Dark Metal</b> (Steel & Obsidian Aesthetics)</li>
      <li>⚪ <b>Light Pearl</b> (Modern Light-Mode Theme)</li>
    </ul>
  </li>
  <li><b>📎 Multi-File Attachment System:</b> Attach source code files (<code>.py</code>, <code>.json</code>, <code>.txt</code>, <code>.csv</code>, <code>.md</code>, etc.) directly to your context window.</li>
  <li><b>🔍 Auto-GGUF Detection:</b> Automatically scans and detects any <code>.gguf</code> model file located in the application root directory.</li>
  <li><b>📊 Syntax Highlighting & Rendered Markdown:</b> Powered by Pygments and Markdown extensions with full table, list, and code block formatting.</li>
  <li><b>🧹 Clean Shutdown & VRAM Release:</b> Features an automated force-cleanup process tree terminator (<code>taskkill /F /T /PID</code>) to immediately free system RAM and GPU VRAM upon exit.</li>
</ul>

<hr>

<h2>💻 Compiling from Source (Developers)</h2>

<p>If you prefer to modify the code and compile the binary yourself:</p>

<ol>
  <li>Install dependencies:
<pre><code>pip install PySide6 httpx markdown pygments nuitka pillow pillow-heif</code></pre>
  </li>
  <li>Place your downloaded <code>runtime/</code> folder into the root directory.</li>
  <li>Run the automated Nuitka build pipeline:
<pre><code>NuitkaBuilder.bat</code></pre>
  </li>
  <li>Copy <code>YashvirIntelligence.gguf</code> into <code>dist/hacker_chat.dist/</code> and launch <code>YashvirIntelligence.exe</code>.</li>
</ol>

<hr>

<div align="center">

  <h2>👨‍💻 Developed by Yashvir Gaming</h2>

  <p>
    <a href="https://youtube.com/@yashvirgaming" target="_blank">
      <img src="https://img.shields.io/badge/Subscribe_on_YouTube-red?style=for-the-badge&logo=youtube" alt="Subscribe on YouTube">
    </a>
    <a href="https://t.me/@YashvirGamingX" target="_blank">
      <img src="https://img.shields.io/badge/Join_Telegram_Channel-blue?style=for-the-badge&logo=telegram" alt="Join Telegram Channel">
    </a>
  </p>

  <p><i>Copyright © 2026 Yashvir Gaming. All Rights Reserved.</i></p>

</div>