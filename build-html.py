#!/usr/bin/env python3
"""Render the markdown docs to a single browsable HTML file with a sidebar."""
import glob
import html
import os
import re

D = os.path.dirname(os.path.abspath(__file__))
ORDER = ["README.md"] + sorted(f for f in os.listdir(D)
                               if re.match(r"\d\d-.*\.md$", f))


def inline(t):
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m:
               f'<a href="{"#" + m.group(2)[:-3] if m.group(2).endswith(".md") else m.group(2)}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def render(md):
    out, code, tbl, lst = [], False, False, False
    for ln in md.split("\n"):
        if ln.startswith("```"):
            if lst: out.append("</ul>"); lst = False
            code = not code
            out.append("<pre><code>" if code else "</code></pre>")
            continue
        if code:
            out.append(html.escape(ln)); continue

        if ln.startswith("|"):
            if lst: out.append("</ul>"); lst = False
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            if not tbl:
                out.append("<table>"); tbl = True
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
                continue
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        if tbl:
            out.append("</table>"); tbl = False

        if ln.startswith("- [ ] "):
            if not lst: out.append('<ul class="check">'); lst = True
            out.append(f"<li>{inline(ln[6:])}</li>"); continue
        if ln.startswith("- "):
            if not lst: out.append("<ul>"); lst = True
            out.append(f"<li>{inline(ln[2:])}</li>"); continue
        if lst and ln.strip() == "":
            out.append("</ul>"); lst = False

        if ln.startswith("### "):   out.append(f"<h3>{inline(ln[4:])}</h3>")
        elif ln.startswith("## "):  out.append(f"<h2>{inline(ln[3:])}</h2>")
        elif ln.startswith("# "):   out.append(f"<h1>{inline(ln[2:])}</h1>")
        elif ln.startswith("> "):   out.append(f"<blockquote>{inline(ln[2:])}</blockquote>")
        elif ln.strip() == "---":   out.append("<hr>")
        elif ln.strip() == "":      out.append("")
        else:                       out.append(f"<p>{inline(ln)}</p>")
    if tbl: out.append("</table>")
    if lst: out.append("</ul>")
    return "\n".join(out)


sections, nav = [], []
for f in ORDER:
    md = open(os.path.join(D, f)).read()
    # strip the breadcrumb lines — the sidebar replaces them
    md = "\n".join(l for l in md.split("\n")
                   if not l.startswith("[←") and "· [Next:" not in l)
    sid = f[:-3]
    title = next((l[2:] for l in md.split("\n") if l.startswith("# ")), sid)
    nav.append(f'<a href="#{sid}">{html.escape(title)}</a>')
    sections.append(f'<section id="{sid}">{render(md)}</section>')

CSS = """
*{box-sizing:border-box}
body{margin:0;font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans",Arial,sans-serif;
 color:#1F2937;background:#fff;display:flex}
nav{width:270px;flex:none;position:sticky;top:0;height:100vh;overflow-y:auto;
 background:#0F172A;padding:22px 0}
nav b{display:block;color:#fff;font-size:17px;padding:0 20px 14px;border-bottom:1px solid #1E293B;margin-bottom:10px}
nav a{display:block;color:#94A3B8;text-decoration:none;padding:9px 20px;font-size:14px;border-left:3px solid transparent}
nav a:hover{color:#fff;background:#1E293B}
nav a.on{color:#fff;border-left-color:#2563EB;background:#1E293B}
main{flex:1;min-width:0;max-width:880px;margin:0 auto;padding:40px 34px 100px}
section{padding-bottom:34px;margin-bottom:34px;border-bottom:1px solid #E5E7EB}
section:last-child{border:0}
h1{font-size:32px;letter-spacing:-.02em;margin:.3em 0 .5em;scroll-margin-top:20px}
h2{font-size:22px;margin:1.9em 0 .5em}
h3{font-size:17px;margin:1.5em 0 .4em}
p{margin:0 0 1em}
img{max-width:100%;border:1px solid #E5E7EB;border-radius:9px;display:block;margin:16px 0;
 box-shadow:0 2px 10px rgba(15,23,42,.07)}
a{color:#2563EB}
code{background:#F1F5F9;padding:2px 6px;border-radius:5px;font-size:13.5px;
 font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
pre{background:#0F172A;color:#E2E8F0;padding:15px 17px;border-radius:9px;overflow:auto;font-size:13.5px}
pre code{background:none;color:inherit;padding:0}
blockquote{margin:1.2em 0;padding:13px 17px;border-left:4px solid #2563EB;background:#EFF6FF;
 border-radius:0 8px 8px 0}
table{width:100%;border-collapse:collapse;margin:1.1em 0;font-size:14.5px}
th{background:#F8FAFC;text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:#475569}
th,td{padding:9px 12px;border-bottom:1px solid #E5E7EB;vertical-align:top}
hr{border:0;border-top:1px solid #E5E7EB;margin:2em 0}
ul{padding-left:22px;margin:0 0 1em}
li{margin:.3em 0}
ul.check{list-style:none;padding-left:4px}
ul.check li::before{content:"☐  ";color:#2563EB;font-weight:700}
@media(max-width:900px){body{display:block}nav{width:auto;height:auto;position:static}main{padding:24px 18px 60px}}
"""

JS = """
const links=[...document.querySelectorAll('nav a')];
const secs=links.map(a=>document.querySelector(a.getAttribute('href')));
function sync(){
  let i=secs.findIndex(s=>s&&s.getBoundingClientRect().top>90);
  if(i===-1)i=secs.length; i=Math.max(0,i-1);
  links.forEach((a,n)=>a.classList.toggle('on',n===i));
}
document.addEventListener('scroll',sync,{passive:true}); sync();
"""

open(os.path.join(D, "index.html"), "w").write(
    "<!doctype html><meta charset='utf-8'>"
    "<title>Voltra — Documentation</title>"
    "<meta name='viewport' content='width=device-width,initial-scale=1'>"
    f"<style>{CSS}</style>"
    f"<nav><b>Voltra docs</b>{''.join(nav)}</nav>"
    f"<main>{''.join(sections)}</main>"
    f"<script>{JS}</script>")
print("index.html written")
