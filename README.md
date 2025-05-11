# Email Extractor

A web application that extracts email addresses from websites by crawling multiple pages within the same domain.

![Email Extractor Screenshot](https://github.com/user-attachments/assets/1e3d3de3-0d5b-43f9-8d2c-9c6ce4ff40dd)

## 🌟 Features

- **Website Crawling**: Extracts emails from an entire website, not just a single page
- **Email Detection**: Finds emails in both visible text and mailto links
- **User-Friendly Interface**: Clean, responsive design that works on desktop and mobile
- **Advanced Settings**: Control how many pages to crawl
- **Results Management**: Copy individual emails, copy all emails, or download as CSV
- **Error Handling**: Clear error messages and timeout handling

## 🚀 Live Demo

The application is deployed and available at: [emails-extractor.onrender.com](https://emails-extractor.onrender.com)

## 🛠️ Technologies Used

### Backend
- **Python 3.9+**
- **Flask**: Web framework
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP requests
- **Flask-CORS**: Cross-Origin Resource Sharing

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript** (Vanilla, no frameworks)
- **Font Awesome**: Icons

### Deployment
- **Render**: Cloud hosting platform
- **Gunicorn**: WSGI HTTP Server

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

## ⚙️ Installation

1. **Clone the repository** (or download the ZIP file):
   ```bash
   git clone https://github.com/yourusername/email-extractor.git
   cd email-extractor
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

### Local Development

1. **Start the Flask server**:
   ```bash
   python server/app.py
   ```

2. **Access the application**:
   Open your web browser and navigate to:
   ```
   http://localhost:5000/
   ```

### Production Deployment

For production deployment on Render:

1. **Push your code to GitHub**
2. **Create a new Web Service on Render**:
   - Connect your GitHub repository
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn wsgi:app`
   - Choose the free plan

## 📝 How to Use

1. **Enter a website URL** in the input field (include http:// or https://)
2. **Adjust settings** (optional):
   - Click the gear icon to access advanced settings
   - Set the maximum number of pages to crawl (default: 10, max: 20)
3. **Click "Extract Emails"** to start the process
4. **View the results**:
   - See the number of emails found and pages crawled
   - Copy individual emails by clicking the copy icon
   - Use "Copy All" to copy all emails to clipboard
   - Use "Download CSV" to download emails as a CSV file

## 🧩 Project Structure

```
email-extractor/
├── client/                  # Frontend files
│   ├── index.html           # Main HTML file
│   ├── styles.css           # CSS styles
│   └── script.js            # JavaScript functionality
├── server/                  # Backend files
│   ├── app.py               # Flask application
│   ├── utils.py             # Utility functions for email extraction
│   └── requirements.txt     # Server dependencies
├── .gitignore               # Git ignore file
├── Procfile                 # For Render deployment
├── README.md                # Project documentation
├── requirements.txt         # Root-level dependencies
└── wsgi.py                  # WSGI entry point
```

## ⚠️ Limitations

- The free tier on Render has limited resources, so crawling large websites may time out
- Maximum of 20 pages can be crawled to prevent timeouts
- The application respects robots.txt implicitly through the requests library
- Free tier on Render may spin down after periods of inactivity, causing the first request to take longer

## 🔍 How It Works

1. **User submits a URL**: The application receives the URL and optional settings
2. **Server crawls the website**:
   - Starts at the provided URL
   - Extracts emails from the page
   - Finds links to other pages on the same domain
   - Visits those pages and repeats the process
   - Continues until all pages are visited or the maximum limit is reached
3. **Server returns results**: The extracted emails and metadata are sent back to the client
4. **Client displays the results**: The emails are displayed in a list with copy options

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

Your Name - [ranjankumarpandit92054@gmail.com](mailto:ranjankumarpandit92054@gmail.com)

Project Link: [https://github.com/Ranj8521Kumar/Emails-Extractor/](https://github.com/Ranj8521Kumar/Emails-Extractor/)

---

Made with ❤️ by Ranjan
