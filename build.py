#!/usr/bin/env python3
"""Static website generator for Skinlogic. Requires Python 3.9+; no third-party packages.
Run: python3 build.py       (demo, noindex)
Run: SITE_URL=https://your-confirmed-domain.hr python3 build.py  (production SEO)
"""
from pathlib import Path
from html import escape as h
import json,os,re
from urllib.parse import quote
from content import SERVICES,CATS
ROOT=Path(__file__).resolve().parent; DIST=ROOT/'dist';DIST.mkdir(exist_ok=True)
SITE_URL=os.environ.get('SITE_URL','').strip().rstrip('/')
if SITE_URL and not SITE_URL.startswith('https://'): raise ValueError('SITE_URL must start with https://')
HR='hr';EN='en'
SLUGS={
 'home':('',''),'services':('usluge','treatments'),'about':('o-nama','about'),
 'gallery':('galerija','gallery'),'pricing':('cjenik','pricing'),
 'booking':('rezervacije','booking'),'contact':('kontakt','contact'),
 'privacy':('privatnost','privacy'),'cookies':('kolacici','cookies'),
 'legal':('pravne-informacije','legal')}
T={
'hr':{'nav_home':'Početna','nav_services':'Tretmani','nav_about':'O nama','nav_gallery':'Galerija','nav_pricing':'Cjenik','nav_contact':'Kontakt','book':'Rezervirajte termin','discover':'Otkrijte tretmane','opening':'USKORO OTVARANJE · ZAGREB','tagline':'Ljepota počinje njegom.','hero_label':'SKINLOGIC · BEAUTY & SKINCARE','hero_more':'Istražite našu ponudu','scroll':'ISTRAŽITE','eyebrow_services':'NAŠ SVIJET NJEGE','services_head':'Njega koja slavi vašu prirodnu ljepotu.','services_intro':'Od njege lica do oblikovanja obrva i estetskih tretmana — otkrijte ponudu koja počinje razumijevanjem vaših želja.','all_treatments':'Svi tretmani','read_more':'Saznajte više','eyebrow_about':'NAŠA FILOZOFIJA','about_head':'Ljepota je u detaljima.','about_intro':'Skinlogic zamišljamo kao mjesto pažljive njege, suvremenog pristupa i prostora u kojem se možete posvetiti sebi.','about_cta':'Upoznajte Skinlogic','eyebrow_manifesto':'SKINLOGIC EXPERIENCE','manifesto':'Svaki detalj ima svoju priču. Svaki tretman počinje razgovorom.','eyebrow_gallery':'VIZUALNI SVIJET SKINLOGIC','gallery_head':'Trenuci posvećeni sebi.','gallery_desc':'Atmosfera koju stvaramo — nježne teksture, toplo svjetlo i pažnja prema svakom detalju.','ai_note':'Prikazane fotografije su AI ilustracije zamišljenog ambijenta i tretmana; nisu fotografije stvarnog salona ni rezultata klijenata.','eyebrow_contact':'PRONAĐITE NAS','contact_title':'Vaš trenutak njege počinje ovdje.','contact_intro':'Veselimo se vašem upitu. Termin potvrđujemo nakon izravnog dogovora.','address_label':'ADRESA','hours_label':'RADNO VRIJEME','hours_soon':'Objavljujemo uskoro','phone_label':'TELEFON','coming_soon':'Podaci uskoro','email_label':'E-MAIL','directions':'Upute za dolazak','eyebrow_booking':'VAŠ TRENUTAK','booking_head':'Zatražite svoj termin.','booking_intro':'Pošaljite nam željeni tretman i datum. Odgovorit ćemo vam nakon što salon aktivira zaprimanje upita. Slanje obrasca nije automatska potvrda termina.','name':'Ime i prezime','phone':'Broj telefona','email':'E-mail adresa','treatment':'Odaberite tretman','date':'Željeni datum','note':'Napomena (neobavezno)','send':'Pošaljite upit','privacy_consent':'Razumijem da će se navedeni podaci koristiti za odgovor na moj upit i pročitao/la sam','privacy_page':'Politiku privatnosti','form_inactive':'Online slanje bit će dostupno nakon što se poveže službena e-mail adresa salona. Ovo je demonstracijska verzija obrasca.','form_error':'Upit trenutačno nije moguće poslati. Pokušajte kasnije.','form_success':'Upit je uspješno poslan. Salon će vam odgovoriti na dostavljene kontakt podatke.','form_processing':'Šaljemo…','visit_us':'Ilica 99, Zagreb','map_intro':'Interaktivna Google karta učitava se na vaš zahtjev.','load_map':'Prikaži Google kartu','map_extern':'Otvorite Google Maps','eyebrow_pricing':'PREGLED CIJENA','pricing_head':'Cjenik tretmana.','pricing_intro':'Cjenik je u pripremi i bit će objavljen nakon potvrde salona. Navedene usluge ne sadrže izmišljene cijene.','price_soon':'Cijena uskoro','duration_soon':'Trajanje se potvrđuje pri upitu','faq':'Česta pitanja','benefits':'Što možete očekivati','approach':'O tretmanu','how_it_works':'Kako pristupamo tretmanu','prep':'Prije i nakon tretmana','prep_text':'Prije dolaska preporučujemo kratke konzultacije o potrebama kože i eventualnim ograničenjima. Točne upute za pripremu i njegu nakon tretmana ovise o metodi i potvrđuje ih salon.','other_services':'Otkrijte i druge tretmane','treatment_cta':'Zainteresirani za ovaj tretman?','treatment_cta_text':'Pošaljite upit za termin ili dodatne informacije.','form_disclaimer':'Za potvrdu termina potrebno je pričekati povratnu informaciju salona.','no_reviews':'Recenzije stvarnih klijenata objavit ćemo nakon otvaranja i uz odgovarajuće dopuštenje.','all':'Svi tretmani','face':'Njega lica','brows':'Obrve i trepavice','aesthetics':'Estetski tretmani','eyebrow_story':'DOBRO DOŠLI U SKINLOGIC','story_head':'Prostor u kojem se ljepota susreće s pažnjom.','story_one':'Skinlogic je novi beauty koncept na adresi Ilica 99 u Zagrebu. Naša je vizija povezati elegantan prostor, individualan pristup i informiran odabir njege kože.','story_two':'Vjerujemo u promišljene rituale njege, jasne informacije o tretmanima i slobodu da odaberete ono što odgovara vašim potrebama. Ponuda je osmišljena tako da obuhvati tretmane lica, obrva i trepavica te estetske postupke.','values_title':'Ono što nam je važno','value1':'Pažnja u svakom detalju','value1_desc':'Ugodno i jasno iskustvo od prvog upita.','value2':'Individualan pristup','value2_desc':'Svaka koža i svaka osoba imaju svoje potrebe.','value3':'Povjerenje i transparentnost','value3_desc':'Bez nerealnih obećanja, uz otvorenu komunikaciju.','faq1':'Kako rezervirati termin?','faqa1':'Ispunite obrazac za upit. Kad salon potvrdi dostupnost kontakata i zaprimanje, odgovorom će dogovoriti termin.','faq2':'Jesu li cijene već dostupne?','faqa2':'Cjenik će biti objavljen nakon što ga salon potvrdi.','faq3':'Gdje se salon nalazi?','faqa3':'Skinlogic se nalazi na adresi Ilica 99 u Zagrebu.','faq4':'Kako znam koji je tretman za mene?','faqa4':'Za odabir tretmana preporučujemo savjetovanje s osobljem salona, osobito kod postupaka koji zahtijevaju procjenu kože.','footer_line':'Ljepota počinje njegom.','footer_visit':'POSJETITE NAS','footer_explore':'ISTRAŽITE','footer_contact':'KONTAKT','footer_legal':'PRAVNE INFORMACIJE','legal_notice':'Informacije za klijente','copyright':'Sva prava pridržana.','made':'Dizajn i razvoj','cookie_title':'Vaša privatnost nam je važna','cookie_text':'Koristimo nužnu lokalnu pohranu za izbor privola. Analitičke i marketinške alate nećemo učitavati bez vaše dozvole.','accept_all':'Prihvati sve','reject':'Odbij neobavezne','settings':'Postavke','save':'Spremi odabir','necessary':'Nužno','analytics':'Analitika','marketing':'Marketing','always':'Uvijek aktivno','preferences':'Postavke privatnosti','menu':'Otvori izbornik','close':'Zatvori','privacy_title':'Politika privatnosti','cookies_title':'Politika kolačića','legal_title':'Pravne informacije','legal_draft':'PREDLOŽAK ZA DOPUNU — prije službene objave potrebno je upisati podatke poslovnog subjekta i pravno provjeriti sadržaj.','legal_entity':'Podaci o poslovnom subjektu','legal_missing':'Puni registrirani naziv, OIB, sjedište, službeni e-mail i druge obvezne informacije bit će upisani nakon potvrde vlasnice.','privacy_scope':'Obrada osobnih podataka','privacy_body':'U obrascu se mogu prikupljati ime, telefon, e-mail, željeni tretman, datum i napomena radi odgovora na upit i dogovora termina. Detalje voditelja obrade, pravnih osnova, primatelja podataka, rokova pohrane i ostvarivanja prava treba potvrditi prije uključivanja obrasca. Nepotpvrđene podatke ne treba izmišljati.','privacy_rights':'Prava posjetitelja','privacy_rights_body':'Posjetitelji mogu ostvarivati prava predviđena primjenjivim propisima o zaštiti osobnih podataka, uključujući pristup, ispravak, brisanje i prigovor kada je primjenjivo. Kontakt voditelja obrade bit će objavljen nakon potvrde.','cookies_body':'Nužna lokalna pohrana čuva izbor o privolama. Analitički i marketinški alati u ovoj demo verziji nisu aktivni. Ako se aktiviraju, počet će raditi samo nakon odgovarajuće privole, uz ažuriranje ove politike.','cookies_manage':'Promijenite postavke kolačića','price_note':'Trajanje, prikladnost i cijene tretmana potvrđuje salon.','image_note_small':'AI ilustracija · stvarne fotografije salona naknadno.','notfound':'Stranica nije pronađena','back_home':'Povratak na početnu','seo_desc':'Skinlogic — kozmetički salon na adresi Ilica 99, Zagreb. Tretmani njege lica, obrva i trepavica te estetski tretmani. Otvaranje uskoro.'},
'en':{'nav_home':'Home','nav_services':'Treatments','nav_about':'About','nav_gallery':'Gallery','nav_pricing':'Pricing','nav_contact':'Contact','book':'Request an appointment','discover':'Explore treatments','opening':'OPENING SOON · ZAGREB','tagline':'Beauty begins with care.','hero_label':'SKINLOGIC · BEAUTY & SKINCARE','hero_more':'Explore our services','scroll':'DISCOVER','eyebrow_services':'OUR WORLD OF CARE','services_head':'Care that celebrates your natural beauty.','services_intro':'From facials and brows to aesthetic treatments — discover services built around understanding your needs.','all_treatments':'All treatments','read_more':'Discover more','eyebrow_about':'OUR PHILOSOPHY','about_head':'Beauty is in the details.','about_intro':'Skinlogic is envisioned as a place of considered care, a modern approach and time dedicated to yourself.','about_cta':'Discover Skinlogic','eyebrow_manifesto':'SKINLOGIC EXPERIENCE','manifesto':'Every detail tells a story. Every treatment begins with a conversation.','eyebrow_gallery':'THE SKINLOGIC WORLD','gallery_head':'Moments made for yourself.','gallery_desc':'The atmosphere we imagine — soft textures, warm light and attention to detail.','ai_note':'These images are AI illustrations of an imagined interior and treatments; they do not depict the actual salon or real client results.','eyebrow_contact':'FIND US','contact_title':'Your moment of care begins here.','contact_intro':'We look forward to your enquiry. Appointments are confirmed only after direct agreement.','address_label':'ADDRESS','hours_label':'OPENING HOURS','hours_soon':'To be announced','phone_label':'PHONE','coming_soon':'Details coming soon','email_label':'EMAIL','directions':'Get directions','eyebrow_booking':'YOUR MOMENT','booking_head':'Request your appointment.','booking_intro':'Send us your preferred treatment and date. We can respond once the salon activates enquiries. Submitting an enquiry does not automatically confirm an appointment.','name':'Full name','phone':'Phone number','email':'Email address','treatment':'Choose a treatment','date':'Preferred date','note':'Note (optional)','send':'Send enquiry','privacy_consent':'I understand these details will be used to answer my enquiry and I have read the','privacy_page':'Privacy Policy','form_inactive':'Online enquiries will become available once the salon’s official email is connected. This is a demonstration form.','form_error':'Unable to send your enquiry right now. Please try again later.','form_success':'Your enquiry has been sent. The salon will reply using the contact details provided.','form_processing':'Sending…','visit_us':'Ilica 99, Zagreb','map_intro':'The interactive Google map is loaded only on request.','load_map':'Show Google Map','map_extern':'Open Google Maps','eyebrow_pricing':'PRICE OVERVIEW','pricing_head':'Treatment pricing.','pricing_intro':'Pricing will be published after confirmation from the salon. No prices have been invented.','price_soon':'Price coming soon','duration_soon':'Duration confirmed on enquiry','faq':'Frequently asked questions','benefits':'What to expect','approach':'About the treatment','how_it_works':'Our approach','prep':'Before and after your treatment','prep_text':'A brief consultation about your skin needs and any relevant limitations is recommended. Preparation and aftercare depend on the exact technique and must be confirmed by the salon.','other_services':'Discover other treatments','treatment_cta':'Interested in this treatment?','treatment_cta_text':'Send an enquiry about availability or further details.','form_disclaimer':'Please await direct confirmation of your appointment from the salon.','no_reviews':'Genuine client reviews can be displayed after opening and with the necessary permissions.','all':'All treatments','face':'Facials','brows':'Brows & lashes','aesthetics':'Aesthetics','eyebrow_story':'WELCOME TO SKINLOGIC','story_head':'Where beauty meets thoughtful care.','story_one':'Skinlogic is a new beauty concept at Ilica 99 in Zagreb. Our vision brings together an elegant setting, an individual approach and informed skincare choices.','story_two':'We believe in thoughtful beauty rituals, clear information and the freedom to choose care that suits your needs. Our range spans facial care, brows and lashes, and aesthetic procedures.','values_title':'What matters to us','value1':'Attention to every detail','value1_desc':'A welcoming, clear experience from your first enquiry.','value2':'An individual approach','value2_desc':'Every person and every skin has different needs.','value3':'Trust and transparency','value3_desc':'No unrealistic promises, just open communication.','faq1':'How do I book an appointment?','faqa1':'Complete an enquiry form. Once enquiries are enabled, the salon can respond and agree on a time with you.','faq2':'Are prices available?','faqa2':'Pricing will be published after confirmation from the salon.','faq3':'Where are you located?','faqa3':'Skinlogic is located at Ilica 99 in Zagreb.','faq4':'Which treatment is right for me?','faqa4':'We recommend discussing your needs with the salon, especially for treatments requiring a skin suitability assessment.','footer_line':'Beauty begins with care.','footer_visit':'VISIT US','footer_explore':'EXPLORE','footer_contact':'CONTACT','footer_legal':'LEGAL','legal_notice':'Information for clients','copyright':'All rights reserved.','made':'Design & development','cookie_title':'Your privacy matters','cookie_text':'Essential local storage saves your consent choices. Analytics and marketing tools will not load without your consent.','accept_all':'Accept all','reject':'Reject optional','settings':'Preferences','save':'Save choices','necessary':'Essential','analytics':'Analytics','marketing':'Marketing','always':'Always enabled','preferences':'Privacy preferences','menu':'Open menu','close':'Close','privacy_title':'Privacy Policy','cookies_title':'Cookie Policy','legal_title':'Legal Information','legal_draft':'DRAFT — the business identity and legal terms must be completed and verified before public launch.','legal_entity':'Business information','legal_missing':'Full registered business name, tax identifier (OIB), registered office, official email and other mandatory details will be added after confirmation from the owner.','privacy_scope':'Processing of personal data','privacy_body':'The enquiry form may collect name, phone, email, desired treatment, preferred date and notes to respond to enquiries and arrange appointments. The identity of the controller, lawful bases, recipients, retention periods and rights must be confirmed before enabling the form. Unconfirmed information should never be invented.','privacy_rights':'Visitor rights','privacy_rights_body':'Visitors can exercise their rights under applicable data protection laws, including access, correction, erasure and objection where applicable. Contact details for the controller will be published once confirmed.','cookies_body':'Essential local storage keeps your consent choice. Analytics and marketing are disabled in this demo. If enabled in future, they will only start after appropriate consent, and this policy must be updated.','cookies_manage':'Change cookie preferences','price_note':'Treatment suitability, duration and prices are confirmed by the salon.','image_note_small':'AI illustration · real salon photos to be added later.','notfound':'Page not found','back_home':'Return home','seo_desc':'Skinlogic beauty salon at Ilica 99, Zagreb. Facials, brows, lashes and aesthetic treatments. Opening soon.'}
}

