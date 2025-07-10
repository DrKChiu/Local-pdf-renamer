# PDF Renamer

This Python script helps you batch rename PDF files in a directory based on their metadata (author, title, and publication year). If metadata is missing or insufficient, it attempts to extract information from the text content of the first few pages, falling back to OCR (Optical Character Recognition) for scanned or image-based PDFs.

## ⚠️ **IMPORTANT LEGAL NOTICE**

**This tool is for personal research and academic use only. Users must comply with all applicable copyright laws and publisher terms of service.**

### **Legal Requirements:**
- **Lawful Access Required**: You must have lawful access to any PDFs you process with this tool
- **Non-Commercial Use Only**: This tool is intended for personal research, not commercial purposes
- **Respect Copyright**: Do not use this tool to process PDFs you do not have permission to access
- **Publisher Terms**: Check individual journal/publisher terms of service before use
- **User Responsibility**: Users are responsible for ensuring their use complies with applicable laws

### **What This Tool Does:**
- Extracts metadata (author, title, year) from PDFs you own or have lawful access to
- Renames files for personal organization
- **Does NOT** extract or reproduce substantial content from PDFs
- **Does NOT** facilitate bulk processing of protected works without permission

**For full legal details, see [LEGAL_NOTICE.md](LEGAL_NOTICE.md)**

## Features

- Renames PDFs to `Author_Title(PublicationYear).pdf` format.
- Uses "UnknownAuthor", "UnknownTitle", or "UnknownYear" as placeholders if information is not found.
- Sanitizes filenames to remove invalid characters and replaces spaces with underscores.
- **OCR Support:** Automatically attempts OCR for PDFs where text extraction is poor or absent, enabling renaming of scanned documents.
- **Failed PDF Management:** Moves unprocessable PDFs to a "failed" subdirectory for manual review.

## Requirements

- Python 3.x
- `PyPDF2` library
- `pytesseract` library
- `pdf2image` library
- **Tesseract OCR Engine:** Required for OCR functionality.
- **Poppler:** Required by `pdf2image` to convert PDF pages to images.

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```
    (Once you create your GitHub repository, you'll replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual details.)

2.  **Install Python libraries:**
    ```bash
    pip install PyPDF2 pytesseract pdf2image
    ```

3.  **Install Tesseract OCR Engine:**
    Follow the instructions for your operating system:
    -   **macOS (Homebrew):** `brew install tesseract`
    -   **Windows:** Download from [Tesseract-OCR GitHub](https://tesseract-ocr.github.io/tessdoc/Downloads.html)
    -   **Linux:** `sudo apt-get install tesseract-ocr` (Debian/Ubuntu) or `sudo yum install tesseract` (RHEL/CentOS)
    
    *Note: You might need to set the `pytesseract.pytesseract.tesseract_cmd` variable in the script to the full path of your Tesseract executable if it's not in your system's PATH.*

4.  **Install Poppler:**
    Follow the instructions for your operating system:
    -   **macOS (Homebrew):** `brew install poppler`
    -   **Windows:** Download from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)
    -   **Linux:** `sudo apt-get install poppler-utils` (Debian/Ubuntu) or `sudo yum install poppler-utils` (RHEL/CentOS)

## Usage

1. **Place the `rename_pdfs.py` script in the directory containing your PDF files, or specify a directory path.**
2. **Open your terminal or command prompt.**
3. **Navigate to the directory where your PDFs and the script are located:**
    ```bash
    cd /path/to/your/pdf/folder
    ```
    (Replace `/path/to/your/pdf/folder` with the actual path to your PDF files.)

4. **Run the script:**
    ```bash
    # Rename PDFs in the current directory
    python3 rename_pdfs.py
    
    # Rename PDFs in a specific directory
    python3 rename_pdfs.py /path/to/your/pdf/folder
    ```

The script will scan for PDF files in the specified directory and attempt to rename them. Output messages will indicate which files were renamed or if any errors occurred.

## Important Notes

-   This script relies on the metadata embedded in the PDF files. If the metadata is incorrect or missing, the script will attempt to extract information from the text content. OCR is used as a fallback for scanned documents, but its accuracy can vary.
-   Some PDF files may be unreadable by `PyPDF2` or unprocessable by OCR due to their internal structure, encryption, or corruption, and the script will skip these files.
-   The script will not overwrite existing files with the same new name.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.