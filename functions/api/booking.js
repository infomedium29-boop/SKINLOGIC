// Cloudflare Pages Function: optional booking enquiry endpoint.
// Requires Resend verified sending domain and three environment variables:
// RESEND_API_KEY, BOOKING_RECEIVER_EMAIL, BOOKING_FROM_EMAIL.
// Not active in the initial demo. Never expose the Resend API key in client code.
const treatmentSlugs = new Set([
  'threading','lash-lift','brow-lift','kemijski-pilinzi','hydrafacial','dermapen',
  'mesoboost','ciscenje-lica','bukalna-masaza','trajna-sminka-usana',
  'trajna-sminka-obrva','kamuflaza-oziljaka-i-strija'
]);
const json = (data,status=200)=>new Response(JSON.stringify(data),{
  status,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}
});
const clean=(value,max)=>typeof value==='string'?value.replace(/[\x00-\x1F\x7F]/g,' ').trim().slice(0,max):'';
export async function onRequestPost({request,env}) {
  if (!env.RESEND_API_KEY || !env.BOOKING_RECEIVER_EMAIL || !env.BOOKING_FROM_EMAIL) return json({error:'not_configured'},503);
  if (!(request.headers.get('Content-Type')||'').toLowerCase().includes('application/json')) return json({error:'invalid_type'},415);
  const raw=await request.text();
  if(raw.length>8000)return json({error:'too_large'},413);
  let form;try{form=JSON.parse(raw);}catch{return json({error:'invalid_json'},400);}
  if(form.website)return json({error:'invalid_request'},400);
  const name=clean(form.name,100),phone=clean(form.phone,35),email=clean(form.email,180),date=clean(form.date,15),treatment=clean(form.treatment,100),note=clean(form.note,1200),language=clean(form.language,2);
  if(!name || !phone || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||!/^\d{4}-\d{2}-\d{2}$/.test(date)||!treatmentSlugs.has(treatment)||form.agreed!=='on')return json({error:'invalid_fields'},400);
  const earliest=new Date();earliest.setUTCHours(0,0,0,0);const desired=new Date(date+'T00:00:00Z');
  if(!Number.isFinite(desired.getTime())||desired.getTime()<earliest.getTime()-86400000)return json({error:'invalid_date'},400);
  const message=[`Skinlogic — novi upit za termin`,`Ime: ${name}`,`Telefon: ${phone}`,`E-mail: ${email}`,`Tretman: ${treatment}`,`Željeni datum: ${date}`,`Jezik: ${language==='en'?'EN':'HR'}`,`Napomena: ${note||'—'}`,`Termin nije automatski potvrđen.`].join('\n');
  try{
    const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${env.RESEND_API_KEY}`,'Content-Type':'application/json'},body:JSON.stringify({from:env.BOOKING_FROM_EMAIL,to:[env.BOOKING_RECEIVER_EMAIL],reply_to:email,subject:'Skinlogic — upit za termin',text:message})});
    if(!response.ok)return json({error:'delivery_failed'},502);
    return json({ok:true},200);
  } catch(_){return json({error:'delivery_failed'},502);}
}