EN_SERVICE_SLUGS={'kemijski-pilinzi':'chemical-peels','ciscenje-lica':'facial-cleansing','bukalna-masaza':'buccal-massage','trajna-sminka-usana':'permanent-lip-makeup','trajna-sminka-obrva':'permanent-brow-makeup','kamuflaza-oziljaka-i-strija':'scar-stretch-mark-camouflage'}
def path(lang,key='home',slug=None):
 if slug:
  local_slug=slug if lang=='hr' else EN_SERVICE_SLUGS.get(slug,slug)
  return f'/{lang}/{"tretmani" if lang=="hr" else "treatments"}/{local_slug}/'
 v=SLUGS[key][0 if lang=='hr' else 1]
 return f'/{lang}/{v+"/" if v else ""}'
def src(name):return '/assets/'+name+'.avif'
def a(href,text,cls='',extra=''):return f'<a href="{href}" class="{cls}" {extra}>{text}</a>'
def brk(txt):return h(txt)
def img(name,alt='',loading='lazy',css=''):
 return f'<img src="{src(name)}" alt="{h(alt)}" loading="{loading}" decoding="async" class="{css}" width="800" height="600">'
def e(tag,cls,text):return f'<{tag} class="{cls}">{text}</{tag}>'
def c(lang,key):return T[lang][key]

