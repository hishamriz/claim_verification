from typing import Dict, Union
import PyPDF2
import logging
from pathlib import Path
import os
import sys

class PDFParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO,
                          format='%(message)s')  # Simplified logging format
        
    def validate_file(self, pdf_path: Union[str, Path]) -> bool:
        """Validate if file exists and is a PDF"""
        path = Path(pdf_path)
        if not path.exists():
            self.logger.error(f"\nError: File does not exist: {pdf_path}")
            return False
        if path.suffix.lower() != '.pdf':
            self.logger.error(f"\nError: File is not a PDF: {pdf_path}")
            return False
        return True

    def parse_pdf(self, pdf_path: Union[str, Path]) -> Dict:
        """Parse PDF file and extract text and metadata"""
        if not self.validate_file(pdf_path):
            return {
                'text': '',
                'metadata': {},
                'pages': 0,
                'success': False,
                'error': 'Invalid file or file not found'
            }

        try:
            print("\nParsing PDF... Please wait.")
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                metadata = reader.metadata or {}
                text_content = []
                total_pages = len(reader.pages)
                
                print(f"\nFound {total_pages} pages.")
                
                for page_num, page in enumerate(reader.pages, 1):
                    print(f"Processing page {page_num}/{total_pages}")
                    text = page.extract_text()
                    text_content.append(text)
                
                return {
                    'text': '\n'.join(text_content),
                    'metadata': metadata,
                    'pages': total_pages,
                    'success': True
                }
                
        except Exception as e:
            self.logger.error(f"\nError parsing PDF: {str(e)}")
            return {
                'text': '',
                'metadata': {},
                'pages': 0,
                'success': False,
                'error': str(e)
            }

def get_pdf_path() -> str:
    """Prompt user for PDF file path and validate input"""
    while True:
        print("\nPlease enter the path to your PDF file.")
        print("You can:")
        print("1. Enter the full path (e.g., /Users/username/Documents/file.pdf)")
        print("2. Drag and drop the PDF file into this terminal")
        print("3. Type 'exit' to quit")
        
        file_path = input("\nPDF path: ").strip()
        
        # Handle quotes if file was dragged into terminal
        file_path = file_path.strip("'\"")
        
        if file_path.lower() == 'exit':
            sys.exit(0)
            
        # Convert relative path to absolute path
        file_path = os.path.expanduser(file_path)  # Handle ~
        file_path = os.path.abspath(file_path)     # Convert to absolute path
            
        return file_path

def display_text(text: str, pages: int):
    """Display extracted text with pagination"""
    if not text.strip():
        print("\nNo text could be extracted from the PDF.")
        return

    lines = text.split('\n')
    page_size = 20  # lines per page
    total_lines = len(lines)
    
    current_line = 0
    while current_line < total_lines:
        # Clear screen (works on both Windows and Unix)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display current page
        print("\n=== Extracted Text ===")
        for line in lines[current_line:current_line + page_size]:
            print(line)
            
        # Navigation prompt
        print("\n=== Navigation ===")
        print("Press:")
        print("n - Next page")
        print("p - Previous page")
        print("q - Quit")
        
        choice = input("\nChoice: ").lower()
        
        if choice == 'n':
            current_line = min(current_line + page_size, total_lines - 1)
        elif choice == 'p':
            current_line = max(0, current_line - page_size)
        elif choice == 'q':
            break

def main():
    parser = PDFParser()
    
    while True:
        try:
            # Get PDF path from user
            pdf_path = get_pdf_path()
            
            # Parse PDF
            result = parser.parse_pdf(pdf_path)
            
            if result['success']:
                print("\nPDF parsed successfully!")
                
                # Display metadata if available
                if result['metadata']:
                    print("\n=== Metadata ===")
                    for key, value in result['metadata'].items():
                        print(f"{key}: {value}")
                
                # Display text with pagination
                display_text(result['text'], result['pages'])
                
                # Ask if user wants to process another PDF
                if input("\nProcess another PDF? (y/n): ").lower() != 'y':
                    break
            else:
                print(f"\nFailed to parse PDF: {result.get('error', 'Unknown error')}")
                if input("\nTry another PDF? (y/n): ").lower() != 'y':
                    break
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            if input("\nTry again? (y/n): ").lower() != 'y':
                break

if __name__ == "__main__":
    main()