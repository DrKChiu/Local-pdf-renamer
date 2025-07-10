import os
import re
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

import pytesseract
from pdf2image import convert_from_path
from PIL import Image # Required by pdf2image and pytesseract

# Set the path to the Tesseract executable if it's not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract' # Example for macOS Homebrew
# You might need to uncomment and adjust this line if you get a TesseractNotFoundError


def sanitize_filename(filename):
    """
    Removes invalid characters from a filename and replaces spaces with underscores.
    """
    if not filename:
        return ""
    # Remove any characters that are not alphanumeric, an underscore, a hyphen, a period, or a space.
    # We keep spaces here, and handle underscore replacement separately for the title part.
    filename = re.sub(r'[^\w\s.-]', '_', filename)
    filename = re.sub(r'_+', '_', filename).strip('_')
    return filename

def get_first_author_from_string(author_string):
    """
    Extracts the first author's last name from an author string.
    Handles various formats like "Last, First", "First Last", "First M. Last", "Last, F. M."
    """
    if not author_string:
        return "UnknownAuthor"
    
    # Try to split by common author separators
    authors = re.split(r'[,;]', author_string)
    if not authors:
        return "UnknownAuthor"
    
    first_author = authors[0].strip()
    
    # Handle "Last, First" format
    if ',' in first_author:
        parts = first_author.split(',')
        if len(parts) > 0:
            return parts[0].strip() # Return the last name
    
    # Handle "First Last" or "First M. Last" format
    parts = first_author.split()
    if len(parts) > 0:
        return parts[-1].strip() # Return the last name

    return "UnknownAuthor"