def icon(name):
 icons={
 'arrow':'<path d="M4 12h16m-6-6 6 6-6 6"/>',
 'arrowup':'<path d="M7 17 17 7M8 7h9v9"/>',
 'pin':'<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
 'sparkle':'<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5L12 2Z"/>',
 'heart':'<path d="M20.8 4.6a5.7 5.7 0 0 0-8.1 0L12 5.3l-.7-.7a5.7 5.7 0 0 0-8.1 8.1 5.7 0 0 0 0 8.1L12 21l8.8-8.3a5.7 5.7 0 0 0 0-8.1Z"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.4 1.4m11.34 11.34 1.4 1.4M2 12h2m16 0h2M4.93 19.07l1.4-1.4M17.67 6.33l1.4-1.4"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/>',
 'phone':'<path d="M21 16.4v3a2 2 0 0 1-2.2 2A18 18 0 0 1 2.6 5.2 2 2 0 0 1 4.6 3h3a2 2 0 0 1 2 1.7l.5 2.5a2 2 0 0 1-.6 1.9L7.9 10.7a14 14 0 0 0 5.4 5.4l1.6-1.6a2 2 0 0 1 1.9-.6l2.5.5a2 2 0 0 1 1.7 2.1Z"/>',
 'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m3 6 9 7 9-7"/>',
 'check':'<path d="m4 12 5 5L20 6"/>',
 'leaf':'<path d="M20 4c-9 0-16 2-16 11a5 5 0 0 0 5 5c9 0 11-7 11-16Z"/><path d="M4 20c4-5 7-8 13-11"/>',
 'instagram':'<rect width="20" height="20" x="2" y="2" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
 'menu':'<path d="M3 7h18M3 12h18M3 17h18"/>',
 'close':'<path d="M5 5 19 19M19 5 5 19"/>',
 'chevron':'<path d="m6 9 6 6 6-6"/>',
 }
 return '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round">'+icons.get(name,icons['sparkle'])+'</svg>'

