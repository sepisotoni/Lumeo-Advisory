#!/usr/bin/env python3
"""Builds the blog, recommended page, sitemap and homepage teaser.

Run:  python3 build.py
Add an article:  add an entry to articles.py, then run this again.
Add a partner link: edit PARTNER_LINKS below, then run this again.
"""
import base64
import html
import mimetypes
import os
import re
from datetime import date

from articles import ARTICLES

SITE = "https://www.lumeo-advisory.co.za"
EMAIL = "admin@lumeo-advisory.co.za"
ROOT = os.path.dirname(os.path.abspath(__file__))

# Partner links. Change a URL here and re-run to update every page.
IKHOKHA_URL = "https://connect.ikhokha.com/ik-referral?code=uYzKEYNl"
NAKED_URL = "https://app.naked.insure/e/j6UDD5yZV6b"
WEBAFRICA_URL = "https://www.webafrica.co.za/affiliate?aff=WA-W3701104"

DISCLOSURE = ("Some links on this page are partner links. Lumeo Advisory may receive a reward "
              "if you sign up through them. Always compare options before you decide.")
GENERAL_NOTE = ("General information for South African small businesses, not tax, legal or "
                "financial advice. Rules and thresholds change, so check with SARS or your "
                "practitioner for your situation.")

FUNDING = [
    ("Funding and finance", [
        ("SEFA", "https://www.sefa.org.za", "Small Enterprise Finance Agency. Loans and guarantees for small businesses."),
        ("NEF", "https://www.nefcorp.co.za", "National Empowerment Fund. Funding for black-owned and empowered businesses."),
        ("Business Partners", "https://www.businesspartners.co.za", "Finance and mentorship for established small and medium businesses."),
        ("IDC", "https://www.idc.co.za", "Industrial Development Corporation. Larger funding for industry, agri-processing and more."),
        ("NYDA", "https://www.nyda.gov.za", "National Youth Development Agency. Support and grants for young entrepreneurs."),
        ("Thundafund", "https://www.thundafund.com", "South African crowdfunding platform for projects and products."),
    ]),
    ("Support and compliance", [
        ("SEDA", "https://www.seda.org.za", "Small Enterprise Development Agency. Free business support and training."),
        ("DSBD", "https://www.dsbd.gov.za", "Department of Small Business Development. Programmes and policy."),
        ("SARS", "https://www.sars.gov.za", "Tax registration, eFiling and tax compliance status."),
        ("CIPC", "https://www.cipc.co.za", "Company registration and annual returns."),
        ("National Credit Regulator", "https://www.ncr.org.za", "Check that a lender is registered before you borrow."),
    ]),
]

NAV = [("Services", "index.html#services"), ("How it works", "index.html#process"),
       ("Plans", "index.html#plans"), ("Blog", "blog/index.html"),
       ("Recommended", "recommended.html")]


def esc(s):
    return html.escape(s, quote=True)


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def head(title, desc, base, path, kind="website", extra=""):
    url = f"{SITE}/{path}"
    return f"""<!DOCTYPE html>
<html lang="en-ZA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="theme-color" content="#234E70">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:type" content="{kind}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/images/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{base}images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="{base}images/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{base}styles.css">
{extra}</head>
<body>
"""


def header(base):
    links = "\n".join(f'        <a href="{base}{h}">{t}</a>' for t, h in NAV)
    return f"""  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap bar">
      <a class="brand" href="{base}index.html" aria-label="Lumeo Advisory home">
        <img class="mark" src="{base}images/logo-mark.png" alt="" width="50" height="34">
        <span>Lumeo Advisory</span>
      </a>
      <nav class="nav" aria-label="Main">
{links}
      </nav>
      <a class="btn btn-small" href="{base}index.html#contact">Book a call</a>
    </div>
  </header>
"""


