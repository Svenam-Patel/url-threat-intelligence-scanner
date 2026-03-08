# URL Threat Intelligence Scanner

A web-based tool that analyzes suspicious URLs using heuristic security checks.  
It evaluates URLs for phishing indicators such as insecure HTTP usage, suspicious keywords, abnormal URL length, and redirect behavior.

## Features

- URL threat analysis using heuristic rules
- Detects phishing keywords in URLs
- Identifies insecure HTTP connections
- Maintains scan history of analyzed URLs
- Displays risk score and status (Safe / Suspicious)

## Tech Stack

Frontend: React  
Backend: Flask  
Database: SQLite  

## How to Run

Backend

cd backend  
pip install flask flask-cors requests  
python app.py  

Frontend

cd frontend  
npm install  
npm start  

## Future Enhancements

- Integration with threat intelligence APIs
- Burp Suite based request/response analysis
- Machine learning based phishing detection
- Advanced threat visualization dashboard
