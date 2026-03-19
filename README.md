# URL Threat Intelligence Platform

A full-stack web application that analyzes URLs for potential phishing and malicious indicators using a multi-layer rule-based detection system.

The system evaluates URLs using lexical analysis, pattern recognition, and domain validation techniques to identify suspicious behavior.

## Features

- Heuristic-based URL threat detection
- Detection of typosquatting domains (e.g., g00gle, rnicrosoft)
- Identifies insecure HTTP usage
- Detects phishing keywords (login, verify, secure, bank)
- Pattern-based detection:
  - Character substitution (0 → o, 1 → l)
  - Repeated characters
  - Visual spoofing patterns (rn, vv)
  - Hyphen abuse and long domain names
- DNS-based domain validation (checks if domain resolves)
- Risk scoring system (Safe / Suspicious classification)
- Scan history storage using SQLite
- Basic authentication system (Login/Register)
- Real-time analytics (total, safe, suspicious URLs)

## Tech Stack

Frontend: React  
Backend: Flask (Python)  
Database: SQLite  
API Communication: Axios  

## How to Run

Backend

cd backend  
pip install flask flask-cors  
python app.py  

Backend runs on: http://127.0.0.1:5000

Frontend

cd frontend  
npm install  
npm start  

Frontend runs on: http://localhost:3000

## Example Detection

- google.com → Safe  
- g00gle.com → Suspicious  
- rnicrosoft.com → Suspicious  
- http://fake-login-bank.com → Suspicious  

## Project Highlights

- Built a rule-based phishing detection engine without using machine learning
- Implemented domain normalization and pattern recognition techniques
- Designed a full-stack system with REST APIs and persistent storage
- Focused on explainability and real-world cybersecurity concepts

## Future Enhancements

- Integration with threat intelligence APIs (VirusTotal, etc.)
- WHOIS-based domain age analysis
- Redirect chain tracking
- JWT-based authentication
- Advanced analytics dashboard with charts
- Scalable URL scanning system