def button(href,text,style='primary',more=''):
 return a(href,h(text)+' <span class="button-arrow">'+icon('arrow')+'</span>',f'button button--{style}',more)

def heading(label,title,description='',align='left'):
 return f'<div class="section-heading section-heading--{align}" data-reveal><p class="eyebrow"><span></span>{h(label)}</p><h2 class="display-title">{h(title)}</h2>'+(f'<p class="section-description">{h(description)}</p>' if description else '')+'</div>'

def page_title(label,title,description='',image=None):
 if image:
  return f'<section class="inner-hero inner-hero--photo"><div class="inner-hero-image">{img(image,title,"eager")}</div><div class="inner-hero-shade"></div><div class="container inner-hero-inner" data-reveal><p class="eyebrow eyebrow--light">{h(label)}</p><h1>{h(title)}</h1><p>{h(description)}</p></div></section>'
 return f'<section class="inner-hero inner-hero--plain"><div class="container inner-hero-inner" data-reveal><p class="eyebrow">{h(label)}</p><h1>{h(title)}</h1><p>{h(description)}</p><div class="hero-ornament">✺</div></div></section>'

def card(lang,s,index=0):
 title=s[lang];short=s[f'{lang}_short'];link=path(lang,'services',s['slug'])
 return f'<article class="treatment-card" data-category="{s["category"]}" data-reveal style="--d:{(index%4)*80}ms"><a href="{link}" class="treatment-card-media" aria-label="{h(title)}">{img(s["image"],title)}<span class="card-index">{index+1:02d}</span><span class="card-link-icon">{icon("arrowup")}</span></a><div class="card-copy"><p class="card-category">{h(CATS[s["category"]][lang])}</p><h3><a href="{link}">{h(title)}</a></h3><p>{h(short)}</p><a class="text-link" href="{link}">{h(c(lang,"read_more"))} {icon("arrow")}</a></div></article>'

def cards(lang,services=None):
 return '<div class="treatments-grid">'+''.join(card(lang,s,i) for i,s in enumerate(services or SERVICES))+'</div>'

def logo():return '<span class="logo-title">SKINLOGIC</span><span class="logo-sub">BEAUTY &amp; SKINCARE</span>'

def header(lang,active='home'):
 links=[('home','nav_home'),('services','nav_services'),('about','nav_about'),('gallery','nav_gallery'),('pricing','nav_pricing'),('contact','nav_contact')]
 nav=''.join(a(path(lang,key),h(c(lang,label)), 'nav-link'+(' is-current' if key==active else ''),('aria-current="page"' if key==active else '')) for key,label in links)
 other='en' if lang=='hr' else 'hr'
 # per-page language path is handled inside layout()
 return f'''<header class="site-header" id="site-header"><div class="nav-wrap"><a class="brand brand--header" href="{path(lang)}" aria-label="Skinlogic — {c(lang,'nav_home')}">{logo()}</a><nav class="desktop-nav" aria-label="Main navigation">{nav}</nav><div class="nav-right"><div class="lang-switch" id="desktop-languages"></div>{a(path(lang,'booking'),h(c(lang,'book')),'nav-book')}<button class="menu-toggle" type="button" aria-label="{h(c(lang,'menu'))}" aria-controls="mobile-navigation" aria-expanded="false"><span></span><span></span></button></div></div></header><div class="mobile-panel" id="mobile-navigation" aria-hidden="true"><nav class="mobile-links" aria-label="Mobile navigation">{nav}{a(path(lang,'booking'),h(c(lang,'book')),'mobile-book')}</nav><div class="mobile-bottom"><span>SKINLOGIC · ZAGREB</span><span class="mobile-language" id="mobile-languages"></span></div></div>'''

def footer(lang):
 z=T[lang]
 nav=''.join(a(path(lang,key),h(z[label])) for key,label in [('home','nav_home'),('services','nav_services'),('about','nav_about'),('gallery','nav_gallery'),('pricing','nav_pricing'),('contact','nav_contact')])
 legal=''.join(a(path(lang,key),h(z[label])) for key,label in [('privacy','privacy_title'),('cookies','cookies_title'),('legal','legal_title')])
 return f'''<footer class="site-footer"><div class="footer-graphic" aria-hidden="true">SKINLOGIC</div><div class="container"><div class="footer-top"><div class="footer-brand"><a href="{path(lang)}" class="brand">{logo()}</a><p>{h(z['footer_line'])}</p><p class="footer-address">Ilica 99 · Zagreb</p></div><div class="footer-col"><h3>{h(z['footer_explore'])}</h3>{nav}</div><div class="footer-col"><h3>{h(z['footer_contact'])}</h3><a href="https://www.google.com/maps/search/?api=1&amp;query=Ilica+99+Zagreb" target="_blank" rel="noopener noreferrer">Ilica 99, Zagreb {icon('arrowup')}</a>{a(path(lang,'booking'),h(z['book']))}</div><div class="footer-col"><h3>{h(z['footer_legal'])}</h3>{legal}<button type="button" class="footer-privacy-link" data-open-consent>{h(z['settings'])}</button></div></div><div class="footer-bottom"><span>© <span id="year">2026</span> Skinlogic. {h(z['copyright'])}</span><span>{h(z['made'])} — Medium29</span></div></div></footer>'''

