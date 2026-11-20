LX.INFO={
'Total cholesterol':['All the cholesterol in your blood: the LDL that can build up in arteries plus the HDL that clears it. On its own it says little.','Use it as a summary only. ApoB, LDL and non-HDL tell you more about heart risk.'],
'LDL':['“Bad” cholesterol: the cholesterol carried by particles that can lodge in artery walls.','Running does not lower LDL much. Diet (fiber, less saturated fat), genetics and sometimes medication do.'],
'HDL':['“Good” cholesterol: particles that carry cholesterol away from the arteries back to the liver.','Endurance training tends to raise it. Higher is generally better.'],
'Triglycerides':['Fat carried in the blood, mostly from recent meals, sugar and alcohol.','Rises with alcohol, sweets and late heavy meals. Usually falls with consistent training.'],
'Non-HDL':['Total cholesterol minus HDL: all the particles that can clog arteries in one number.','A good single summary of heart risk from cholesterol. Moves with LDL and triglycerides.'],
'ApoB':['A count of the particles that carry cholesterol into artery walls. Each one has one ApoB.','Considered the most direct cholesterol risk marker. It moves with diet, weight and medication, not with mileage.'],
'Lp(a)':['A sticky cholesterol particle set mostly by your genes.','It barely changes with diet or training, so one test is usually enough. A high value means keeping LDL and ApoB lower.'],
'Remnant cholesterol':['Cholesterol in the leftover particles after fat from food is processed.','Tracks with triglycerides. Falls with less alcohol and sugar.'],
'TSH':['The brain’s signal telling the thyroid to work harder. High TSH means the thyroid needs more push.','Hard training blocks, poor sleep and low energy intake can nudge it. Recheck when rested.'],
'T4':['The main hormone the thyroid makes (total amount).','Read it together with TSH and free T4.'],
'T3':['The active thyroid hormone that sets how fast the body burns energy.','Can dip with low calorie intake or very heavy training.'],
'Free T4':['The unbound, usable part of T4 that tissues can actually use.','Normal free T4 with a mildly high TSH is usually just something to watch.'],
'Free T3':['The unbound, active thyroid hormone.','Drops when energy intake does not match training. A useful under-fueling check.'],
'TPO antibody':['Antibodies against the thyroid. They show whether the immune system targets it.','Negative means an autoimmune thyroid problem is unlikely.'],
'PSA':['A protein made by the prostate, used to screen for prostate problems.','Long rides and hard efforts can raise it briefly. Avoid cycling and hard sessions 48 h before the test.'],
'Glucose':['Blood sugar at the moment of the draw.','Fasting values are what matter. A big carb dinner or a hard morning session can shift it.'],
'Fructosamine':['Average blood sugar over the last 2–3 weeks.','Less affected by one meal than glucose. Useful during high-carb training blocks.'],
'Uric acid':['A waste product from breaking down purines (red meat, seafood, alcohol, fructose).','Dehydration and hard efforts raise it. High levels can cause gout.'],
'Creatinine':['A waste product from muscle, cleared by the kidneys.','Runs naturally higher in muscular, active people and after hard training or a lot of protein.'],
'eGFR':['An estimate of how well the kidneys filter, calculated from creatinine.','Can look low in athletes because creatinine is high from muscle. Cystatin C gives a cleaner reading.'],
'BUN':['Urea nitrogen: a waste product from protein, cleared by the kidneys.','Rises with high protein intake and dehydration.'],
'Cystatin C':['A kidney filtration marker that does not depend on muscle mass.','The fairer kidney check for muscular athletes.'],
'Urine albumin/creatinine':['How much protein leaks into the urine.','Hard exercise can cause a temporary leak. Test on a rest day.'],
'Urine creatinine 24h':['Total creatinine passed in a full day of urine.','Mostly used to check that a 24-hour urine collection was complete.'],
'Calcium':['Calcium in the blood, kept in a tight range by hormones (PTH and vitamin D).','Repeated high values are worth a doctor’s look: ionized calcium, PTH, vitamin D intake and supplements.'],
'Albumin':['The main protein in blood. It also carries calcium.','Dehydration raises it, and with it total calcium. Hydrate well before the draw.'],
'PTH':['Parathyroid hormone, which raises blood calcium when it gets low.','Normal PTH with high calcium is a key clue for the doctor.'],
'Vitamin D':['Vitamin D stored in the body. It helps absorb calcium and supports bones and muscles.','Sun in Miami helps, but supplements can push it too high. Check before adding more.'],
'ALT':['A liver enzyme. It rises when liver cells are stressed.','Can rise for a few days after very hard or long sessions, from muscle as well as liver.'],
'AST':['An enzyme found in liver and muscle.','Often high after long runs and races because of muscle damage. Test after 2 easy days.'],
'ALP':['An enzyme from liver and bone.','Can be higher in people building bone or with liver bile issues.'],
'GGT':['A liver enzyme that rises with alcohol, liver fat and some medications.','One of the most alcohol-sensitive markers. Usually falls after a few dry weeks.'],
'Hemoglobin':['The oxygen-carrying protein in red blood cells.','Directly linked to endurance. Training can dilute it a little (more plasma).'],
'Hematocrit':['The share of blood made of red cells.','Low values can mean low iron. Dehydration makes it read higher.'],
'Platelets':['Cells that help blood clot.','Usually unaffected by training. Values far from range need a recheck.'],
'WBC':['White blood cells: the immune system’s soldiers.','Can dip in heavy training blocks and rise with infection or right after a hard session.'],
'Ferritin':['Stored iron, the body’s iron reserve.','Runners lose iron through foot strike, sweat and the gut. Low ferritin can mean fatigue before anemia shows.'],
'Testosterone (total)':['The main male hormone, important for muscle repair and energy.','Can fall with very high training load, low calorie intake and poor sleep.'],
'Cortisol':['The stress hormone, highest in the morning.','Early draws and hard training raise it. Compare at the same time of day.'],
'Estradiol':['The main estrogen. Men need some for bone and heart health.','Usually read together with testosterone and SHBG.'],
'SHBG':['A protein that binds sex hormones and decides how much is free to use.','Rises with high endurance volume and low energy intake.'],
'hs-CRP':['A sensitive marker of inflammation anywhere in the body.','Spikes for a day or two after hard sessions and when sick. Test after easy days.'],
};
LX.WHO=window.LX_WHO||null;
LX.ib=m=>{const b=LX.el('button','lx-ib');b.type='button';b.setAttribute('aria-label','About '+m);b.title='What is '+m+'?';b.textContent='i';b.onclick=e=>{e.stopPropagation();LX.info=m;dash.draw('info');};return b;};
LX.story=(m)=>{const d=dash.data('labs');const L=LX.latest();if(d.status!=='ok')return '';const rs=d.data.filter(r=>r.marker===m).sort((a,b)=>a.date<b.date?-1:1);if(!rs.length)return '';
  const who=LX.WHO?LX.WHO+'’s':'Your',f=rs[0],l=rs[rs.length-1],u=l.unit,lr=L&&L.find(x=>x.marker===m);const out=[];
  if(rs.length===1)out.push(`${who} only result is ${l.qualifier||''}${l.value} ${u} (${LX.fmt(LX.parse(l.date))}).`);
  else{const a=+f.value,b=+l.value,pct=a?Math.round((b-a)/a*100):0;const dir=Math.abs(pct)<5?'held steady':pct>0?'rose':'fell';
    out.push(`${who} ${rs.length} results since ${LX.fmt(LX.parse(f.date))}: from ${f.qualifier||''}${f.value} to ${l.qualifier||''}${l.value} ${u}. It ${dir}${Math.abs(pct)>=5?' '+Math.abs(pct)+'%':''}.`);}
  const hi=rs.filter(r=>r.flag==='H').length,lo=rs.filter(r=>r.flag==='L').length;
  if(hi)out.push(`The lab flagged it high ${hi===rs.length?'every time':hi===1?'once':hi+' times'}.`);if(lo)out.push(`The lab flagged it low ${lo===1?'once':lo+' times'}.`);
  if(lr){if(lr.status==='High')out.push('The latest result is above the lab range — worth raising with the doctor.');
    else if(lr.status==='Watch')out.push(`The latest result is inside the lab range but ${lr.target_max!=null?'above':'below'} the athlete target (${lr.target_max!=null?'<'+lr.target_max:'>'+lr.target_min} ${u}).`);
    else if(!hi)out.push('The latest result is in range.');
    else out.push('The latest result is back in range.');}
  return out.join(' ');};
