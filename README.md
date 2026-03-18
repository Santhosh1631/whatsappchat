# Chat Importer

A full-stack WhatsApp chat import and visualization app.

## Stack

- Frontend: React + Vite
- Backend: Flask
- Database: MySQL
- Optional real-time support: Flask-SocketIO initialized in backend

## Features

- Upload WhatsApp exported .txt files
- Robust chat parser with real-world edge-case handling:
  - Multiline messages
  - Multiple date formats (dd/mm/yy, mm/dd/yyyy, dd-mm-yy)
  - 12-hour and 24-hour times
  - Media message detection
  - System message detection
  - Missing sender handling
- MySQL persistence with participant mapping
- WhatsApp-like chat interface (sidebar, bubbles, timestamps)
- Message search with highlighted matches
- Analytics dashboard:
  - Total messages
  - Most active user
  - Messages per day
  - Word frequency
- Bonus endpoints:
  - AI-style summary (heuristic)
  - Sentiment snapshot (lexicon-based)
  - Export parsed chat as JSON

## Folder Structure

```text
whatsappchat/
  backend/
    app.py
    requirements.txt
    .env.example
    chat_importer/
      __init__.py
      config.py
      extensions.py
      models/
        user.py
        message.py
      routes/
        chat_routes.py
        analytics_routes.py
      services/
        parser_service.py
        import_service.py
        analytics_service.py
        ai_service.py
      utils/
  frontend/
    package.json
    vite.config.js
    index.html
    src/
      App.jsx
      main.jsx
      styles.css
      pages/
        ChatPage.jsx
      components/
        UploadPanel.jsx
        Sidebar.jsx
        SearchBar.jsx
        ChatWindow.jsx
        MessageBubble.jsx
        AnalyticsPanel.jsx
      services/
        api.js
  schema.sql
  README.md
```

## MySQL Schema

The SQL schema is provided in:

- schema.sql

## Setup Instructions

1. Create database tables.

```bash
mysql -u root -p < schema.sql
```

2. Configure backend environment.

- Copy backend/.env.example to backend/.env
- Update MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

3. Install backend dependencies.

```bash
cd backend
pip install -r requirements.txt
```

4. Run backend server.

```bash
python app.py
```

Backend will run on http://localhost:5000

5. Install frontend dependencies.

```bash
cd ../frontend
npm install
```

6. Run frontend app.

```bash
npm run dev
```

Frontend will run on http://localhost:5173

## API Endpoints

- POST /api/upload-chat
  - multipart/form-data with field name: file
- GET /api/messages?search=keyword
- GET /api/users
- GET /api/analytics
- GET /api/export-json
- GET /api/ai-summary
- GET /api/sentiment

## Parsing Engine Notes

Parser logic is in backend/chat_importer/services/parser_service.py.

Core implementation details:

- Regex detects message start lines with date-time prefix
- Intelligent buffering appends non-matching lines to previous message
- Date-time parser attempts multiple formats with day/month ambiguity heuristic
- Message classifier marks text/media/system types
- Sorting ensures chronological reconstruction before persistence

## Production Improvement Ideas

- Add file size and rate limiting
- Add conversation table and multi-chat grouping
- Use background jobs for very large imports
- Replace heuristic AI summary with an LLM provider
- Replace sentiment lexicon with transformer sentiment model
- Add authentication + chat ownership