def consent_ui(lang):
 z=T[lang]
 return f'''<div class="cookie-banner" id="cookie-banner" hidden role="dialog" aria-modal="false" aria-label="{h(z['cookie_title'])}"><div class="cookie-content"><div><p class="eyebrow">SKINLOGIC · PRIVACY</p><h2>{h(z['cookie_title'])}</h2><p>{h(z['cookie_text'])} {a(path(lang,'cookies'),h(z['cookies_title']))}</p></div><div class="cookie-actions"><button class="button button--primary" data-consent="all">{h(z['accept_all'])}</button><button class="button button--ghost" data-consent="essential">{h(z['reject'])}</button><button class="button button--underlined" data-open-consent>{h(z['settings'])}</button></div></div></div><dialog class="consent-dialog" id="consent-dialog" aria-labelledby="consent-title"><div class="consent-body"><button class="dialog-close" type="button" data-close-consent aria-label="{h(z['close'])}">{icon('close')}</button><p class="eyebrow">SKINLOGIC · PRIVACY</p><h2 id="consent-title">{h(z['preferences'])}</h2><p>{h(z['cookie_text'])}</p><label class="preference-row"><span><strong>{h(z['necessary'])}</strong><small>{h(z['always'])}</small></span><input type="checkbox" checked disabled></label><label class="preference-row"><span><strong>{h(z['analytics'])}</strong></span><input id="consent-analytics" type="checkbox"></label><label class="preference-row"><span><strong>{h(z['marketing'])}</strong></span><input id="consent-marketing" type="checkbox"></label><button type="button" class="button button--primary" data-save-consent>{h(z['save'])} {icon('check')}</button></div></dialog>'''

def intro(lang):
 return '<div class="intro-overlay" id="intro-overlay" aria-hidden="true"><div class="intro-center"><span class="intro-brand">SKINLOGIC</span><span class="intro-rule"></span><span class="intro-sub">BEAUTY &amp; SKINCARE · ZAGREB</span></div></div>'

def language_target(lang,key,slug=None):
 return path('en' if lang=='hr' else 'hr',key,slug)

def layout(lang,key,title,description,body,slug=None,image='salon-hero'):
 page_path=path(lang,key,slug);other=language_target(lang,key,slug)
 seo_title=f'{title} | Skinlogic Zagreb' if key!='home' else ('Skinlogic — Ljepota počinje njegom. | Kozmetički salon Zagreb' if lang=='hr' else 'Skinlogic — Beauty begins with care. | Beauty salon Zagreb')
 og=h(description); meta_robots='index,follow' if SITE_URL else 'noindex,nofollow'
 seo_meta=(f'<link rel="canonical" href="{SITE_URL+page_path}"><link rel="alternate" hreflang="hr" href="{SITE_URL+path("hr",key,slug)}"><link rel="alternate" hreflang="en" href="{SITE_URL+path("en",key,slug)}"><link rel="alternate" hreflang="x-default" href="{SITE_URL+path("hr",key,slug)}">' if SITE_URL else '')
 metadata={'@context':'https://schema.org','@type':'BeautySalon','name':'Skinlogic','address':{'@type':'PostalAddress','streetAddress':'Ilica 99','addressLocality':'Zagreb','addressCountry':'HR'},'description':description}
 if SITE_URL:metadata['url']=SITE_URL+path(lang)
 ld=f'<script type="application/ld+json">{json.dumps(metadata,ensure_ascii=False)}</script>' if key in ('home','contact') else ''
 nav=header(lang,key if not slug else 'services')
 language=f'<a href="{path("hr",key,slug)}" hreflang="hr" class="{"active" if lang=="hr" else ""}" aria-label="Hrvatski">HR</a><span aria-hidden="true">/</span><a href="{path("en",key,slug)}" hreflang="en" class="{"active" if lang=="en" else ""}" aria-label="English">EN</a>'
 nav=nav.replace('<div class="lang-switch" id="desktop-languages"></div>','<div class="lang-switch">'+language+'</div>').replace('<span class="mobile-language" id="mobile-languages"></span>','<span class="mobile-language">'+language+'</span>')
 data={'lang':lang,'bookingEnabled':os.environ.get('BOOKING_ENABLED')=='1','analyticsId':'','metaPixelId':''}
 # Access key and owner email are not known. No fake success responses.
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#F6F1E9"><meta name="description" content="{og}"><meta name="robots" content="{meta_robots}"><title>{h(seo_title)}</title>{seo_meta}<meta property="og:type" content="website"><meta property="og:title" content="{h(seo_title)}"><meta property="og:description" content="{og}"><meta property="og:image" content="{SITE_URL+src(image) if SITE_URL else src(image)}"><meta property="og:locale" content="{'hr_HR' if lang=='hr' else 'en_GB'}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&amp;family=Manrope:wght@400;500;600;700&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/styles.css"><noscript><style>.intro-overlay{{display:none}}[data-reveal]{{opacity:1;transform:none}}</style></noscript>{ld}</head><body class="page-{key}" data-lang="{lang}" data-page="{key}">{intro(lang)}{nav}<main id="main-content">{body}</main>{footer(lang)}{consent_ui(lang)}<script>window.SKINLOGIC_CONFIG={json.dumps(data,ensure_ascii=False)};</script><script src="/assets/site.js" defer></script></body></html>'''