dash.draw('info',(el)=>{el.replaceChildren();const m=LX.info;if(!m)return;const L=LX.latest();const r=L&&L.find(x=>x.marker===m);const I=LX.INFO[m]||['A lab marker from the panel.','Ask your doctor what it means for you.'];
  const close=()=>{LX.info=null;dash.draw('info');};
  const ov=LX.el('div','lx-ov');ov.onclick=e=>{if(e.target===ov)close();};const card=LX.el('div','lx-sheet');card.setAttribute('role','dialog');card.setAttribute('aria-modal','true');card.setAttribute('aria-label','About '+m);
  const top=LX.el('div','row');const t=LX.el('div');t.append(LX.el('span','lx-eye',r?r.category||'Marker':'Marker'),LX.el('h3',null,m));const x=LX.el('button','lx-x','✕');x.type='button';x.setAttribute('aria-label','Close');x.onclick=close;top.append(t,x);card.append(top);
  if(r){const [cls,col]=LX.ST[r.status];const v=LX.el('div','row');const vv=LX.el('div');vv.append(LX.mark(LX.el('span','lx-val',r.qualifier+r.value),'latest','value','marker='+encodeURIComponent(m)),LX.el('span','lx-unit',r.unit));v.append(vv,LX.el('span','lx-pill '+cls,r.status));card.append(v);
    const sp=LX.el('div');card.append(sp);const hist=dash.data('labs').data.filter(z=>z.marker===m).map(z=>({dt:LX.parse(z.date),v:+z.value,flag:z.flag})).sort((a,b)=>a.dt-b.dt);if(hist.length>1)requestAnimationFrame(()=>LX.spark(sp,hist,Math.max(240,sp.clientWidth||300),col));}
  [['What it is',I[0],'flask'],['For a runner',I[1],'heart'],[LX.WHO?LX.WHO+'’s history':'Your history',LX.story(m),'chart']].forEach(([h,p,ic])=>{if(!p)return;const s=LX.el('div','lx-isec');const hh=LX.el('div','lx-ih');hh.append(LX.svg(ic,15,dash.colors[1]),LX.el('span',null,h));s.append(hh,LX.el('p',null,p));card.append(s);});
  card.append(LX.el('p','lx-muted','Educational only — review your results with your doctor.'));
  ov.append(card);el.append(ov);x.focus();
  const esc=e=>{if(e.key==='Escape'){document.removeEventListener('keydown',esc);close();}};document.addEventListener('keydown',esc);});
