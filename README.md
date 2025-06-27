# PDF Renamer

This Python script helps you batch rename PDF files in a directory based on their metadata (author, title, and publication year). If metadata is missing, it attempts to extract the year from the text content of the first page.

## Features

- Renames PDFs to `Author_Title(PublicationYear).pdf` format.
- Uses "UnknownAuthor", "UnknownTitle", or "UnknownYear" as placeholders if information is not found.
- Sanitizes filenames to remove invalid characters and replaces spaces with underscores.

## Requirements

- Python 3.x
- `PyPDF2` library

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```
    (Once you create your GitHub repository, you'll replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual details.)

2.  **Install the required Python library:**
    ```bash
    pip install PyPDF2
    ```

## Usage

1.  **Place the `rename_pdfs.py` script in the directory containing your PDF files.**
2.  **Open your terminal or command prompt.**
3.  **Navigate to the directory where your PDFs and the script are located:**
    ```bash
    cd /path/to/your/pdf/folder
    ```
    (Replace `/path/to/your/pdf/folder` with the actual path to your PDF files.)

4.  **Run the script:**
    ```bash
    python3 rename_pdfs.py
    ```

The script will scan for PDF files in the current directory and attempt to rename them. Output messages will indicate which files were renamed or if any errors occurred.

## Important Notes

-   This script relies on the metadata embedded in the PDF files. If the metadata is incorrect or missing, the script will attempt to extract information from the text content of the first page, but this is not always reliable.
-   Some PDF files may be unreadable by `PyPDF2` due to their internal structure or corruption, and the script will skip these files.
-   The script will not overwrite existing files with the same new name.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests!

## License

[Choose a license, e.g., MIT, Apache 2.0, etc. and add it here.]