def footer(base):
    return f"""  <footer class="site-footer">
    <div class="wrap foot">
      <a class="foot-logo" href="{base}index.html" aria-label="Lumeo Advisory home"><img src="{base}images/logo.png" alt="Lumeo Advisory" width="110" height="114"></a>
      <div class="foot-meta">
        <span class="foot-links"><a href="{base}blog/index.html">Blog</a><a href="{base}recommended.html">Recommended tools</a><a href="mailto:{EMAIL}">{EMAIL}</a></span>
        <span>&copy; {date.today().year} Lumeo Advisory</span>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def data_uri(rel):
    full = os.path.join(ROOT, rel)
    mime = mimetypes.guess_type(full)[0] or "application/octet-stream"
    with open(full, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def inline_assets(page):
    """Make a page self-contained: CSS, JS and images are embedded."""
    with open(os.path.join(ROOT, "styles.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(ROOT, "script.js"), encoding="utf-8") as f:
        js = f.read()
    page = re.sub(r'<link rel="stylesheet" href="[^"]*styles\.css">', lambda m: "<style>\n" + css + "\n</style>", page)
    page = re.sub(r'<script src="[^"]*script\.js" defer></script>', lambda m: "<script>\n" + js + "\n</script>", page)

    def img(m):
        rel = m.group(2).replace("../", "")
        return f'{m.group(1)}="{data_uri(rel)}"'

    return re.sub(r'(src|href)="((?:\.\./)?images/[^"]+)"', img, page)


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if path.endswith(".html"):
        content = inline_assets(content)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def render_blocks(blocks):
    out = []
    for kind, val in blocks:
        if kind == "p":
            out.append(f"<p>{val}</p>")
        elif kind == "h2":
            out.append(f"<h2>{val}</h2>")
        elif kind == "ul":
            out.append("<ul>" + "".join(f"<li>{i}</li>" for i in val) + "</ul>")
    return "\n        ".join(out)


def words(blocks):
    n = 0
    for kind, val in blocks:
        text = " ".join(val) if isinstance(val, list) else val
        n += len(re.sub(r"<[^>]+>", " ", text).split())
    return n


def post_list(posts, base):
    rows = []
    for a in posts:
        rows.append(f"""          <a class="post" href="{base}blog/{a['slug']}.html">
            <img class="thumb" src="{base}images/blog/{a['slug']}.svg" alt="" width="168" height="88">
            <span class="post-body">
              <time datetime="{a['date']}">{long_date(a['date'])}</time>
              <span class="post-title">{esc(a['title'])}</span>
              <span class="post-sum">{esc(a['summary'])}</span>
            </span>
          </a>""")
    return "\n".join(rows)


# ---- Cover images (one SVG per article, drawn from simple shapes) ----
W = 'stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" fill="none"'
G = 'stroke="#F4C24B" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" fill="none"'
ICONS = {
    "where-small-businesses-can-find-funding": f'<g {W}><ellipse cx="560" cy="400" rx="110" ry="34"/><path d="M450 400v-50M670 400v-50"/><ellipse cx="560" cy="350" rx="110" ry="34"/><path d="M450 350v-50M670 350v-50"/><ellipse cx="560" cy="300" rx="110" ry="34"/></g><g {G}><ellipse cx="700" cy="230" rx="70" ry="22"/><path d="M630 230v-36M770 230v-36"/><ellipse cx="700" cy="194" rx="70" ry="22"/></g>',
    "what-funders-ask-for": f'<g {W}><path d="M480 190h170l70 70v200H480z"/><path d="M650 190v70h70M520 320h160M520 370h120"/></g><g {G}><path d="M690 420l32 32 62-70"/></g>',
    "surviving-the-january-cash-flow-dip": f'<g {W}><path d="M440 210v250h330"/></g><g {G}><path d="M470 260l80 60 60-30 70 120 60-40"/></g>',
    "set-up-your-business-finances-for-the-new-year": f'<g {W}><rect x="470" y="190" width="260" height="280" rx="20"/><path d="M520 260h40M520 330h40M520 400h40M600 260h80M600 330h80M600 400h80"/></g><g {G}><path d="M516 262l10 10 20-24M516 332l10 10 20-24"/></g>',
    "provisional-tax-without-the-panic": f'<g {W}><rect x="450" y="210" width="300" height="250" rx="22"/><path d="M450 280h300M520 180v50M680 180v50"/></g><g {G}><path d="M520 340h20M590 340h20M660 340h20M520 400h20M590 400h20"/></g>',
    "tax-year-end-gather-your-records": f'<g {W}><path d="M450 230a20 20 0 0 1 20-20h90l36 40h134a20 20 0 0 1 20 20v190a20 20 0 0 1-20 20H470a20 20 0 0 1-20-20z"/></g><g {G}><path d="M540 360h120M540 410h80"/></g>',
    "grants-and-support-programmes": f'<g {W}><path d="M450 250l150-70 150 70z"/><path d="M490 280v150M560 280v150M640 280v150M710 280v150M450 450h300"/></g><g {G}><path d="M600 228v0"/></g>',
    "do-you-need-to-register-for-vat": f'<g {W}><path d="M470 220h150l140 140-120 120-140-140z"/></g><g {G}><path d="M545 420l100-120"/><circle cx="535" cy="318" r="14"/><circle cx="655" cy="402" r="14"/></g>',
    "taking-card-payments-what-to-look-for": f'<g {W}><rect x="440" y="230" width="320" height="210" rx="28"/><path d="M440 290h320"/></g><g {G}><path d="M480 380h90M480 410h50"/></g>',
    "know-your-margins-before-you-change-prices": f'<g {W}><path d="M450 460h300"/></g><g {G}><path d="M500 440v-80M580 440v-140M660 440v-200M740 440v-250" /></g>',
    "protect-yourself-not-only-the-business": f'<g {W}><path d="M600 180l140 50v110c0 80-60 120-140 150-80-30-140-70-140-150V230z"/></g><g {G}><path d="M540 340l45 45 80-95"/></g>',
    "funding-without-a-bank-loan": f'<g {W}><path d="M450 270h260M450 270l50-45M450 270l50 45"/><path d="M750 390H490M750 390l-50-45M750 390l-50 45"/></g><g {G}><circle cx="600" cy="460" r="0"/></g>',
    "five-things-to-do-before-december": f'<g {W}><path d="M450 330h300"/><circle cx="470" cy="330" r="18"/><circle cx="535" cy="330" r="18"/><circle cx="600" cy="330" r="18"/><circle cx="665" cy="330" r="18"/><circle cx="730" cy="330" r="18"/></g><g {G}><path d="M590 330l8 8 14-16"/></g>',
}
DEFAULT_ICON = f'<g {W}><circle cx="600" cy="300" r="90"/></g>'


def cover_svg(slug):
    icon = ICONS.get(slug, DEFAULT_ICON)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-hidden="true">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#234E70"/><stop offset="1" stop-color="#3F8F98"/></linearGradient></defs>
<rect width="1200" height="630" fill="url(#g)"/>
<circle cx="1050" cy="90" r="190" fill="#fff" fill-opacity=".07"/><circle cx="130" cy="560" r="150" fill="#fff" fill-opacity=".06"/>
<g transform="translate(600 315) scale(1.7) translate(-600 -320)">{icon}</g>
</svg>
"""


