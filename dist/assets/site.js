(() => {
  'use strict';
  const cfg = window.SKINLOGIC_CONFIG || {};
  const lang = document.body.dataset.lang === 'en' ? 'en' : 'hr';
  const tr = {
    hr: {
      success:'Upit je uspješno poslan. Salon će vam odgovoriti.',
      error:'Slanje upita nije uspjelo. Pokušajte kasnije.',
      sending:'Šaljemo upit…',
      invalid:'Provjerite unesene podatke i označite privolu.',
      formDisabled:'Online slanje bit će dostupno nakon što se poveže službena e-mail adresa salona. Ovo je demonstracijska verzija obrasca.'
    },
    en: {
      success:'Your enquiry was sent. The salon will get back to you.',
      error:'Unable to send your enquiry. Please try again later.',
      sending:'Sending your enquiry…',
      invalid:'Please check your details and tick the consent box.',
      formDisabled:'Online enquiries will become available once the salon’s official email is connected. This is a demonstration form.'
    }
  }[lang];
  const $ = (sel, scope = document) => scope.querySelector(sel);
  const $$ = (sel, scope = document) => Array.from(scope.querySelectorAll(sel));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Opening brand animation plays once per browser tab; it never delays every navigation.
  const intro = $('#intro-overlay');
  if (intro) {
    let seen = false;
    try { seen = sessionStorage.getItem('skinlogic_intro_seen') === '1'; sessionStorage.setItem('skinlogic_intro_seen','1'); } catch (_) {}
    const delay = reduced || seen ? 0 : 1450;
    window.setTimeout(() => {
      intro.classList.add('hide');
      window.setTimeout(() => intro.remove(), 740);
    }, delay);
  }

  const header = $('#site-header');
  const updateHeader = () => header && header.classList.toggle('scrolled', window.scrollY > 30);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  const menu = $('.menu-toggle');
  const mobilePanel = $('#mobile-navigation');
  const closeMenu = () => {
    document.body.classList.remove('menu-open');
    menu?.setAttribute('aria-expanded','false');
    mobilePanel?.setAttribute('aria-hidden','true');
  };
  menu?.addEventListener('click', () => {
    const open = !document.body.classList.contains('menu-open');
    document.body.classList.toggle('menu-open',open);
    menu.setAttribute('aria-expanded', String(open));
    mobilePanel?.setAttribute('aria-hidden',String(!open));
  });
  $$('.mobile-panel a').forEach(el => el.addEventListener('click',closeMenu));
  window.addEventListener('keydown', e => { if(e.key === 'Escape') closeMenu(); });

  // Scroll reveal (honours OS reduced-motion preference).
  if (!reduced && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target);}
      });
    },{threshold:0.09,rootMargin:'0px 0px -25px 0px'});
    $$('[data-reveal]').forEach(el=>observer.observe(el));
  } else {
    $$('[data-reveal]').forEach(el=>el.classList.add('is-visible'));
  }

  // Service listing filters: no missing or phantom treatments.
  const filters = $$('.filter-btn');
  filters.forEach(btn=>btn.addEventListener('click',()=>{
    const filter=btn.dataset.filter;
    filters.forEach(b=>{b.classList.toggle('active',b===btn);b.setAttribute('aria-pressed',String(b===btn));});
    $$('.treatment-card[data-category]').forEach(el=>el.classList.toggle('is-hidden',filter!=='all'&&el.dataset.category!==filter));
  }));
  filters.forEach((b,i)=>b.setAttribute('aria-pressed', String(i===0)));

  // Load third-party Google Maps only after an explicit click.
  const mapBtn = $('#load-map');
  mapBtn?.addEventListener('click',()=>{
    const panel=$('#map-panel');
    if(!panel)return;
    const iframe=document.createElement('iframe');
    iframe.title=lang==='hr'?'Karta: Ilica 99, Zagreb':'Map: Ilica 99, Zagreb';
    iframe.src='https://www.google.com/maps?q='+encodeURIComponent('Ilica 99, Zagreb, Croatia')+'&output=embed';
    iframe.loading='lazy';
    iframe.referrerPolicy='no-referrer-when-downgrade';
    iframe.setAttribute('allowfullscreen','');
    panel.replaceChildren(iframe);
  });

  // Demo form remains visibly disabled until the salon provides a verified receiver email
  // and the deploy owner enables Cloudflare Pages Functions with Resend env vars.
  const form = $('#booking-form');
  if(form){
    const send = $('#submit-booking');
    const status = $('#form-status');
    const date = $('input[name="date"]',form);
    if(date){const today=new Date();today.setMinutes(today.getMinutes()-today.getTimezoneOffset());date.min=today.toISOString().slice(0,10);}
    const incoming = new URLSearchParams(location.search).get('treatment');
    if(incoming){const sel=$('select[name="treatment"]',form);if(sel && [...sel.options].some(opt=>opt.value===incoming))sel.value=incoming;}
    if(cfg.bookingEnabled === true){
      if(send)send.disabled=false;
      if(status)status.hidden=true;
    } else if(status){status.textContent=tr.formDisabled;}
    form.addEventListener('submit', async event=>{
      event.preventDefault();
      if(!cfg.bookingEnabled)return;
      if(!form.reportValidity()) {if(status){status.textContent=tr.invalid;status.hidden=false;status.className='form-status form-status--error';}return;}
      const fields=Object.fromEntries(new FormData(form).entries());
      if(fields.website)return;
      if(send)send.disabled=true;
      if(status){status.hidden=false;status.className='form-status form-status--notice';status.textContent=tr.sending;}
      try{
        const response=await fetch('/api/booking',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...fields,language:lang}),credentials:'same-origin'});
        if(!response.ok)throw new Error('request_failed');
        if(status){status.className='form-status form-status--success';status.textContent=tr.success;}
        form.reset();
      }catch(e){if(status){status.className='form-status form-status--error';status.textContent=tr.error;}}
      finally{if(send)send.disabled=false;}
    });
  }

  // Consent management. Optional analytics are OFF by default.
  const banner = $('#cookie-banner');
  const dialog = $('#consent-dialog');
  const STORAGE='skinlogic_consent_v1';
  function getConsent(){try{const val=localStorage.getItem(STORAGE);return val?JSON.parse(val):null;}catch(_){return null;}}
  function saveConsent(next){try{localStorage.setItem(STORAGE,JSON.stringify({analytics:!!next.analytics,marketing:!!next.marketing,savedAt:Date.now()}));}catch(_){} if(banner)banner.hidden=true; if(dialog?.open)dialog.close(); activateOptional(next);}
  const initial=getConsent();
  if(banner)banner.hidden=Boolean(initial);
  $$('.cookie-banner [data-consent]').forEach(btn=>btn.addEventListener('click',()=>saveConsent(btn.dataset.consent==='all'?{analytics:true,marketing:true}:{analytics:false,marketing:false})));
  $$('[data-open-consent]').forEach(btn=>btn.addEventListener('click',()=>{
    if(!dialog)return;
    const existing=getConsent()||{analytics:false,marketing:false};
    $('#consent-analytics').checked=Boolean(existing.analytics);
    $('#consent-marketing').checked=Boolean(existing.marketing);
    if(!dialog.open)dialog.showModal();
  }));
  $$('[data-close-consent]').forEach(btn=>btn.addEventListener('click',()=>dialog?.close()));
  dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  $('[data-save-consent]')?.addEventListener('click',()=>saveConsent({analytics:$('#consent-analytics').checked,marketing:$('#consent-marketing').checked}));
  let gaLoaded=false,pixelLoaded=false;
  function activateOptional(state){
    // In this initial delivery no measurement IDs are set or loaded.
    // If IDs are supplied later, revocation stops future optional events; for full
    // revocation handling, configure the provider's consent mode before go-live.
    if(state?.analytics && cfg.analyticsId && !gaLoaded){
      gaLoaded=true;
      const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(cfg.analyticsId);document.head.append(s);
      window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments)};
      window.gtag('js',new Date());window.gtag('config',cfg.analyticsId,{anonymize_ip:true});
    }
    if(state?.marketing && cfg.metaPixelId && !pixelLoaded){
      pixelLoaded=true;
      (function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)})(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      window.fbq('init',cfg.metaPixelId);window.fbq('track','PageView');
    }
  }
  if(initial)activateOptional(initial);
  const year=$('#year');if(year)year.textContent=String(new Date().getFullYear());
})();
