

import os
import re
from PyPDF2 import PdfReader

def sanitize_filename(filename):
    """
    Removes invalid characters from a filename and replaces spaces with underscores.
    """
    if not filename:
        return ""
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove any characters that are not alphanumeric, an underscore, a hyphen, or a period.
    filename = re.sub(r'[^\[\]\w._()-]', '', filename) # Added parentheses for year
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
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            # Read first few pages to get enough text for extraction
            for i in range(min(3, len(pdf_reader.pages))):
                text += pdf_reader.pages[i].extract_text() or ""
    except Exception as e:
        print(f"Error reading text from {pdf_path}: {e}")
        return "UnknownAuthor", "UnknownTitle", "UnknownYear"

    # Normalize whitespace for easier regex matching
    text = re.sub(r'\s+', ' ', text).strip()

    # Regex for Title (often at the beginning, bold, or large font - hard to capture reliably with regex alone)
    # This is a very basic attempt and might need refinement based on common paper formats.
    # For now, let's try to find a prominent line that looks like a title.
    # This is highly heuristic and might not work for all papers.
    title_match = re.search(r'\n\s*([A-Z][A-Za-z0-9\s,-:]+?)\s*\n', text)
    title = title_match.group(1).strip() if title_match else "UnknownTitle"
    # Further refine title to remove common headers/footers if they get caught
    if len(title) > 100 or "Journal of" in title or "Psychology" in title: # Heuristic to avoid journal names
        title = "UnknownTitle"


    # Regex for Author (often "First Last, First Last" or "First Last and First Last")
    # This is also heuristic. Looking for common patterns like "by Author Names" or just names.
    author_match = re.search(r'(?:by|By)\s+([A-Z][a-zA-Z\s.,-]+(?:and\s+[A-Z][a-zA-Z\s.,-]+)*)', text)
    if not author_match:
        author_match = re.search(r'([A-Z][a-zA-Z\s.,-]+(?:,\s*[A-Z][a-zA-Z\s.,-]+)*)', text)
    
    author = author_match.group(1).strip() if author_match else "UnknownAuthor"
    # Simple heuristic to avoid capturing too much text as author
    if len(author.split()) > 10: # More than 10 words, likely not just authors
        author = "UnknownAuthor"
    
    # Regex for Year (common patterns like "YYYY", "(YYYY)", "YYYYa")
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    year = year_match.group(0) if year_match else "UnknownYear"

    return author, title, year

def rename_pdfs_in_directory(directory_path):
    """
    Renames all PDF files in a given directory based on their metadata or text content.
    """
    print(f"Scanning for PDF files in: {directory_path}")
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            old_filepath = os.path.join(directory_path, filename)
            
            author = "UnknownAuthor"
            title = "UnknownTitle"
            year = "UnknownYear"

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

                new_filename_base = f"{first_author_lastname}_{title}({year})"
                new_filename = sanitize_filename(new_filename_base)
                
                # To avoid overly long filenames, truncate if necessary
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

            except Exception as e:
                print(f"Could not process '{filename}': {e}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    rename_pdfs_in_directory(current_directory)