def home(lang):
 z=T[lang]
 hero=f'''<section class="home-hero"><div class="hero-bg">{img('salon-hero','AI illustration of a warm beige beauty studio','eager')}</div><div class="hero-wash"></div><div class="hero-decoration" aria-hidden="true">S</div><div class="container hero-inner"><div class="hero-content"><p class="hero-overline">{h(z['opening'])}</p><h1 class="hero-title">SKINLOGIC</h1><p class="hero-tagline">{h(z['tagline'])}</p><span class="hero-divider"></span><p class="hero-small">{h(z['hero_label'])}</p><div class="hero-actions">{button(path(lang,'booking'),z['book'])}{a(path(lang,'services'),h(z['hero_more'])+' '+icon('arrow'),'hero-secondary')}</div></div></div><a href="#discover" class="scroll-prompt"><span>{h(z['scroll'])}</span><span class="scroll-line"></span></a><div class="hero-side-text" aria-hidden="true">{h("ILUSTRATIVNA AI VIZUALIZACIJA" if lang=="hr" else "ILLUSTRATIVE AI VISUAL")}</div></section>'''
 values=f'''<section class="value-strip"><div class="container value-strip-inner"><div>{icon('leaf')}<span>{h(z['value1'])}</span></div><div>{icon('sparkle')}<span>{h(z['value2'])}</span></div><div>{icon('heart')}<span>{h(z['value3'])}</span></div></div></section>'''
 about=f'''<section class="section intro-section" id="discover"><div class="container intro-grid"><div class="intro-art" data-reveal><div class="intro-photo">{img('beauty-portrait','Illustrative skincare beauty portrait')}</div><div class="intro-seal"><img src="/assets/seal.svg" alt="" width="120" height="120"></div><span class="photo-marker">SKINLOGIC / 01</span></div><div class="intro-text">{heading(z['eyebrow_about'],z['about_head'],z['about_intro'])}<div class="intro-extra" data-reveal><p>{h(z['story_one'])}</p>{button(path(lang,'about'),z['about_cta'],'outline')}</div></div></div></section>'''
 treatments=f'''<section class="section section-treatments" id="treatments"><div class="container"><div class="section-head-row">{heading(z['eyebrow_services'],z['services_head'],z['services_intro'])}<div data-reveal>{a(path(lang,'services'),h(z['all_treatments'])+' '+icon('arrow'),'text-link text-link--large')}</div></div>{cards(lang)}</div></section>'''
 editorial=f'''<section class="editorial-break"><div class="editorial-img">{img('beauty-care','Beauty care editorial image')}</div><div class="editorial-overlay"></div><div class="editorial-inner"><p class="eyebrow eyebrow--light">{h(z['eyebrow_manifesto'])}</p><h2>{h(z['manifesto'])}</h2>{button(path(lang,'booking'),z['book'],'light')}</div><div class="editorial-number">02 / SKINLOGIC</div></section>'''
 contact=f'''<section class="section home-contact"><div class="container home-contact-grid"><div>{heading(z['eyebrow_contact'],z['contact_title'],z['contact_intro'])}<div class="home-address">{icon('pin')}<div><span>{h(z['address_label'])}</span><strong>Ilica 99, Zagreb</strong></div></div><div class="home-address">{icon('clock')}<div><span>{h(z['hours_label'])}</span><strong>{h(z['hours_soon'])}</strong></div></div>{button(path(lang,'contact'),z['nav_contact'],'outline')}</div><div class="home-contact-picture" data-reveal>{img('salon-atmosphere','AI illustrated spa atmosphere')}<span class="picture-caption">SKINLOGIC · ZAGREB</span></div></div></section>'''
 faq=f'''<section class="section section-faq"><div class="container faq-layout"><div>{heading(z['faq'],z['faq'])}<p class="faq-intro">{h(z['contact_intro'])}</p></div><div class="faq-list">{faq_items([(z['faq1'],z['faqa1']),(z['faq2'],z['faqa2']),(z['faq3'],z['faqa3']),(z['faq4'],z['faqa4'])])}</div></div></section>'''
 return hero+values+about+treatments+editorial+contact+faq

def faq_items(faqs):
 return ''.join(f'<details class="faq-item"><summary><span>{h(q)}</span><span class="faq-plus">+</span></summary><div class="faq-answer">{h(ans)}</div></details>' for q,ans in faqs)

def services_page(lang):
 z=T[lang]
 hero=page_title(z['nav_services'],z['services_head'],z['services_intro'],'beauty-care')
 filters='<div class="filter-row" role="group" aria-label="'+h(z['nav_services'])+'">'+''.join(f'<button type="button" class="filter-btn {"active" if i==0 else ""}" data-filter="{key}">{h(z[label])}</button>' for i,(key,label) in enumerate([('all','all'),('face','face'),('brows','brows'),('aesthetics','aesthetics')]))+'</div>'
 return hero+f'<section class="section"><div class="container">{filters}{cards(lang)}</div></section>'+cta_band(lang)

def cta_band(lang):
 z=T[lang]
 return f'<section class="cta-band"><div class="container cta-band-inner"><div><p class="eyebrow">SKINLOGIC · ZAGREB</p><h2>{h(z["treatment_cta"])}</h2><p>{h(z["treatment_cta_text"])}</p></div>{button(path(lang,"booking"),z["book"],"light")}</div></section>'

def treatment_page(lang,s):
 z=T[lang];name=h(s[lang]);desc=h(s[f'{lang}_short']);story=h(s[f'{lang}_text']);l=lang
 bread=f'<nav class="breadcrumbs" aria-label="Breadcrumb">{a(path(lang),h(z["nav_home"]))}<span>/</span>{a(path(lang,"services"),h(z["nav_services"]))}<span>/</span><span>{name}</span></nav>'
 hero=f'''<section class="treatment-hero"><div class="container treatment-hero-grid"><div class="treatment-hero-text" data-reveal>{bread}<p class="eyebrow">{h(CATS[s['category']][lang])}</p><h1>{name}</h1><p class="treatment-summary">{desc}</p><div class="treatment-meta"><span>{icon('pin')} Ilica 99 · Zagreb</span><span>{icon('clock')} {h(z['duration_soon'])}</span></div>{button(path(lang,'booking')+'?treatment='+quote(s['slug']),z['book'])}</div><div class="treatment-hero-photo" data-reveal>{img(s['image'],s[lang],'eager')}<span class="photo-watermark">SKINLOGIC</span></div></div></section>'''
 benefits=''.join(f'<div class="benefit"><span>{icon("check")}</span><p>{h(t)}</p></div>' for t in s[f'{lang}_benefits'])
 main=f'''<section class="section treatment-copy"><div class="container treatment-body-grid"><div class="treatment-main"><p class="eyebrow">{h(z['approach'])}</p><h2 class="display-title">{name}</h2><p class="prose-lead">{story}</p><h3>{h(z['how_it_works'])}</h3><p>{h(z['prep_text'])}</p><div class="note-block"><span>{icon('sparkle')}</span><div><h3>{h(z['prep'])}</h3><p>{h(z['price_note'])}</p></div></div></div><aside class="treatment-aside"><div class="aside-card"><p class="eyebrow">SKINLOGIC · CARE</p><h3>{h(z['benefits'])}</h3>{benefits}<div class="aside-rule"></div><span class="price-unknown">{h(z['price_soon'])}</span>{button(path(lang,'booking')+'?treatment='+quote(s['slug']),z['book'],'outline')}</div></aside></div></section>'''
 faqs=[(z['faq4'],z['faqa4']),(z['faq2'],z['faqa2']),(z['faq1'],z['faqa1'])]
 faq=f'<section class="section section-faq"><div class="container faq-layout"><div>{heading(z["faq"],z["faq"])}</div><div class="faq-list">{faq_items(faqs)}</div></div></section>'
 related=[x for x in SERVICES if x['slug']!=s['slug'] and x['category']==s['category']][:2]
 related+= [x for x in SERVICES if x['slug']!=s['slug'] and x not in related][:max(0,3-len(related))]
 more=f'<section class="section section-related"><div class="container">{heading("SKINLOGIC",z["other_services"])}{cards(lang,related)}</div></section>'
 return hero+main+faq+more+cta_band(lang)

