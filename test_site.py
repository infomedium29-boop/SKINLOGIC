"""Static checks for generated Skinlogic website. Requires BeautifulSoup4."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from collections import Counter
root=Path(__file__).resolve().parent/'dist'; pages=list(root.rglob('index.html'));missing=[];missing_alt=[];h1_errors=[];noindex_errors=[]
for file in pages:
 soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
 if file==root/'index.html':continue
 heads=soup.find_all('h1')
 if len(heads)!=1:h1_errors.append((str(file.relative_to(root)),len(heads)))
 if not soup.find('meta',attrs={'name':'robots','content':'noindex,nofollow'}):noindex_errors.append(str(file))
 for a in soup.find_all(['a','img','link','script']):
  u=a.get('href') or a.get('src') or ''
  if a.name=='img' and not a.has_attr('alt'):missing_alt.append(str(file))
  if not u.startswith('/') or u.startswith('//'):continue
  path=urlsplit(u).path
  local=root/unquote(path).lstrip('/')
  if local.is_dir():local=local/'index.html'
  if not local.exists():missing.append((str(file.relative_to(root)),u))
print('HTML files:',len(pages),'localized:',len(pages)-1,'images:',len(list((root/'assets').glob('*.avif'))))
print('Broken internal paths:',len(missing),'H1 issues:',len(h1_errors),'Missing alt:',len(missing_alt),'Missing noindex:',len(noindex_errors))
if missing:print('Missing:',missing[:15])
if h1_errors:print('H1:',h1_errors[:8])
assert len(pages)==45
assert len(list((root/'assets').glob('*.avif')))==16
assert not (missing or missing_alt or h1_errors or noindex_errors)
print('PASS')
