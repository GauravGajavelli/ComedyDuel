"""
Scrape Seinfeld opening monologues from seinfeldscripts.com.
We grab 5 episodes, extract the full script text, and save it for manual boundary identification.
"""

import urllib.request
import ssl
import re
from html.parser import HTMLParser

# Bypass SSL certificate verification (site has cert issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class SimpleHTMLStripper(HTMLParser):
    """Strip HTML tags, keep text and basic line breaks."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True
        elif tag in ('br', 'p', 'div', 'tr'):
            self.result.append('\n')

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag in ('p', 'div', 'tr'):
            self.result.append('\n')

    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            self.result.append(data)

    def get_text(self):
        return ''.join(self.result)


def strip_html(html):
    s = SimpleHTMLStripper()
    s.feed(html)
    return s.get_text()


def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    })
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')


# Step 1: Get the episode index page
print("Fetching episode index...")
index_html = fetch("http://www.seinfeldscripts.com/seinfeld-scripts.html")

# Step 2: Extract episode links
# Links look like: <a href="TheStakeout.htm">The Stakeout</a>
link_pattern = re.compile(r'<a\s+href=["\']([^"\']+\.htm)["\'][^>]*>([^<]+)</a>', re.IGNORECASE)
episodes = []
for match in link_pattern.finditer(index_html):
    href, title = match.group(1), match.group(2).strip()
    if title and not title.lower().startswith('home') and len(title) > 2:
        episodes.append((href, title))

print(f"Found {len(episodes)} episode links")

# Pick 5 early episodes (seasons 1-2 have the most standup content)
# Seinfeld's early episodes had extended opening monologues
selected = episodes[:10]  # grab first 10 to have fallback options
print(f"\nFirst 10 episodes available:")
for i, (href, title) in enumerate(selected):
    print(f"  {i+1}. {title} ({href})")

# Fetch the first 5
targets = selected[:5]
print(f"\n--- Fetching 5 episodes ---\n")

for href, title in targets:
    url = f"http://www.seinfeldscripts.com/{href.strip()}"
    print(f"Fetching: {title} -> {url}")
    try:
        html = fetch(url)
        text = strip_html(html)
        # Clean up excessive whitespace
        lines = [l.rstrip() for l in text.split('\n')]
        text = '\n'.join(lines)
        # Remove runs of 3+ blank lines
        text = re.sub(r'\n{4,}', '\n\n\n', text)

        safe_title = re.sub(r'[^a-zA-Z0-9]+', '_', title).strip('_')
        outpath = f"/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/raw_scripts/{safe_title}.txt"
        import os
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, 'w') as f:
            f.write(text)
        print(f"  Saved: {outpath} ({len(text)} chars)")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nDone. Now manually identify opening monologue boundaries in each file.")
