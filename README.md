# SKINLOGIC — Premium beauty salon website

**Verzija:** v1.0 / 12. listopada 2026.
**Izrada:** Medium29
**Lokacija salona:** Ilica 99, Zagreb

## Što je uključeno

- Premium responsive dizajn, bež/champagne/zlatne boje, elegantna serif tipografija.
- Lebdeći izbornik, mobilni menu, uvodna animacija loga, scroll animacije i efektne fotografske sekcije.
- Hrvatski i engleski jezik; **44 unaprijed generirane HTML stranice**.
- Početna, tretmani, o nama, galerija, cjenik, rezervacije, kontakt, privatnost, kolačići i pravne informacije u oba jezika.
- **12 pojedinačnih tretmana na oba jezika** (24 detaljne stranice).
- Interaktivno filtriranje tretmana, FAQ, galerija i Google karta na klik.
- Cookie consent banner s opcijama „Prihvati / Odbij / Postavke”. Analitika i Meta Pixel nisu aktivni.
- Lokalni SEO meta opisi za svaku stranicu, OpenGraph i osnovni BeautySalon schema podaci.
- AVIF slike ilustrativnih AI vizualizacija (bez vanjskih image CDN-ova).
- Cloudflare Pages Function za zaprimanje upita preko Resend servisa, **spremna za kasniju konfiguraciju**.

## VAŽNO — u ovoj verziji još nije aktivno

**Ne objavljivati kao konačnu stranicu dok vlasnica ne potvrdi:**

1. Službeni telefon, e-mail, WhatsApp broj, društvene mreže i radno vrijeme.
2. Cijene i trajanje svakog tretmana.
3. Točnu proceduru, opremu, kvalifikacije i napomene o tretmanima; tekstove treba stručno potvrditi.
4. Registrirani naziv poslovnog subjekta, OIB, e-mail voditelja obrade i ostale pravne podatke za politiku privatnosti, kolačića i pravne informacije. Pravne stranice su označene kao **nacrti**, a ne završeno pravno usklađenje.
5. Stvarni izgled salona: **sve slike u ovoj verziji nastale su iz AI-generiranih ilustrativnih vizuala**. Ne prikazuju stvarni interijer ili stvarne rezultate klijenata.
6. Konačnu domenu, nakon čega uključiti indeksiranje i generirati sitemap.
7. Konfiguraciju sustava e-mail upita; do tada je slanje namjerno onemogućeno i korisnik vidi obavijest.

## Pregled stranice bez instalacije

Sve gotove statičke datoteke nalaze se u mapi `dist/`.

**Najjednostavnije preko lokalnog računala:**

```bash
python -m http.server 8000 -d dist
```

Otvoriti `http://localhost:8000/hr/`. Poveznice unutar stranice rade lokalno. Za mobilni prikaz koristiti responsive način rada preglednika.

## Github + Cloudflare Pages

1. Napraviti novi GitHub repozitorij i uploadati **sadržaj ovog ZIP-a**, uključujući `dist`, `build.py`, `content.py`, `functions` i `README.md`.
2. Cloudflare Dashboard → **Workers & Pages** → Create → Pages → Connect to Git.
3. Framework preset: **None**.
4. Za **brzu demo objavu**, Build command ostaviti prazno; Build output directory: `dist`.
5. Za **automatsko generiranje pri svakoj promjeni**, Build command: `python3 build.py`; Output directory: `dist`.
6. Nakon deploya otvoriti dodijeljenu `*.pages.dev` adresu. Testni web je **noindex** i `/robots.txt` onemogućuje indeksiranje.

### Službena domena i SEO

Nakon odabira stvarne domene upisati u Cloudflare Pages environment variables:

```text
SITE_URL=https://STVARNA-POTVRDENA-DOMENA.HR
```

U build postavkama mora biti `python3 build.py`. Ponovno izvršiti deploy. Generator zatim izrađuje produkcijski sitemap, dopušta indeksiranje te generira canonical i hreflang oznake. **Ne upisivati izmišljenu ili nedostupnu domenu.** Prije puštanja live provjeriti točnost svih sadržaja, poveznica i robota.

## Aktivacija obrasca za rezervaciju

U početnoj isporuci `bookingEnabled` je `false`, gumb za slanje je onemogućen, i nema lažne potvrde upita. Za aktivaciju:

1. Vlasnica treba dostaviti adresu na koju stižu upiti.
2. Otvoriti Resend račun, provjeriti domenu pošiljatelja i konfigurirati DNS.
3. U Cloudflare Pages projektu dodati **Secrets/Environment Variables**:

```text
RESEND_API_KEY=...              # Secret; samo server-side
BOOKING_RECEIVER_EMAIL=...     # Vlasničina e-mail adresa
BOOKING_FROM_EMAIL=...         # npr. Skinlogic <rezervacije@vasa-provjerena-domena.hr>
BOOKING_ENABLED=1              # Environment variable u build okruženju
```

4. **Build command:** `python3 build.py`, pa novi deploy.
5. Testirati stvarno slanje i dostavu (uključujući spam mapu) nakon što sve bude konfigurirano.
6. Prije aktivacije ažurirati politiku privatnosti za upite, pružatelja e-mail usluge i rokove čuvanja podataka. Po potrebi uključiti Cloudflare Turnstile / zaštitu od neželjenih upita.

Cloudflare Pages Function nalazi se u `functions/api/booking.js`; `RESEND_API_KEY` **nikada** ne smije biti upisan u javni `site.js`.

## Gdje se uređuje sadržaj

- `content.py`: svi tretmani, nazivi, kratki opisi i tekstovi na HR/EN.
- `build.py`: ostali tekstovi, navigacija, struktura stranica i generator.
- `dist/assets/styles.css`: izgled, animacije, boje, mobilna prilagodba.
- `dist/assets/site.js`: izbornik, galerija/filteri, forma, karta, kolačići.
- `dist/assets/*.avif`: slike. Zamijeniti stvarnim odobrenim fotografijama čim stignu.
- `dist/assets/favicon.svg`: favicon.

Nakon izmjene tekstova, pokrenuti `python3 build.py` i uploadati/commitati promjene. Bez CMS-a, ali struktura se može kasnije povezati s CMS-om.

## Važne napomene o privatnosti i SEO-u

- U demo načinu stranice imaju `noindex,nofollow` i `Disallow: /` u robots.txt.
- Google Maps iframe se ne učitava automatski; posjetitelj ga aktivira klikom.
- Lokalna pohrana čuva postavke kolačića. Google Analytics i Meta Pixel nisu uključeni; prije aktivacije integrirati prave ID-eve i ažurirati sustav privola, uključujući opoziv suglasnosti.
- Tekstovi tretmana ne obećavaju rezultate; medicinski relevantne detalje i kontraindikacije treba potvrditi s kvalificiranom osobom.
- Generirane AI fotografije su ilustracije. Ne objavljivati ih pod opisima ili oglasima koji impliciraju da su stvarne fotografije objekta ili rezultata klijenata.

## Sadržaj projekta

```
SKINLOGIC_WEB_V1/
├── README.md
├── content.py
├── build.py
├── functions/api/booking.js
└── dist/
    ├── index.html
    ├── robots.txt
    ├── _headers
    ├── hr/ (22 stranice)
    ├── en/ (22 stranice)
    └── assets/ (CSS, JS, favicon, 16 AVIF ilustracija)
```
