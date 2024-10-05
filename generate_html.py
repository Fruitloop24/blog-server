import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

def generate_combined_html(combined_summary):
    timestamp = time.strftime("%B %d, %Y, %I:%M %p")
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daily Newsletter Summary - {timestamp}</title>
        <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: #000000;
                color: #33ff33;
                font-family: 'VT323', monospace;
                margin: 20px;
            }}
            h1 {{
                text-align: center;
                color: #ffcc00;
                font-size: 4rem;
                margin-bottom: 2rem;
            }}
            p {{
                font-size: 1.5rem;
                margin-bottom: 1.5rem;
            }}
            #blog-posts-container {{
                max-height: 500px;
                width: 90%;
                overflow-y: scroll;
                padding: 20px;
                background-color: #000;
                border: 2px solid #33ff33;
                border-radius: 10px;
                box-shadow: 0 0 20px #33ff33;
                margin: 20px auto;
            }}
            .highlight {{
                color: #ffcc00; /* Highlight important text */
                font-weight: bold;
            }}
            .content {{
                margin-top: 40px;
                padding: 10px;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <h1>Newsletter Summary for {timestamp}</h1>
        <div id="blog-posts-container">
    """

    paragraphs = combined_summary.strip().split('\n\n')
    for para in paragraphs:
        if para.strip():
            html_content += f"<p>{para.strip()}</p>\n"

    html_content += """
        </div>
    </body>
    </html>
    """
    return html_content

# Archive the old file (move it from $web to blogdb)
def archive_old_html(blob_service_client, source_container='$web', archive_container='blogdb'):
    try:
        blob_client = blob_service_client.get_blob_client(container=source_container, blob='newsletter_summary.html')

        # Check if the file exists before archiving
        if blob_client.exists():
            # Create a timestamp for the archive
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            archive_blob_name = f'archive/newsletter_summary_{timestamp}.html'

            # Copy the old file to the archive
            archive_blob_client = blob_service_client.get_blob_client(container=archive_container, blob=archive_blob_name)
            archive_blob_client.start_copy_from_url(blob_client.url)
            print(f"Old file copied to '{archive_container}/{archive_blob_name}'.")

    except Exception as e:
        print(f"Error archiving the old HTML file: {e}")

# Delete the old file from $web
def delete_old_html(blob_service_client, source_container='$web'):
    try:
        blob_client = blob_service_client.get_blob_client(container=source_container, blob='newsletter_summary.html')

        # Check if the file exists before deleting
        if blob_client.exists():
            blob_client.delete_blob()
            print(f"Old newsletter_summary.html deleted from '{source_container}'.")

    except Exception as e:
        print(f"Error deleting the old HTML file: {e}")

# Upload the new HTML file to $web after generating the content
def upload_new_html(blob_service_client, html_content):
    try:
        source_container = '$web'

        # Now upload the new file to the $web container
        blob_name = 'newsletter_summary.html'
        blob_client = blob_service_client.get_blob_client(container=source_container, blob=blob_name)
        blob_client.upload_blob(html_content, overwrite=True, content_type='text/html')
        print(f"New HTML output uploaded to Azure Blob Storage in container '{source_container}' as '{blob_name}'.")

    except Exception as e:
        print(f"Error uploading to Blob Storage: {e}")

def save_html_output(html_content):
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not connect_str:
            print("Azure Storage connection string not found.")
            return

        # Establish the connection
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Archive, delete, and upload -- ALL happen only at the END of the script
        archive_old_html(blob_service_client, source_container='$web', archive_container='blogdb')
        delete_old_html(blob_service_client, source_container='$web')
        upload_new_html(blob_service_client, html_content)

    except Exception as e:
        print(f"Error processing HTML file: {e}")

if __name__ == "__main__":
    # Example usage
    combined_summary = "Your newsletter content goes here."
    html_content = generate_combined_html(combined_summary)
    
    # All actions happen at the end
    save_html_output(html_content)