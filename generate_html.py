import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import time
from datetime import timezone
import pytz

# Load environment variables from .env file
load_dotenv()

def generate_combined_html(combined_summary, latest_blog_dates):
    # Generate a timestamp for the HTML content
    timestamp = time.strftime("%B %d, %Y, %I:%M %p")
    
    # Create the HTML content with inline styles and the provided summary and latest blog dates
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
                font-size: 2.5rem;
                margin-bottom: 1.5rem;
            }}
            h2 {{
                color: #ffcc00;
                font-size: 2rem;
                text-align: center;
                margin-bottom: 1rem;
            }}
            p {{
                font-size: 1.5rem; /* Increased size for blog text */
                margin-bottom: 1rem;
            }}
            #blog-posts-container {{
                max-height: 400px;
                width: 90%;
                overflow-y: scroll;
                padding: 20px;
                background-color: #000;
                border: 2px solid #33ff33;
                border-radius: 10px;
                box-shadow: 0 0 20px #33ff33;
                margin: 20px auto;
            }}
            .content {{
                margin-top: 20px;
                padding: 10px;
                line-height: 1.6;
            }}
            #latest-blogs-container {{
                margin-top: 40px;
                padding: 10px;
                text-align: center;
                color: #ffcc00; /* Yellow text */
            }}
            .latest-blog-item a {{
                color: #ffcc00; /* Yellow text for the links */
                font-size: 1.5rem; /* Match the font size with the rest */
                text-decoration: none;
                border: 1px dashed #33ff33; /* Pixelated border effect */
                padding: 5px;
                border-radius: 5px;
                margin: 0 10px;
            }}
            .latest-blog-item a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>Newsletter Summary for {timestamp}</h1>

        <!-- Sources Section -->
        <p>Sources: TLDR, Stocktwits, Google Dev Community</p>

        <div id="blog-posts-container">
    """

    # Split the combined summary into paragraphs and add each paragraph to the HTML content
    paragraphs = combined_summary.strip().split('\n\n')
    for para in paragraphs:
        if para.strip():
            html_content += f"<p>{para.strip()}</p>\n"

    html_content += "</div>\n"

    # Adding the recent blog section at the bottom of the HTML content
    html_content += '<div id="latest-blogs-container">\n'
    html_content += "<h2>Recent Blogs</h2>\n"
    for date, name in latest_blog_dates:
        html_content += f"<div class='latest-blog-item'><a href='{name}' target='_blank'>{date}</a></div>\n"

    html_content += """
        </div>
    </body>
    </html>
    """
    return html_content

# Improved get_latest_three_blog_dates function with timezone conversion
def get_latest_three_blog_dates():
    try:
        # Get the Azure Storage connection string from environment variables
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING_blogdb')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client('blogdb')

        # List all blobs in the container and sort them by last_modified (newest first)
        blobs = container_client.list_blobs()
        sorted_blobs = sorted(blobs, key=lambda b: b.last_modified, reverse=True)

        # Define your local timezone (example: US/Eastern)
        local_timezone = pytz.timezone('US/Eastern')

        blog_dates = []
        count = 0
        for blob in sorted_blobs:
            if count >= 3:
                break
            # Construct the URL for each blob
            blob_url = f"https://{container_client.account_name}.blob.core.windows.net/{container_client.container_name}/{blob.name}"
            
            # Convert UTC to local timezone
            blob_utc_time = blob.last_modified.replace(tzinfo=timezone.utc)
            blob_local_time = blob_utc_time.astimezone(local_timezone)
            formatted_date_str = blob_local_time.strftime("%B %d, %Y, %I:%M %p")

            # Append the formatted date and blob URL to the list
            blog_dates.append((formatted_date_str, blob_url))

        return blog_dates[:3]  # Return only the last three blogs if available

    except Exception as e:
        # Print error message if any exception occurs
        print(f"Error retrieving blog dates: {e}")
        return []

def archive_old_html(blob_service_client, source_container='$web', archive_container='blogdb'):
    try:
        # Get the blob client for the existing HTML file
        blob_client = blob_service_client.get_blob_client(container=source_container, blob='newsletter_summary.html')

        if blob_client.exists():
            # Create a timestamp for the archived file name
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            archive_blob_name = f'archive/newsletter_summary_{timestamp}.html'

            # Copy the existing file to the archive container with the new name
            archive_blob_client = blob_service_client.get_blob_client(container=archive_container, blob=archive_blob_name)
            copy = archive_blob_client.start_copy_from_url(blob_client.url)
            while copy['copy_status'] == 'pending':
                time.sleep(1)
                copy = archive_blob_client.get_blob_properties().copy
            print(f"Old file copied to '{archive_blob_name}'.")

    except Exception as e:
        # Print error message if any exception occurs
        print(f"Error archiving the old HTML file: {e}")

def delete_old_html(blob_service_client, source_container='$web'):
    try:
        # Get the blob client for the existing HTML file
        blob_client = blob_service_client.get_blob_client(container=source_container, blob='newsletter_summary.html')
        if blob_client.exists():
            # Delete the old HTML file
            blob_client.delete_blob()
            print(f"Old newsletter_summary.html deleted from '{source_container}'.")
    except Exception as e:
        # Print error message if any exception occurs
        print(f"Error deleting the old HTML file: {e}")

def upload_new_html(blob_service_client, html_content):
    try:
        # Upload the new HTML content to the '$web' container for public access
        source_container = '$web'
        blob_name = 'newsletter_summary.html'
        blob_client = blob_service_client.get_blob_client(container=source_container, blob=blob_name)
        blob_client.upload_blob(html_content, overwrite=True, content_type='text/html')
        print(f"New HTML output uploaded to Azure Blob Storage in container '{source_container}' as '{blob_name}'.")
    except Exception as e:
        # Print error message if any exception occurs
        print(f"Error uploading to Blob Storage: {e}")

def save_html_output(html_content):
    try:
        # Get the Azure Storage connection strings from environment variables
        blogdb_connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING_blogdb')
        podfunction_connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING_podfunction')
        if not blogdb_connect_str or not podfunction_connect_str:
            print("Azure Storage connection string(s) not found.")
            return

        # Create BlobServiceClient instances for both storage accounts
        blogdb_blob_service_client = BlobServiceClient.from_connection_string(blogdb_connect_str)
        podfunction_blob_service_client = BlobServiceClient.from_connection_string(podfunction_connect_str)

        # Step 1: Delete the old HTML file from '$web'
        delete_old_html(blogdb_blob_service_client, source_container='$web')

        # Step 2: Upload the new HTML to the '$web' container
        upload_new_html(blogdb_blob_service_client, html_content)

        # Step 3: Upload the new HTML content to the 'pod-prep' container in the podfunction storage account
        pod_prep_container = 'pod-prep'
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        pod_prep_blob_name = f'newsletter_summary_{timestamp}.html'
        pod_prep_client = podfunction_blob_service_client.get_blob_client(container=pod_prep_container, blob=pod_prep_blob_name)
        pod_prep_client.upload_blob(html_content, overwrite=True, content_type='text/html')
        print(f"New HTML output also uploaded to Azure Blob Storage in container '{pod_prep_container}' as '{pod_prep_blob_name}'.")

    except Exception as e:
        # Print error message if any exception occurs
        print(f"Error processing HTML file: {e}")


