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

<h2>🛠️ Complete Technical Changelog & Fixes (v1.0)</h2>

<details>
  <summary><b>Click to expand full v1.0 engineering details</b></summary>
  <br>

  <h3>1. Architecture Overhaul</h3>
  <ul>
    <li>Replaced third-party streaming clients with a lightweight, direct HTTP OpenAI-compatible endpoint (<code>http://127.0.0.1:8080/v1/chat/completions</code>).</li>
    <li>Integrated an <code>asyncio</code> event loop thread runner (<code>AsyncLlamaStreamWorker</code>) with <code>httpx.AsyncClient</code> for low-latency line-by-line SSE token parsing.</li>
  </ul>

  <h3>2. UI & CSS Engine Fixes</h3>
  <ul>
    <li>Resolved string formatting crashes (<code>SyntaxError: f-string: single '}' is not allowed</code>) by escaping QSS and HTML stylesheet blocks (<code>{{ }}</code>).</li>
    <li>Added a graceful Pygments fallback mechanism in <code>build_document_html()</code> to prevent missing syntax theme crashes (<code>ClassNotFound</code>).</li>
  </ul>

  <h3>3. Memory & Process Lifecycle Fixes</h3>
  <ul>
    <li>Updated process termination from gentle <code>.terminate()</code> to Windows tree-kill (<code>taskkill /F /T /PID</code>). This eliminates orphan <code>llama-server.exe</code> background processes and releases up to ~23 GB of trapped host RAM/VRAM instantly.</li>
  </ul>

  <h3>4. Build & Nuitka 4.x Production Pipeline</h3>
  <ul>
    <li>Built custom <code>NuitkaBuilder.bat</code> with CPU auto-detection (<code>%NUMBER_OF_PROCESSORS%</code>), dynamic <code>.ico</code> fallback engines, auto-download flags, and automated build artifact cleanup (<code>rmdir</code>).</li>
  </ul>
</details>

<hr>

<h2>📂 Project Directory Layout</h2>

<pre><code>YashvirIntelligence/
├── hacker_chat.py              # Main Application Entry Point
├── YashvirIntelligence.gguf    # Model Weights Binary (8+ GB GGUF)
├── app_icon.ico                # High-Res Multi-Layer Icon
├── requirements.txt            # Pinned Dependencies
├── NuitkaBuilder.bat           # Automated Compiler Engine
└── runtime/
    ├── llama-server.exe        # Native llama.cpp Server Executable
    ├── llama.dll               # Core LLM Engine Library
    ├── ggml.dll                # Tensor Library
    └── cudart64_13.dll         # NVIDIA CUDA Runtime Libraries</code></pre>

<hr>

<h2>🛠️ Build Requirements</h2>

<p>Install all required runtime and compilation dependencies before building:</p>

<pre><code>PySide6&gt;=6.6.0
httpx&gt;=0.25.0
markdown&gt;=3.5.0
pygments&gt;=2.17.0
nuitka&gt;=4.1.3
pillow&gt;=10.0.0
pillow-heif&gt;=0.13.0</code></pre>

<hr>

<h2>💻 Compiling to Standalone EXE</h2>

<p>To compile the Python application and bundled runtime environment into a single portable binary <code>YashvirIntelligence.exe</code>, run the batch script from Command Prompt:</p>

<pre><code>NuitkaBuilder.bat</code></pre>

<hr>

<h3>📥 Model Download</h3>
<p>
  Download the required model weights file (<code>YashvirIntelligence.gguf</code>) from 
  <a href="DRIVE_LINK_HERE">Direct Link</a> 
  and place it inside the root directory alongside the executable.
</p>

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
