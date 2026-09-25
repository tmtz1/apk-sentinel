#!/usr/bin/env python3
"""Deterministic human HTML pages from reviewed Markdown and canonical status."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit
import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SITE = 'https://apk-sentinel.willowbirdie.com'
STYLE = '''body{margin:0;background:#101419;color:#e8edf2;font:17px/1.65 system-ui,sans-serif}main{max-width:900px;margin:auto;padding:32px 20px 64px}a{color:#77d6a3;overflow-wrap:anywhere}nav{display:flex;flex-wrap:wrap;gap:16px;border-bottom:1px solid #52606d;padding-bottom:16px}h1{font-size:clamp(1.8rem,5vw,3rem);line-height:1.2}pre{overflow:auto;padding:16px;background:#171d24}code{overflow-wrap:anywhere}aside{border-left:4px solid #e8c46c;padding:12px 18px;background:#171d24;margin:24px 0}table{display:block;overflow:auto;border-collapse:collapse}td,th{padding:8px;border:1px solid #52606d}img{max-width:100%;height:auto}footer{margin-top:40px;border-top:1px solid #52606d;padding-top:16px}'''
SUMMARIES = {'README.md': ('product-status.json', 'docs/pricing.md'), 'llms.txt': None, 'docs/llms.txt': None}
NAV = '<nav aria-label="Main"><a href="/">Home</a><a href="/about/">About</a><a href="/pricing/">Availability</a><a href="/agent-api-contract/">API contract</a><a href="/report-guide/">Report guide</a><a href="/contact/">Contact</a><a href="/security/">Security</a></nav>'


def link_target(match):
    href = match.group(1)
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return match.group(0)
    target = (DOCS / parsed.path).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError('Link escapes repository')
    if target.is_relative_to(DOCS):
        path = '/' + target.relative_to(DOCS).as_posix()
        if target.suffix == '.md':
            path = path[:-3] + '/'
    else:
        path = 'https://github.com/tmtz1/apk-sentinel/blob/main/' + target.relative_to(ROOT).as_posix()
    return 'href="' + urlunsplit(('', '', path, parsed.query, parsed.fragment)) + '"'


def availability_summary(status, name):
    payment = status['payment']
    label = 'Availability: ' + status['status'] + '.'
    text = status['availability_note']
    if status['status'] == 'limited-beta':
        text += f" Current terms: `{payment['price_usdc']} USDC` (`{payment['atomic_amount']}` atomic units) via {payment['mechanism']} on {payment['network']} (`{payment['network_id']}`) through {payment['test_ends']}."
    enabled = {'Browser upload': status['browser_upload'], 'General customer intake': status['general_customer_intake'], 'Customer support': status['customer_support']}
    text += ' ' + ' '.join(k + (': enabled.' if v else ': not enabled.') for k, v in enabled.items())
    if SUMMARIES[name]:
        status_link, pricing_link = SUMMARIES[name]
        return f"**{label}** {text} See the [canonical status]({status_link}) and [availability explanation]({pricing_link}). Documented endpoint: `{status['endpoint']}`."
    return label + ' ' + text + f"\n\nCanonical status: {SITE}/product-status.json\nAvailability explanation: {SITE}/pricing/\nDocumented endpoint: {status['endpoint']}"


def render_availability(text, status, name):
    pattern = r'<!-- AVAILABILITY:START -->\n.*?\n<!-- AVAILABILITY:END -->'
    if len(re.findall(pattern, text, flags=re.S)) != 1:
        raise ValueError(name + ' needs exactly one generated availability block')
    block = '<!-- AVAILABILITY:START -->\n' + availability_summary(status, name) + '\n<!-- AVAILABILITY:END -->'
    return re.sub(pattern, lambda _: block, text, flags=re.S)


def artifacts():
    status = json.loads((ROOT / 'product-status.json').read_text())
    banner = '<aside><strong>Availability: ' + escape(status['status']) + '.</strong> ' + escape(status['availability_note']) + ' <a href="/product-status.json">Canonical status</a>.</aside>'
    output = {ROOT / name: render_availability((ROOT / name).read_text(), status, name) for name in SUMMARIES}
    for source in sorted(DOCS.glob('*.md')):
        text = source.read_text()
        title = text.splitlines()[0].lstrip('# ')
        body = markdown.markdown(text, extensions=['fenced_code', 'tables'])
        body = re.sub(r'href="([^"]+)"', link_target, body)
        slug = source.stem
        output[DOCS / slug / 'index.html'] = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)}</title><link rel="canonical" href="{SITE}/{slug}/"><style>{STYLE}</style></head>
<body><main>{NAV}{banner}{body}<footer><a href="/{slug}.md">Markdown source</a> · <a href="https://github.com/tmtz1/apk-sentinel">Documentation and evidence</a></footer></main></body></html>
'''
    homepage = (DOCS / 'index.html').read_text()
    output[DOCS / 'index.html'] = re.sub(r'<!-- STATUS:START -->.*?<!-- STATUS:END -->', '<!-- STATUS:START -->' + banner + '<!-- STATUS:END -->', homepage, flags=re.S)
    urls = [SITE + '/'] + [SITE + '/' + p.stem + '/' for p in sorted(DOCS.glob('*.md'))]
    output[DOCS / 'sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + escape(u) + '</loc></url>\n' for u in urls) + '</urlset>\n'
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for path, content in artifacts().items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if stale:
        raise SystemExit('Regenerate stale generated files: ' + ', '.join(stale))
    print('Rendered documentation: ' + ('current' if args.check else 'generated'))


if __name__ == '__main__':
    main()
