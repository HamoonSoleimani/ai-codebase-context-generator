# AI Codebase Context Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern desktop application built by **Hamoon Soleimani** to consolidate any code project into a single, structured text file. This output is perfectly formatted for large language models (LLMs) like GPT-4, Claude, and Gemini, allowing you to give the AI a comprehensive view of your entire codebase for advanced debugging, analysis, and refactoring.

---

### Screenshot
<img width="1922" height="1018" alt="image" src="https://github.com/user-attachments/assets/b7d932aa-e7aa-4fa4-8da0-bdc2aafa27f5" />

---

### The Problem It Solves

When working with AI models, providing context is key. Pasting individual files is tedious and often misses the "big picture"—dependencies in `build.gradle`, settings in `AndroidManifest.xml`, or connections between different classes. This tool automates the process, creating a complete, single-file context that gives the AI everything it needs to understand your project's architecture.

### Key Features

- **Modern & Intuitive UI:** Built with `customtkinter` for a beautiful, themeable interface that works on Windows, macOS, and Linux.
- **Interactive File Selection:** Easily browse for your project directory and choose where to save the consolidated output file.
- **Fully Customizable Rules:** Interactively edit lists of file extensions to include and directories/files to exclude, tailoring the output to your exact needs.
- **Non-Blocking Operation:** The heavy lifting is done in a background thread, ensuring the application UI never freezes, even with large projects.
- **Real-time Progress:** A dynamic progress bar and status label show you exactly which file is being processed.
- **Detailed Summary Report:** After processing, get a full report including files processed, total lines of code, and final output size.
- **Convenient Post-Actions:**
  - **Copy to Clipboard:** Instantly copy the entire generated text with a single click.
  - **Open File:** Immediately open the generated `.txt` file in your default text editor.

---

### Installation

To run this application, you need Python 3 and the `customtkinter` library.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/HamoonSoleimani/ai-codebase-context-generator.git
    cd ai-codebase-context-generator
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

### How to Use

1.  **Run the application:**
    ```sh
    python main.py
    ```
2.  **Select Project Directory:** Click the first "Browse..." button and choose the root folder of your code project.
3.  **Select Output File:** Click the "Save As..." button and choose a name and location for the final `.txt` file.
4.  **Configure Rules (Optional):** Modify the comma-separated lists of extensions to include or patterns to exclude.
5.  **Click "Generate Context File"**: The process will start, and you can monitor the progress.
6.  **Use the Output:** Once complete, use the **"Copy to Clipboard"** button and paste the entire context into your chosen AI model along with your request.

---

### Contributing

Contributions are welcome! If you have ideas for new features or find a bug, please feel free to open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

### License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

---

### Acknowledgments

-   This tool was inspired by the need for better context in AI-assisted programming.
-   Built with the excellent [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) library.