def build_covers(posts):
    for a in posts:
        write(f"images/blog/{a['slug']}.svg", cover_svg(a["slug"]))


def build_articles(posts):
    for i, a in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        mins = max(1, round(words(a["body"]) / 200))
        ld = f"""  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article","headline":{esc(a['title']).join(['"','"'])},"datePublished":"{a['date']}","author":{{"@type":"Organization","name":"Lumeo Advisory"}},"publisher":{{"@type":"Organization","name":"Lumeo Advisory"}},"mainEntityOfPage":"{SITE}/blog/{a['slug']}.html"}}
  </script>
"""
        page = head(f"{a['title']} | Lumeo Advisory", a["summary"], "../", f"blog/{a['slug']}.html", "article", ld)
        page += header("../")
        page += f"""
  <main id="main">
    <article class="article narrow">
      <div class="meta"><time datetime="{a['date']}">{long_date(a['date'])}</time><span>{mins} min read</span></div>
      <h1>{esc(a['title'])}</h1>
      <img class="cover" src="../images/blog/{a['slug']}.svg" alt="" width="1200" height="630">
      <div class="prose">
        {render_blocks(a['body'])}
      </div>
"""
        if a.get("partner"):
            page += f'      <p class="disclosure">{DISCLOSURE}</p>\n'
        page += f"""      <aside class="help">
        <h2>{a['help'][0]}</h2>
        <p>{a['help'][1]}</p>
        <a class="btn" href="../index.html#contact">Book a free 20-minute call</a>
      </aside>
      <p class="note">{GENERAL_NOTE}</p>
      <nav class="pager" aria-label="More articles">
"""
        if older:
            page += f'        <a class="prev" href="{older["slug"]}.html"><span>Older</span><strong>{esc(older["title"])}</strong></a>\n'
        if newer:
            page += f'        <a class="next" href="{newer["slug"]}.html"><span>Newer</span><strong>{esc(newer["title"])}</strong></a>\n'
        page += """      </nav>
    </article>
  </main>

"""
        page += footer("../")
        write(f"blog/{a['slug']}.html", page)


