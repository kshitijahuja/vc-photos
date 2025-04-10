"""
====================================================================================
 Author        : Kshitij Ahuja 
 Description   : This script read the supplied CSV containing Veracross person_id 
                    and corresponding photo URIs and downloads those files in the 
                    specified directory. 
====================================================================================
 For any queries or contributions, contact: kahuja@academicdatasolutions.com
====================================================================================
"""

# -------- HARDCODED VARIABLES (MODIFY THESE) --------
CSV_FILE_PATH = "source_file.csv"  # Path to your CSV file
DOWNLOAD_FOLDER = "downloads"    # Folder where photos will be downloaded
URL_COLUMN_NAME = "person_photo"    # Name of the column containing photo URLs
# ----------------------------------------------------

import os
import csv
import requests
from urllib.parse import urlparse
from pathlib import Path

def download_photos_from_csv():
    """
    Download photos from URLs found in a specified column of a CSV file.
    """
    # Create downloads folder if it doesn't exist
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
        print(f"Created directory: {DOWNLOAD_FOLDER}")
    
    # Read the CSV file
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames
            
            if not headers:
                print("Error: CSV file is empty or has no headers.")
                return
            
            # Check if the specified column exists
            if URL_COLUMN_NAME not in headers:
                print(f"Error: Column '{URL_COLUMN_NAME}' not found in CSV.")
                print(f"Available columns: {headers}")
                return
            
            print(f"Using column '{URL_COLUMN_NAME}' for photo URLs")
            
            # Process each row and download photos
            total_rows = 0
            successful_downloads = 0
            failed_downloads = 0
            
            for i, row in enumerate(reader):
                total_rows += 1
                url = row[URL_COLUMN_NAME].strip()
                
                if not url:
                    print(f"Row {i+2}: Empty URL, skipping.")
                    continue
                    
                try:
                    # Generate filename from URL or row index
                    parsed_url = urlparse(url)
                    path_parts = Path(parsed_url.path).parts
                    if path_parts:
                        filename = path_parts[-1]
                        # If filename doesn't have extension, add .jpg
                        if not Path(filename).suffix:
                            filename = f"{filename}.jpg"
                    else:
                        # Fallback filename
                        filename = f"photo_{i+1}.jpg"
                    
                    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                    
                    # Download the image with authentication key preserved in URL
                    print(f"Downloading: {url} -> {file_path}")
                    response = requests.get(url, stream=True, timeout=30)
                    response.raise_for_status()
                    
                    # Save the image
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    successful_downloads += 1
                    print(f"Successfully downloaded to {file_path}")
                    
                except requests.exceptions.RequestException as e:
                    failed_downloads += 1
                    print(f"Failed to download from row {i+2}: {e}")
                except Exception as e:
                    failed_downloads += 1
                    print(f"Error processing row {i+2}: {e}")
        
        print(f"\nDownload Summary:")
        print(f"Total rows processed: {total_rows}")
        print(f"Successful downloads: {successful_downloads}")
        print(f"Failed downloads: {failed_downloads}")
    
    except FileNotFoundError:
        print(f"Error: CSV file '{CSV_FILE_PATH}' not found.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    print("Starting photo download process...")
    print(f"CSV File: {CSV_FILE_PATH}")
    print(f"URL Column: {URL_COLUMN_NAME}")
    print(f"Download Folder: {DOWNLOAD_FOLDER}")
    print("-" * 50)
    download_photos_from_csv()