def about_page(lang):
 z=T[lang]
 return page_title(z['eyebrow_story'],z['story_head'],z['about_intro'],'salon-hero')+f'''<section class="section"><div class="container about-page-grid"><div class="about-page-picture" data-reveal>{img('salon-atmosphere','AI illustrated salon interior')}</div><div class="about-page-content">{heading(z['eyebrow_about'],z['about_head'])}<p>{h(z['story_one'])}</p><p>{h(z['story_two'])}</p>{button(path(lang,'services'),z['discover'],'outline')}</div></div></section><section class="section values-section"><div class="container">{heading('SKINLOGIC',z['values_title'])}<div class="values-grid"><article data-reveal>{icon('leaf')}<h3>{h(z['value1'])}</h3><p>{h(z['value1_desc'])}</p></article><article data-reveal>{icon('sparkle')}<h3>{h(z['value2'])}</h3><p>{h(z['value2_desc'])}</p></article><article data-reveal>{icon('heart')}<h3>{h(z['value3'])}</h3><p>{h(z['value3_desc'])}</p></article></div></div></section>'''+cta_band(lang)

def gallery_page(lang):
 z=T[lang]
 images=['salon-hero','beauty-portrait','salon-atmosphere','hydrafacial','dermapen','lash-lift','beauty-care','facial-cleansing','brow-lift','permanent-lips','mesoboost','buccal-massage']
 grid='<div class="masonry-gallery">'+''.join(f'<figure class="gallery-photo gallery-photo--{i%7}" data-reveal>{img(name,"AI illustrated skincare or beauty salon aesthetic")}<figcaption>SKINLOGIC · 0{i+1:02d}</figcaption></figure>' for i,name in enumerate(images))+'</div>'
 return page_title(z['eyebrow_gallery'],z['gallery_head'],z['gallery_desc'])+f'<section class="section"><div class="container">{grid}<p class="gallery-disclaimer">{icon("sparkle")} {h(z["ai_note"])}</p></div></section>'+cta_band(lang)

def pricing_page(lang):
 z=T[lang]
 groups=''
 for group in ['face','brows','aesthetics']:
  items=[s for s in SERVICES if s['category']==group]
  rows=''.join(f'<div class="pricing-row"><a href="{path(lang,"services",s["slug"])}">{h(s[lang])} {icon("arrowup")}</a><span>{h(z["price_soon"])}</span></div>' for s in items)
  groups+=f'<div class="price-category" data-reveal><div class="price-category-head"><p class="eyebrow">SKINLOGIC · MENU</p><h2>{h(CATS[group][lang])}</h2></div>{rows}</div>'
 return page_title(z['eyebrow_pricing'],z['pricing_head'],z['pricing_intro'])+f'<section class="section pricing-page"><div class="container pricing-grid"><div class="price-photo" data-reveal>{img("beauty-portrait","AI illustration of skincare portrait")}<span>SKINLOGIC · BEAUTY & SKINCARE</span></div><div class="price-list">{groups}</div></div></section>'+cta_band(lang)

def booking_form(lang):
 z=T[lang]
 opts='<option value="">'+h(z['treatment'])+'</option>'+''.join(f'<option value="{s["slug"]}">{h(s[lang])}</option>' for s in SERVICES)
 return f'''<form class="booking-form" id="booking-form" novalidate><div class="form-hp" aria-hidden="true"><label for="website">Leave this blank</label><input type="text" name="website" id="website" tabindex="-1" autocomplete="off"></div><div class="form-grid"><label>{h(z['name'])} *<input name="name" type="text" autocomplete="name" maxlength="100" required></label><label>{h(z['phone'])} *<input name="phone" type="tel" autocomplete="tel" maxlength="35" required></label><label>{h(z['email'])} *<input name="email" type="email" autocomplete="email" maxlength="180" required></label><label>{h(z['treatment'])} *<select name="treatment" required>{opts}</select></label><label>{h(z['date'])} *<input name="date" type="date" required></label><label class="form-wide">{h(z['note'])}<textarea name="note" rows="4" maxlength="1200"></textarea></label></div><label class="consent-label"><input type="checkbox" name="agreed" required><span>{h(z['privacy_consent'])} <a href="{path(lang,'privacy')}" target="_blank" rel="noopener noreferrer">{h(z['privacy_page'])}</a>.</span></label><p class="form-status form-status--notice" id="form-status" role="status">{h(z['form_inactive'])}</p><button class="button button--primary" id="submit-booking" type="submit" disabled>{h(z['send'])} {icon('arrow')}</button><p class="form-footnote">{h(z['form_disclaimer'])}</p></form>'''

def booking_page(lang):
 z=T[lang]
 return page_title(z['eyebrow_booking'],z['booking_head'],z['booking_intro'])+f'''<section class="section booking-section"><div class="container booking-layout"><div class="booking-panel"><p class="eyebrow">SKINLOGIC · REQUEST</p><h2 class="small-display">{h(z['booking_head'])}</h2>{booking_form(lang)}</div><aside class="booking-photo" data-reveal>{img("salon-atmosphere","AI illustrated beauty salon atmosphere")}<div class="booking-photo-overlay"><span>SKINLOGIC / ZAGREB</span><h3>{h(z['tagline'])}</h3><p>Ilica 99 · Zagreb</p></div></aside></div></section>'''