def build_blog_index(posts):
    page = head("Blog | Lumeo Advisory",
                "Practical articles on funding, cash flow, tax admin, accounting and bookkeeping for South African small businesses.",
                "../", "blog/index.html")
    page += header("../")
    page += f"""
  <main id="main">
    <section class="page-head">
      <div class="wrap">
        <h1>Blog</h1>
        <p class="lead">Practical notes on funding, cash flow and money admin for South African small businesses.</p>
      </div>
    </section>
    <section class="section" style="padding-top:1rem">
      <div class="wrap">
        <label class="search"><span class="sr">Search articles</span><input id="post-search" type="search" placeholder="Search articles, e.g. VAT or funding" autocomplete="off"></label>
        <p id="no-results" class="fineprint" hidden>No articles match your search.</p>
        <div class="posts" id="post-list">
{post_list(posts, '../')}
        </div>
      </div>
    </section>
  </main>

"""
    page += footer("../")
    page = page.replace("</body>", '  <script src="../script.js" defer></script>\n</body>')
    write("blog/index.html", page)


def funding_grid():
    cols = []
    for title, items in FUNDING:
        lis = "".join(
            f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a><span>{esc(d)}</span></li>'
            for n, u, d in items)
        cols.append(f"<div><h3>{title}</h3><ul>{lis}</ul></div>")
    return '<div class="links-grid">' + "".join(cols) + "</div>"


