"""Dependency-free portfolio web server. Start: python server.py"""
from __future__ import annotations
import json
import os
import re
import sqlite3
import ssl
import smtplib
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

ROOT = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get('PORTFOLIO_DATA_DIR', str(ROOT / 'data'))).resolve()
DB = DATA_DIR / 'messages.sqlite3'
DATA_DIR.mkdir(parents=True, exist_ok=True)
RECENT = {}
LOCK = Lock()


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_utc TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )''')


def send_optional_notification(name, email, message):
    """Email is optional. Messages are saved even if SMTP is not configured."""
    required = ['SMTP_HOST', 'SMTP_USER', 'SMTP_PASSWORD', 'CONTACT_NOTIFY_EMAIL']
    if not all(os.environ.get(k) for k in required):
        return False
    mail = EmailMessage()
    mail['Subject'] = f'Portfolio contact: {name}'
    mail['From'] = os.environ['SMTP_USER']
    mail['To'] = os.environ['CONTACT_NOTIFY_EMAIL']
    mail['Reply-To'] = email
    mail.set_content(f'From: {name} <{email}>\n\n{message}')
    with smtplib.SMTP_SSL(os.environ['SMTP_HOST'], int(os.environ.get('SMTP_PORT', '465')), context=ssl.create_default_context(), timeout=12) as smtp:
        smtp.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
        smtp.send_message(mail)
    return True


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, code, payload):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split('?')[0].startswith(('/data/', '/__pycache__/', '/.')):
            self.send_error(404)
            return
        if self.path == '/api/health':
            self.send_json(200, {'ok': True, 'service': 'Thanuja Portfolio'})
            return
        super().do_GET()

    def do_POST(self):
        if self.path != '/api/contact':
            return self.send_json(404, {'ok': False, 'error': 'Not found.'})
        try:
            content_length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            return self.send_json(400, {'ok': False, 'error': 'Invalid request size.'})
        if content_length <= 0 or content_length > 12000:
            return self.send_json(413, {'ok': False, 'error': 'Request is empty or too large.'})
        try:
            payload = json.loads(self.rfile.read(content_length))
            if not isinstance(payload, dict):
                raise ValueError('Expected an object')
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            return self.send_json(400, {'ok': False, 'error': 'Invalid message format.'})
        if payload.get('website'):
            return self.send_json(200, {'ok': True, 'message': 'Thank you for your message.'})
        name, email, message = (str(payload.get(k, '')).strip() for k in ('name', 'email', 'message'))
        if not (2 <= len(name) <= 100):
            return self.send_json(400, {'ok': False, 'error': 'Name must be 2–100 characters.'})
        if not (len(email) <= 254 and re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email)):
            return self.send_json(400, {'ok': False, 'error': 'A valid email is required.'})
        if not (10 <= len(message) <= 5000):
            return self.send_json(400, {'ok': False, 'error': 'Message must be 10–5000 characters.'})
        key = self.client_address[0]
        with LOCK:
            now = time.monotonic()
            if now - RECENT.get(key, -1000) < 15:
                return self.send_json(429, {'ok': False, 'error': 'Please wait 15 seconds before sending another message.'})
            RECENT[key] = now
        try:
            with sqlite3.connect(DB, timeout=10) as db:
                db.execute('INSERT INTO messages (created_utc, name, email, message) VALUES (?, ?, ?, ?)',
                           (datetime.now(timezone.utc).isoformat(), name, email, message))
        except sqlite3.Error:
            return self.send_json(500, {'ok': False, 'error': 'The message could not be saved. Please email directly.'})
        notified = False
        try:
            notified = send_optional_notification(name, email, message)
        except (OSError, smtplib.SMTPException) as error:
            print('SMTP notification failed; message is saved:', str(error))
        return self.send_json(201, {'ok': True, 'message': 'Thank you! Your message was saved successfully.' + (' An email notification was sent.' if notified else '')})


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', '8000'))
    host = os.environ.get('HOST', '127.0.0.1')
    print(f'Portfolio running at http://{host}:{port} (Ctrl+C to stop)')
    ThreadingHTTPServer((host, port), Handler).serve_forever()
