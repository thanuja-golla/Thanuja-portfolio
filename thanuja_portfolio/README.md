# Golla Thanuja — portfolio website

A responsive HTML/CSS/JavaScript website with a dependency-free Python backend. The visual theme uses the user-supplied pink artwork and portrait. Content is based on the attached résumé.

## Run locally

1. Extract the ZIP archive.
2. Open a terminal inside the `thanuja_portfolio` folder.
3. Run `python server.py` (Windows may require `py server.py`).
4. Open **http://127.0.0.1:8000**.

No pip installs or frameworks are necessary. Python 3.9+ recommended.

**Important:** Do not open `index.html` directly from the file system if you want the contact form to work. Launch the Python server.

## Functional elements

- Responsive desktop/mobile menu and all navigation anchors.
- Explore my work / filter project cards (All, Professional, Academic).
- Open and close project details dialogs.
- Download the real uploaded résumé PDF.
- Professional profile link, direct email link, phone link and back-to-top.
- Contact form validates fields and posts messages to Python API.
- Messages stored in `data/messages.sqlite3` with a timestamp, name, email and message.
- Backend includes a honeypot and simple IP submission cooldown.
- Scroll reveal, progress indicator and current year footer.

## Optional email notifications

Contact submission **always stores messages in SQLite**; it does not automatically email anyone without setup. To receive email notifications, set these environment variables before running `server.py`:

- `SMTP_HOST` — your SMTP mail server
- `SMTP_PORT` — defaults to 465 (implicit TLS)
- `SMTP_USER` — SMTP login and sender address
- `SMTP_PASSWORD` — SMTP app password
- `CONTACT_NOTIFY_EMAIL` — inbox receiving notifications

If SMTP fails, messages remain in the database. Never commit SMTP credentials.

## Deployment notes

The Python server is designed for local use and demos. For production, host it behind an HTTPS reverse proxy (such as nginx), set `HOST=127.0.0.1`, use managed storage, and apply production-grade anti-spam, retention and security measures. Do not expose the `data` directory publicly. The application blocks HTTP access to it.

The fonts are loaded from Google Fonts when online, with local serif/sans-serif fallbacks. All image assets are bundled locally.

## Résumé accuracy / publishing check

The source résumé lists Innovapte internship as **July 2024 – “Till date”**. The site carries that wording as “PRESENT*” with a note to verify it before publishing. The résumé does not include live project URLs, so these are presented as descriptions with interactive detail dialogs, not fabricated links. The résumé’s short URL is included as a *Professional profile* link without claiming its destination was verified.

## Files

- `index.html` — semantic page structure
- `styles.css` — responsive styling and pink design theme
- `script.js` — interaction and form submission
- `server.py` — HTTP server, contact API and SQLite persistence
- `assets/portrait.webp` — optimized supplied photo
- `assets/pink-abstract.webp` — optimized supplied pink visual
- `assets/Thanuja_Golla_Resume.pdf` — original user-provided résumé

## Additional portfolio content
- Skills include Python, HTML, CSS, and Basic JavaScript.
- A Digital Marketing Certification entry is shown. The issuing organization and completion date were not supplied, so no credentials or verification links have been invented.