def contact_page(lang):
 z=T[lang]
 contact=f'''<section class="section"><div class="container contact-layout"><div class="contact-info">{heading(z['eyebrow_contact'],z['contact_title'],z['contact_intro'])}<div class="contact-detail">{icon('pin')}<div><span>{h(z['address_label'])}</span><strong>Ilica 99, Zagreb</strong><a target="_blank" rel="noopener noreferrer" href="https://www.google.com/maps/search/?api=1&amp;query=Ilica+99+Zagreb">{h(z['directions'])} {icon('arrowup')}</a></div></div><div class="contact-detail">{icon('clock')}<div><span>{h(z['hours_label'])}</span><strong>{h(z['hours_soon'])}</strong></div></div><div class="contact-detail">{icon('phone')}<div><span>{h(z['phone_label'])}</span><strong>{h(z['coming_soon'])}</strong></div></div><div class="contact-detail">{icon('mail')}<div><span>{h(z['email_label'])}</span><strong>{h(z['coming_soon'])}</strong></div></div>{button(path(lang,'booking'),z['book'])}</div><div class="contact-image" data-reveal>{img("salon-hero","AI illustrated salon interior")}</div></div></section>'''
 maps=f'<section class="map-section"><div class="container"><div class="map-panel" id="map-panel"><div class="map-before"><span>{icon("pin")}</span><h2>Ilica 99, Zagreb</h2><p>{h(z["map_intro"])}</p><button class="button button--outline" id="load-map">{h(z["load_map"])} {icon("arrow")}</button><a target="_blank" rel="noopener noreferrer" href="https://www.google.com/maps/search/?api=1&amp;query=Ilica+99+Zagreb">{h(z["map_extern"])} {icon("arrowup")}</a></div></div></div></section>'
 return page_title(z['nav_contact'],z['contact_title'],z['contact_intro'])+contact+maps

def legal_page(lang,key):
 z=T[lang]
 title=z[key+'_title']
 common=f'<div class="legal-notice">{icon("sparkle")} {h(z["legal_draft"])}</div>'
 if key=='privacy':
  contents=f'<h2>{h(z["legal_entity"])}</h2><p>{h(z["legal_missing"])}</p><h2>{h(z["privacy_scope"])}</h2><p>{h(z["privacy_body"])}</p><h2>{h(z["privacy_rights"])}</h2><p>{h(z["privacy_rights_body"])}</p>'
 elif key=='cookies':
  contents=f'<h2>{h(z["necessary"])}, {h(z["analytics"])}, {h(z["marketing"])}</h2><p>{h(z["cookies_body"])}</p><button class="button button--outline" data-open-consent>{h(z["cookies_manage"])}</button>'
 else:
  contents=f'<h2>{h(z["legal_entity"])}</h2><p>{h(z["legal_missing"])}</p><h2>{h(z["legal_notice"])}</h2><p>{h(z["legal_draft"])}</p>'
 return page_title('SKINLOGIC · LEGAL',title)+f'<section class="section legal-section"><div class="container"><div class="legal-text">{common}{contents}</div></div></section>'

def write(page,source):
 loc=DIST/page.lstrip('/')/'index.html';loc.parent.mkdir(parents=True,exist_ok=True);loc.write_text(source,encoding='utf-8')

def generate():
 import shutil
 for generated_lang in ("hr","en"):
  shutil.rmtree(DIST/generated_lang,ignore_errors=True)
 routes=[]
 for lang in ('hr','en'):
  z=T[lang]
  pages=[('home','Skinlogic',z['seo_desc'],home(lang)),('services',z['nav_services'],z['services_intro'],services_page(lang)),('about',z['nav_about'],z['story_one'],about_page(lang)),('gallery',z['nav_gallery'],z['gallery_desc'],gallery_page(lang)),('pricing',z['nav_pricing'],z['pricing_intro'],pricing_page(lang)),('booking',z['book'],z['booking_intro'],booking_page(lang)),('contact',z['nav_contact'],z['contact_intro'],contact_page(lang))]
  for key in ['privacy','cookies','legal']:pages.append((key,z[key+'_title'],z['legal_draft'],legal_page(lang,key)))
  for key,title,desc,body in pages:
   p=path(lang,key);write(p,layout(lang,key,title,desc,body));routes.append(p)
  for s in SERVICES:
   p=path(lang,'services',s['slug']);write(p,layout(lang,'services',s[lang],s[f'{lang}_short'],treatment_page(lang,s),s['slug'],s['image']));routes.append(p)
 # Root redirects to localized Croatian version, uses relative URL to retain nested deployment support.
  # Root: redirect at Cloudflare edge; real homepage as fallback on local servers.
  (DIST/'_redirects').write_text('/ /hr/ ' + ('301' if SITE_URL else '302') + '\\n', encoding='utf-8')
  hr_home = (DIST/'hr'/'index.html').read_text(encoding='utf-8')
  hr_home = hr_home.replace('</head>', '<link rel="canonical" href="/hr/"></head>', 1)
  (DIST/'index.html').write_text(hr_home, encoding='utf-8')
 (DIST/'404.html').write_text('<!doctype html><html lang="hr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>404 — Skinlogic</title><link rel="stylesheet" href="/assets/styles.css"></head><body><main class="not-found"><div><p class="eyebrow">404 / SKINLOGIC</p><h1>Stranica nije pronađena.</h1><p>Page not found.</p><a href="/hr/" class="button button--primary">Povratak na početnu ↗</a></div></main></body></html>',encoding='utf-8')
 if SITE_URL:
  from xml.sax.saxutils import escape as x
  urls='\n'.join(f'<url><loc>{x(SITE_URL+p)}</loc><changefreq>monthly</changefreq></url>' for p in routes)
  (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>',encoding='utf-8')
  (DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n',encoding='utf-8')
 else:
  (DIST/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
  (DIST/'sitemap.xml').unlink(missing_ok=True)
 # Security headers and caching policies for static sites
 (DIST/'_headers').write_text('''/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: DENY\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n/assets/*.avif\n  Cache-Control: public, max-age=31536000, immutable\n\n/assets/*.css\n  Cache-Control: public, max-age=3600\n\n/assets/*.js\n  Cache-Control: public, max-age=3600\n''',encoding='utf-8')
 print('Generated',len(routes),'localized pages + root + 404', 'PRODUCTION' if SITE_URL else 'DEMO/noindex')

if __name__=='__main__':generate()
