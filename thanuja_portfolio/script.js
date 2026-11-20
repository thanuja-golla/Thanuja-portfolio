'use strict';
const navToggle = document.querySelector('#navToggle');
const navLinks = document.querySelector('#navLinks');
navToggle.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
  navToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
});
navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  navLinks.classList.remove('open'); navToggle.setAttribute('aria-expanded','false');
}));
document.addEventListener('keydown', e => { if(e.key==='Escape') {navLinks.classList.remove('open');navToggle.setAttribute('aria-expanded','false');} });
const observer = new IntersectionObserver(entries => entries.forEach(entry => {
  if(entry.isIntersecting) {entry.target.classList.add('visible');observer.unobserve(entry.target);}
}),{threshold:.08});
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
const progress = document.querySelector('#progress');
function updateProgress(){const max=document.documentElement.scrollHeight-innerHeight;progress.style.width=`${max>0?window.scrollY/max*100:0}%`;}
addEventListener('scroll',updateProgress,{passive:true});updateProgress();
document.querySelector('#year').textContent=new Date().getFullYear();
const filterButtons=document.querySelectorAll('.filter-btn');
filterButtons.forEach(button=>button.addEventListener('click',()=>{
  const filter=button.dataset.filter;
  filterButtons.forEach(b=>{const active=b===button;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
  document.querySelectorAll('.project-card').forEach(card=>card.hidden=filter!=='all'&&card.dataset.category!==filter);
}));
const projectDetails={
  data:{category:'PROFESSIONAL · DATA VALIDATION',title:'Data Validation & Preprocessing',description:'Responsibilities described in the Innovapte internship include preparing and checking datasets so that teams can work with cleaner information.',highlights:['Preprocessed data to handle missing values, remove duplicates and correct errors.','Used Excel functions for cleaning, analysis and visualization.','Extracted data from résumés into spreadsheets.','Researched SAP-domain profiles, supported LinkedIn outreach and downloaded leads from Apollo.io.','Shared findings with senior team members or clients.']},
  balance:{category:'ACADEMIC PROJECT · FEB–MAY 2023',title:'Study on Work–Life Balance of Employees',description:'The résumé describes a mixed-methods research approach combining quantitative surveys with qualitative interviews to understand employee work–life balance.',highlights:['Survey design included demographics, work-related factors and perceived work–life balance.','Qualitative interviews were intended to explore employee experiences in greater depth.','This is presented as an academic research project, not a published research paper.']},
  human:{category:'ACADEMIC PROJECT',title:'Human Touch Alive',description:'A concept exploring the continuing importance of human involvement even as machinery and automation take on more work.',highlights:['Explores the value of human input alongside technology.','Emphasizes people-focused thinking in increasingly automated settings.','No separate project URL or deliverable was supplied in the résumé.']}
};
const dialog=document.querySelector('#projectDialog');
document.querySelectorAll('.project-detail').forEach(button=>button.addEventListener('click',()=>{
  const item=projectDetails[button.dataset.project];if(!item)return;
  document.querySelector('#dialogCategory').textContent=item.category;
  document.querySelector('#dialogTitle').textContent=item.title;
  document.querySelector('#dialogDescription').textContent=item.description;
  const ul=document.createElement('ul');item.highlights.forEach(t=>{const li=document.createElement('li');li.textContent=t;ul.append(li);});
  document.querySelector('#dialogHighlights').replaceChildren(ul);
  if(typeof dialog.showModal==='function')dialog.showModal();else dialog.setAttribute('open','');
}));
function closeDialog(){dialog.close?.();dialog.removeAttribute('open');}
document.querySelector('#dialogClose').addEventListener('click',closeDialog);
document.querySelector('#dialogDone').addEventListener('click',closeDialog);
dialog.addEventListener('click',e=>{if(e.target===dialog)closeDialog();});
const form=document.querySelector('#contactForm');const status=document.querySelector('#formStatus');const send=document.querySelector('#sendBtn');
form.addEventListener('submit',async e=>{
  e.preventDefault();status.className='form-status';status.textContent='';
  const name=form.elements.namedItem('name').value.trim();const email=form.elements.namedItem('email').value.trim();const message=form.elements.namedItem('message').value.trim();const website=form.elements.namedItem('website').value;
  if(name.length<2||name.length>100){status.textContent='Please enter your name (2–100 characters).';status.classList.add('error');return;}
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){status.textContent='Please enter a valid email address.';status.classList.add('error');return;}
  if(message.length<10||message.length>5000){status.textContent='Please enter a message between 10 and 5000 characters.';status.classList.add('error');return;}
  send.disabled=true;send.textContent='Sending…';
  try{
    const res=await fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,email,message,website})});
    const data=await res.json();if(!res.ok||!data.ok)throw Error(data.error||'Unable to submit your message.');
    status.textContent=data.message||'Your message was saved successfully.';status.classList.add('success');form.reset();
  }catch(err){status.textContent=err.message==='Failed to fetch'?'Could not connect to the website server. Please use the email link instead.':err.message;status.classList.add('error');}
  finally{send.disabled=false;send.innerHTML='Send message <span aria-hidden="true">↗</span>';}
});
