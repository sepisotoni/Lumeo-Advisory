Lumeo Advisory website - www.lumeo-advisory.co.za
Static HTML. Every page has its CSS, script and images embedded, so each .html file also works when opened on its own.

DEPLOY
Upload everything except build.py and articles.py (optional) to your host's web root, then point the domain at it.

PAGES
index.html          Home
recommended.html    Recommended tools: iKhokha, Naked Insurance, Webafrica, funding links
blog/               13 articles, October 2025 to October 2026
images/             Logo files and one cover image per article (made by build.py)

EDIT
Contact email: admin@lumeo-advisory.co.za (script.js, index.html, build.py)
Plans:          edit index.src.html and styles.css, then regenerate the homepage.
Partner links:  top of build.py (IKHOKHA_URL, NAKED_URL, WEBAFRICA_URL), then run: python3 build.py
New article:   add an entry to articles.py, then run: python3 build.py
               (this also updates the blog list, homepage teaser and sitemap.xml)

CHECK BEFORE LAUNCH
Funder links in build.py (FUNDING) and articles.py were not all opened during the build.
Click each one once. The homepage contact form sends through Formspree; check its dashboard
to confirm submissions and notification settings.

LOGO: images/logo.png (full), images/logo-mark.png (header). Replace these files to change the logo.
Blog search runs in the browser, so it works on any host.

Homepage source is index.src.html. Edit it, then run python3 build.py to regenerate index.html.