def extract_info_from_text(pdf_path):
    """
    Extracts author, title, and year from the text content of the first few pages.
    Tries PyPDF2 first, then falls back to OCR if text extraction is poor.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            # Read first few pages to get enough text for extraction
            for i in range(min(3, len(pdf_reader.pages))):
                text += pdf_reader.pages[i].extract_text() or ""
    except Exception as e:
        print(f"Error reading text from {pdf_path} with PyPDF2: {e}")
        # Fall through to OCR attempt

    # If PyPDF2 extracted little or no text, try OCR
    if len(text.strip()) < 50: # Heuristic: if less than 50 characters, try OCR
        print(f"PyPDF2 extracted insufficient text from {pdf_path}. Attempting OCR...")
        try:
            # Convert first page to image
            images = convert_from_path(pdf_path, first_page=1, last_page=1)
            if images:
                # Perform OCR on the image
                ocr_text = pytesseract.image_to_string(images[0])
                text = ocr_text # Use OCR text for extraction
                print(f"OCR successful for {pdf_path}. Extracted {len(text.strip())} characters.")
            else:
                print(f"Could not convert {pdf_path} to image for OCR.")
        except pytesseract.TesseractNotFoundError:
            print("Tesseract is not installed or not in your PATH. Please install it.")
            print("See: https://tesseract-ocr.github.io/tessdoc/Installation.html")
            return "UnknownAuthor", "UnknownTitle", "UnknownYear"
        except Exception as e:
            print(f"Error during OCR for {pdf_path}: {e}")
            return "UnknownAuthor", "UnknownTitle", "UnknownYear"

    if not text.strip():
        print(f"No text extracted from {pdf_path} even after OCR. Cannot rename.")
        return "UnknownAuthor", "UnknownTitle", "UnknownYear"

    # Normalize whitespace for easier regex matching
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"--- Extracted Text (first 500 chars):\n{text[:500]}\n---")

    # Improved title extraction - look for common academic paper title patterns
    title = "UnknownTitle"
    
    # Try multiple patterns to find title
    title_patterns = [
        r'^\s*([A-Z][^\n]{10,200})\s*\n',  # Standalone capitalized line at the beginning
        r'(?i)title[:\s]*([A-Z][^\n]{10,200})',  # "Title:" followed by text
        r'(?i)^\s*([A-Z][A-Za-z\s\-:,\.]{20,200})\s*(?=\n[A-Z][a-z])',  # Title before author line
        r'^\s*([A-Z][A-Za-z\s\-:,\.]{10,200})\s*\n\s*(?:by|By|AUTHOR|Author)', # Title followed by 'by' or 'author'
    ]
    
    for pattern in title_patterns:
        title_match = re.search(pattern, text, re.MULTILINE)
        if title_match:
            potential_title = title_match.group(1).strip()
            # Filter out common false positives and ensure reasonable length
            if (len(potential_title) >= 10 and len(potential_title) <= 200 and 
                not any(word in potential_title.lower() for word in ['journal of', 'proceedings', 'copyright', 'abstract', 'introduction', 'university', 'downloaded', 'review', 'article', 'report'])):
                title = potential_title
                break

    # Improved author extraction
    author = "UnknownAuthor"
    
    # Try multiple patterns to find authors
    author_patterns = [
        r'(?i)by\s+([A-Z][A-Za-z\s\.,-]+(?:(?:\s+and|,)\s*[A-Z][A-Za-z\s\.,-]+)*)',  # "By" followed by names
        r'(?i)authors?:\s*([A-Z][^\n]{5,200})',  # "Author(s):" followed by names
        r'([A-Z][a-z]+(?:\s+[A-Z]\.)?\s+[A-Z][a-z]+(?:,\s*[A-Z][a-z]+(?:\s+[A-Z]\.)?\s+[A-Z][a-z]+)*)',  # Name patterns
        r'([A-Z][a-z]+,\s*[A-Z]\.[^\n]{0,50})',  # "LastName, F." format
        r'([A-Z][a-z]+(?:\s+[A-Z]\.)?\s+[A-Z][a-z]+)', # First Last or First M. Last
    ]
    
    for pattern in author_patterns:
        author_match = re.search(pattern, text, re.MULTILINE)
        if author_match:
            potential_author = author_match.group(1).strip()
            # Filter based on reasonable author name criteria
            words = potential_author.split()
            if (len(words) >= 2 and len(words) <= 10 and 
                not any(word.lower() in potential_author.lower() for word in ['university', 'department', 'journal', 'abstract', 'copyright'])):
                author = potential_author
                break
    
    # Improved year extraction - prioritize more recent years and common formats
    year = "UnknownYear"
    
    # Look for years in parentheses first (common in citations), then standalone years
    year_patterns = [
        r'\b(19|20)\d{2}\b',  # General YYYY format
        r'\((19|20)\d{2}\)',  # (YYYY) format
    ]
    
    for pattern in year_patterns:
        year_matches = re.findall(pattern, text)
        if year_matches:
            # Take the most recent year found
            years = [int(match) if isinstance(match, str) else int(match[0]) for match in year_matches]
            year = str(max(years))
            break

    print(f"--- Extracted Info: Author='{author}', Title='{title}', Year='{year}' ---")
    return author, title, year

def rename_pdfs_in_directory(directory_path):
    """
    Renames all PDF files in a given directory based on their metadata or text content.
    """
    print(f"Scanning for PDF files in: {directory_path}")
    pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
    total_pdfs = len(pdf_files)
    failed_pdfs = 0

    for filename in pdf_files:
        if filename.lower().endswith('.pdf'):
            old_filepath = os.path.join(directory_path, filename)
            
            author = "UnknownAuthor"
            title = "UnknownTitle"
            year = "UnknownYear"
            processed_successfully = False

            try:
                with open(old_filepath, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    metadata = pdf_reader.metadata

                    # Try to get from metadata first
                    if metadata:
                        if metadata.author:
                            author = metadata.author
                        if metadata.title:
                            title = metadata.title
                        if metadata.creation_date:
                            year = str(metadata.creation_date.year)
                        elif metadata.mod_date:
                            year = str(metadata.mod_date.year)

                # Fallback to text content if metadata is missing or generic
                if author == "UnknownAuthor" or title == "UnknownTitle" or year == "UnknownYear":
                    extracted_author, extracted_title, extracted_year = extract_info_from_text(old_filepath)
                    if author == "UnknownAuthor":
                        author = extracted_author
                    if title == "UnknownTitle":
                        title = extracted_title
                    if year == "UnknownYear":
                        year = extracted_year

                first_author_lastname = get_first_author_from_string(author)

                # Truncate title to 15 words
                title_words = title.split()
                brief_title = " ".join(title_words[:15])

                brief_title_underscored = brief_title

                # Construct new filename base: FirstAuthorSurname (PublicationYear) brief_title
                new_filename_base = f"{first_author_lastname} ({year}) {brief_title_underscored}"
                new_filename = sanitize_filename(new_filename_base)
                
                # To avoid overly long filenames, truncate if necessary (after sanitization)
                if len(new_filename) > 150:
                    new_filename = new_filename[:150]

                new_filename += ".pdf"
                new_filepath = os.path.join(directory_path, new_filename)

                # Ensure the new filename doesn't already exist
                if os.path.exists(new_filepath) and new_filepath != old_filepath:
                    print(f'Skipping rename for "{filename}" as "{new_filename}" already exists.')
                    continue

                os.rename(old_filepath, new_filepath)
                print(f'Renamed "{filename}" to "{new_filename}"')
                processed_successfully = True

            except PdfReadError as e:
                print(f"Could not read PDF content for '{filename}' (possibly corrupted or encrypted): {e}")
            except Exception as e:
                print(f"Could not process '{filename}': {e}")
            
            if not processed_successfully:
                failed_pdfs += 1

    if total_pdfs > 0:
        failure_percentage = (failed_pdfs / total_pdfs) * 100
        print(f"Failed to process {failed_pdfs} out of {total_pdfs} PDFs ({failure_percentage:.2f}% failure rate).")


if __name__ == "__main__":
    # Use the specific directory path provided by the user
    articles_directory = "/Users/kc/Desktop/2025 MRC and NIHR fellowship application/Articles"
    
    if not os.path.exists(articles_directory):
        print(f"Articles directory not found at: {articles_directory}")
        exit(1)
    
    print(f"Processing PDFs in Articles directory: {articles_directory}")
    rename_pdfs_in_directory(articles_directory)

print("PDF renaming process complete!")