def build_recommended():
    page = head("Recommended tools | Lumeo Advisory",
                "Payment, insurance and funding tools we recommend to small business owners, from Lumeo Advisory.",
                "", "recommended.html")
    page += header("")
    page += f"""
  <main id="main">
    <section class="page-head">
      <div class="wrap">
        <h1>Recommended tools</h1>
        <p class="lead">Tools and places we point business owners to: getting paid, staying protected and finding funding. Share this page with anyone starting out.</p>
        <p class="fineprint" style="margin-top:1rem">{DISCLOSURE}</p>
      </div>
    </section>

    <section class="partner" id="ikhokha">
      <div class="wrap partner-grid">
        <div>
          <h2>iKhokha</h2>
          <p class="kicker">Card payments for small businesses, without a monthly machine rental.</p>
          <a class="btn" href="{IKHOKHA_URL}" target="_blank" rel="sponsored noopener">Sign up for 10% off</a>
        </div>
        <div class="partner-body">
          <p>iKhokha is a South African card payment provider. It helps small businesses, market traders and service providers move from cash-only to taking cards, using devices and tools that work with a free app.</p>
          <p>Our referral link takes you to iKhokha's sign-up page for a 10% discount. You need to sign up to access the offer, but you do not have to buy a card machine straight away. If you have low foot traffic, you can sign up, download the app and decide whether to buy a machine later.</p>
          <h3>What you can use</h3>
          <ul>
            <li><strong>Card machines.</strong> Portable machines (the iK Flyer and the smaller iK Flyer Lite) that take tap, insert and swipe payments and send receipts.</li>
            <li><strong>Tap on Phone.</strong> Accept contactless payments on a compatible smartphone, with no separate machine.</li>
            <li><strong>Pay Links and invoices.</strong> Send a link by WhatsApp, SMS or email so customers can pay online. Useful if you take bookings or sell remotely.</li>
            <li><strong>Online store tools.</strong> A payment gateway for WooCommerce, Wix and Shopstar sites.</li>
            <li><strong>Sales tracking.</strong> The app records your sales so you can see what came in each day.</li>
          </ul>
          <h3>Why it matters for your books</h3>
          <p>Card payments reach your bank account as settlements, with transaction fees taken out. That means your bank statement will not match your sales one for one. When we do your bookkeeping, we reconcile settlements against sales and record the fees, so your income and costs are both accurate.</p>
          <p class="fineprint">iKhokha is part of the Nedbank group. Device prices and transaction rates change and depend on your volumes, so check <a href="https://www.ikhokha.com" target="_blank" rel="noopener">ikhokha.com</a> for current pricing and compare it with other providers.</p>
        </div>
      </div>
    </section>

    <section class="partner band" id="naked">
      <div class="wrap partner-grid">
        <div>
          <h2>Naked Insurance</h2>
          <p class="kicker">Personal insurance for the person behind the business.</p>
          <a class="btn" href="{NAKED_URL}" target="_blank" rel="sponsored noopener">Get a quote from Naked</a>
        </div>
        <div class="partner-body">
          <p>Naked is a South African digital insurer. You get a quote and manage your policy online or in the app, without a call centre. Policies are underwritten by Hollard Specialist Insurance, and Naked is an authorised financial services provider (FSP 48822).</p>
          <h3>Cover that suits entrepreneurs</h3>
          <ul>
            <li><strong>Car insurance.</strong> Comprehensive cover for the vehicle you drive to clients and suppliers.</li>
            <li><strong>Single-item insurance.</strong> Cover for specific items such as a laptop, phone or camera. Ask Naked to confirm how business use is treated before you buy.</li>
            <li><strong>Home contents and building insurance.</strong> Protect your home, including the space you work from.</li>
          </ul>
          <h3>What it does not replace</h3>
          <p>Naked is personal insurance. Stock, business equipment and liability cover for the business itself usually need separate business insurance, and income protection, life and disability cover come from a financial adviser. We cover this in <a href="blog/protect-yourself-not-only-the-business.html">Protect yourself, not only the business</a>.</p>
          <h3>How it links to your business</h3>
          <p>A claim, a stolen laptop or a written-off car can interrupt your income. Keeping personal and business money separate, and your books up to date, makes it easier to see what a disruption costs and whether you can absorb it. <a href="index.html#contact">Talk to Lumeo</a> about setting that up.</p>
        </div>
      </div>
    </section>

    <section class="partner" id="webafrica">
      <div class="wrap partner-grid">
        <div>
          <h2>Webafrica</h2>
          <p class="kicker">Internet and hosting services for your business.</p>
          <a class="btn" href="{WEBAFRICA_URL}" target="_blank" rel="sponsored noopener">Explore Webafrica</a>
        </div>
        <div class="partner-body">
          <p>Webafrica is a South African internet service provider offering home and business connectivity. Reliable internet can help you keep in touch with customers, manage online sales and use cloud-based business tools.</p>
          <h3>Internet options</h3>
          <ul>
            <li><strong>Fibre.</strong> Uncapped fibre packages, with speeds advertised up to 1Gbps where the service is available.</li>
            <li><strong>Fixed Wireless.</strong> Plug-and-play internet that connects through a nearby cellular tower, without a fibre cable to the premises. Webafrica advertises speeds up to 150Mbps for this service.</li>
            <li><strong>Address-based availability.</strong> Fibre coverage and wireless performance depend on your location, so check your address and the package details before choosing.</li>
          </ul>
          <p>Compare current speeds, pricing, setup requirements and contract terms before signing up. The link goes to Webafrica and may be used to sign up for its services.</p>
        </div>
      </div>
    </section>

    <section class="partner" id="funding">
      <div class="wrap">
        <h2>Funding and support links</h2>
        <p class="kicker" style="max-width:40rem">Places to look for finance, training and compliance help. Each funder has its own criteria, so read them before you apply. Funders will ask for up-to-date financial records, and that is where Lumeo comes in.</p>
        {funding_grid()}
        <p class="fineprint" style="margin-top:2rem">Links open the organisation's own website. We have no control over their content or criteria.</p>
      </div>
    </section>

    <section class="section band" id="suggest">
      <div class="wrap narrow">
        <h2>Know a tool worth sharing?</h2>
        <p style="margin-top:1rem;color:var(--muted)">If you are a business owner or a provider and think something belongs here, email <a href="mailto:{EMAIL}" style="color:var(--pine)">{EMAIL}</a>.</p>
      </div>
    </section>
  </main>

"""
    page += footer("")
    write("recommended.html", page)


def update_homepage(posts):
    with open(os.path.join(ROOT, "index.src.html"), encoding="utf-8") as f:
        s = f.read()
    block = '<!--LATEST-->\n        <div class="posts">\n' + post_list(posts[:3], "") + '\n        </div>\n        <!--/LATEST-->'
    s = re.sub(r"<!--LATEST-->.*?<!--/LATEST-->", lambda m: block, s, flags=re.S)
    write("index.html", s)


def build_sitemap(posts):
    urls = [("", date.today().isoformat()), ("recommended.html", date.today().isoformat()),
            ("blog/index.html", posts[0]["date"])]
    urls += [(f"blog/{a['slug']}.html", a["date"]) for a in posts]
    body = "\n".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{d}</lastmod></url>" for p, d in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    posts = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)
    build_covers(posts)
    build_articles(posts)
    build_blog_index(posts)
    build_recommended()
    update_homepage(posts)
    build_sitemap(posts)
    print(f"Built index, {len(posts)} articles, blog index, recommended page, sitemap.")
