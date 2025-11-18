---

# 📝 **AI-Powered Blog Automation** 📝

### 🚀 **Project Overview**
Welcome to the AI-Powered Blog Automation tool! This project is a fully automated system that pulls newsletters via Gmail, processes them using OpenAI for a customizable tone, and updates your website with fresh blog content—all seamlessly integrated with Azure Blob Storage. 

For a live demonstration of this automation in action, visit **[my website](https://eportkc.com)**, where content is continuously updated, archived, and displayed with the help of a simple cron job. Explore and see how it’s possible to maintain an engaging, hands-free blogging experience!

### 🎯 **Key Features**
- **Email Automation**: Securely fetches content using the Gmail API with OAuth 2.0.
- **AI Content Generation**: Utilizes OpenAI to create customizable, engaging blog content.
- **Instant Website Updates**: Stores and displays generated content through Azure Blob Storage for real-time website updates.
- **Podcast Preparation**: Sends blog data to a designated "pod-prep" directory after each blog update cycle, facilitating future podcast creation.
- **Customizable Sources & Tone**: Adjust the content source and the AI’s tone to refresh your content in minutes.
- **Retro-Style HTML**: Generated content features vintage-style formatting for a unique look.

### ⚙️ **Setup & Installation**
#### **Pre-requisites**:
- Python 3.x installed
- Azure Blob Storage account configured
- Gmail API with OAuth set up
- OpenAI API key or chosen API key for content generation

#### **Installation Steps**:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Fruitloop24/blog-server.git
   ```
2. **Set Up a Virtual Environment**:
   - Navigate to the project directory:
     ```bash
     cd blog-server
     ```
   - Create a virtual environment to avoid installing packages globally:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
3. **Install Dependencies**:
   - With the virtual environment activated, install the required packages:
     ```bash
     pip install -r requirements.txt
     ```
4. **Configure Environment Variables**:
   - Create a `.env` file and add the following:
     ```bash
     AZURE_STORAGE_CONNECTION_STRING_blogdb=<your_connection_string>
     AZURE_STORAGE_CONNECTION_STRING_podfunction=<your_connection_string>
     OPENAI_API_KEY=<your_openai_api_key>
     GMAIL_API_KEY=<your_gmail_api_key>
     ```

#### **Gmail API Setup**:
- Follow the [Gmail API guide](https://developers.google.com/gmail/api/quickstart/python) for detailed instructions on setting up OAuth credentials.

### 🛠️ **Running the Tool**
After completing the setup, you're ready to start using the tool! Just run:
```bash
python main.py
```
And you’re in business, baby! 🎉

### 📝 **Customization Options**
- **Changing Content Sources**:  
   In `fetch_newsletters.py`, you can easily modify the content sources by adding or removing newsletter subscriptions. We recommend signing up for free, high-quality newsletters that deliver fresh content regularly. This removes the need for web scraping and provides a steady stream of great material.
- **Customizing AI Tone & Intensity**:  
   For personalized content, adjust the tone and intensity of the blog generation in `generate_synopsis.py`. This file allows you to modify the AI’s "persona" or style, so you can get creative with the blog’s voice.

### 🔐 **Security Considerations**
- Ensure your `.env` file is secure and excluded from version control (already covered in your `.gitignore`).
- Use OAuth for secure Gmail API access.
- Keep your connection strings safe and encrypted if possible.

### 🖼️ **Azure Blob Storage & Podcast Integration**
This tool leverages **Azure Blob Storage** for both real-time blog display and structured storage of content for future audio production:
- **Blog Display**: The HTML content is stored in the `$web` container, enabling seamless embedding into your site using:
   ```html
   <iframe src="https://<your-storage-account>.blob.core.windows.net/$web/newsletter_summary.html" width="100%" height="800px"></iframe>
   ```
- **Podcast Preparation**: After each blog generation cycle, content is automatically sent to a `pod-prep` directory in a separate container (`podfunction`). This prepares the content for podcast creation, allowing you to easily add audio or voice synthesis in future updates.

### 💡 **Future Enhancements**
- **Google Notebook LLM**: Currently used for generating conversational scripts with two-person roles. Although no API is available yet, it’s on the horizon and will seamlessly integrate when ready.
- **Azure Speech Services**: Could be incorporated for automatic voice synthesis, turning written content into spoken word for a fully automated podcast workflow.

Azure’s **Blob Storage** and **Static Web Apps** provide an efficient and scalable solution for hosting, updating, and presenting dynamic content—perfect for projects aiming for both automation and reliability.

---

For a live showcase of this project in action, visit **[my e-portfolio](https://eportkc.com)** or contact me for collaboration and I'm actively pursueing new roles!!

---
heyyyy 
