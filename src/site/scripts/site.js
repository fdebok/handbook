
(function(){
  var main=document.querySelector('main');
  var hs=[].slice.call(main.querySelectorAll('article h3, .part-band h2'));
  var list=document.getElementById('toclist');
  var map=[];
  hs.forEach(function(h){
    var host=h.closest('article, .part-band');
    if(!host||!host.id) return;
    if(h.tagName==='H2'){
      var d=document.createElement('div');
      d.className='toc-part'; d.textContent=h.textContent.trim(); d.dataset.id=host.id;
      list.appendChild(d); map.push({id:host.id,el:d,lv:2});
    }else{
      var t=h.childNodes; var name='';
      for(var i=0;i<t.length;i++){ if(t[i].nodeType===3) name+=t[i].textContent; }
      var a=document.createElement('a');
      a.href='#'+host.id; a.textContent=(name.trim()||h.textContent.trim());
      list.appendChild(a); map.push({id:host.id,el:a,lv:3});
    }
  });
  var links=map.filter(function(m){return m.lv===3;});
  var arts=[].slice.call(main.querySelectorAll('article[id]'));
  function onScroll(){
    var y=window.scrollY+120, cur=null;
    arts.forEach(function(a){ if(a.offsetTop<=y) cur=a.id; });
    links.forEach(function(m){
      var active=m.id===cur;
      m.el.classList.toggle('on',active);
      if(active)m.el.setAttribute('aria-current','location');
      else m.el.removeAttribute('aria-current');
    });
    var dh=document.documentElement.scrollHeight-window.innerHeight;
    document.getElementById('bar').style.width=(dh>0?(window.scrollY/dh*100):0)+'%';
    document.getElementById('top').classList.toggle('show', window.scrollY>700);
  }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  var topButton=document.getElementById('top');
  topButton.onclick=function(){window.scrollTo({top:0,behavior:'smooth'})};
  var q=document.getElementById('tq');
  var empty=document.getElementById('toc-empty');
  q.addEventListener('input',function(){
    var v=q.value.trim().toLowerCase();
    var shown=0;
    [].slice.call(list.children).forEach(function(n){
      var match=!v||n.textContent.toLowerCase().indexOf(v)>-1;
      n.style.display=match?'':'none';
      if(match)shown++;
    });
    empty.style.display=v&&shown===0?'block':'none';
  });
  document.querySelectorAll('.tw').forEach(function(w){
    w.setAttribute('role','group');
    w.setAttribute('tabindex','0');
    if(!w.hasAttribute('aria-label'))w.setAttribute('aria-label','可横向滚动的数据表格');
  });
  var tocPanel=document.getElementById('toc-panel');
  if(window.matchMedia){
    var compact=window.matchMedia('(max-width:980px)');
    function syncToc(event){tocPanel.open=!event.matches}
    syncToc(compact);
    if(compact.addEventListener)compact.addEventListener('change',syncToc);
    else if(compact.addListener)compact.addListener(syncToc);
  }
})();


(function(){
 var translationDataNode=document.getElementById('translation-data');
 if(!translationDataNode)throw new Error('Missing translation data');
 var translationData=JSON.parse(translationDataNode.textContent);
 var ENG=translationData.eng;
 var ATTR=translationData.attr;
var selfCheckGuidance=[
   {titleZh:'业务结果与验收',titleEn:'Business outcomes and acceptance',href:'#d1',
    lowZh:'与业务 Owner 明确一个可测的业务结果，记录上线前基线、数据来源、测量周期和验收人。',
    lowEn:'Agree on a measurable business outcome with its owner; record the pre-launch baseline, data source, measurement period, and acceptance owner.',
    nextZh:'在不同业务周期复核指标，检验收益归因，并把结果纳入项目复盘和后续方案。',
    nextEn:'Recheck the metric across business cycles, validate attribution, and carry the findings into retrospectives and future plans.'},
   {titleZh:'现场诊断与约束',titleEn:'Field diagnosis and constraints',href:'#d2',
    lowZh:'补齐可复核的现场诊断：流程、代表性样本、数据与权限、接口验证、部署限制和未证实假设。',
    lowEn:'Complete a verifiable field diagnosis: workflow, representative samples, data and permissions, interface checks, deployment constraints, and untested assumptions.',
    nextZh:'将诊断清单与验证脚本版本化，并在不同环境验证可复用性。',
    nextEn:'Version the diagnostic checklist and verification scripts, then test them in another environment.'},
   {titleZh:'评测与回归',titleEn:'Evaluation and regression',href:'#d7',critical:true,
    lowZh:'先与业务方约定失败类型和发布门槛，建立分层、版本化的评测集，并让关键变更触发回归。',
    lowEn:'Agree on failure categories and release criteria with business owners; build a stratified, versioned evaluation set and run regressions for material changes.',
    nextZh:'用线上坏例校准评测集与人工判分，将门禁、发布和回滚流程连起来。',
    nextEn:'Calibrate the evaluation set and human judgments with production failures; connect quality gates to release and rollback procedures.'},
   {titleZh:'失败归因与修复',titleEn:'Failure attribution and remediation',href:'#d7',
    lowZh:'为真实失败样例标注检索、推理、数据或评测归因，记录证据、修复责任人及复测结果。',
    lowEn:'Classify real failures as retrieval, reasoning, data, or evaluation issues; record evidence, an owner, and retest results.',
    nextZh:'分析不同故障类别的重复率与修复周期，优先消除系统性根因。',
    nextEn:'Track recurrence and time to resolution by failure class, prioritizing systemic root causes.'},
   {titleZh:'用户验证与人工兜底',titleEn:'User validation and human fallback',href:'#d8',
    lowZh:'观察代表性用户完成真实任务，明确异常升级、拒答、人工接管和恢复路径。',
    lowEn:'Observe representative users completing real tasks; define exception escalation, abstention, human handoff, and recovery paths.',
    nextZh:'持续抽样用户结果与反馈，确认兜底流程可运行并由明确角色负责。',
    nextEn:'Sample user outcomes and feedback continuously; exercise fallback procedures and assign clear owners.'},
   {titleZh:'跨项目复用',titleEn:'Reuse across projects',href:'#c19',
    lowZh:'从一个真实项目开始沉淀可配置的脚本、连接器、评测样本或模板，并指定维护人。',
    lowEn:'Start with one real project: package a configurable script, connector, evaluation case, or template and assign an owner.',
    nextZh:'记录复用次数、适配成本与失效边界，避免把客户特例误当通用组件。',
    nextEn:'Track reuse, adaptation cost, and limitations; do not mistake a customer-specific exception for a reusable component.'},
   {titleZh:'写操作与权限',titleEn:'Write operations and permissions',href:'#d4',critical:true,
    lowZh:'逐项盘点写操作与数据边界，落实最小权限、人工审批、审计记录、停用开关和已验证的回滚方案。',
    lowEn:'Inventory write operations and data boundaries; implement least privilege, human approval, audit records, a suspension control, and a tested rollback.',
    nextZh:'通过角色测试与故障演练验证授权、审计和回滚；任何高风险写操作未闭环前都应保持人工审批。',
    nextEn:'Verify access, audit, and rollback through role-based tests and failure exercises; keep human approval for high-risk writes until controls are proven.'},
   {titleZh:'全链路成本',titleEn:'End-to-end cost',href:'#d1',
    lowZh:'按一次业务动作核算模型、平台、人工复核、维护和异常处置成本，并注明数据来源与遗漏项。',
    lowEn:'Calculate model, platform, human-review, maintenance, and exception-handling costs per business action; document sources and exclusions.',
    nextZh:'对照业务收益与质量变化复核单位成本，明确成本上升时的责任人与处置阈值。',
    nextEn:'Compare unit cost with business value and quality; define owners and action thresholds for cost increases.'},
   {titleZh:'需求判断与沟通',titleEn:'Scope judgment and communication',href:'#c1',
    lowZh:'用书面记录呈现目标、风险、替代方案、范围取舍和客户确认，避免口头承诺掩盖分歧。',
    lowEn:'Document goals, risks, alternatives, scope trade-offs, and customer agreement so verbal commitments do not hide unresolved issues.',
    nextZh:'复盘一次范围谈判或方案调整，验证决策依据、沟通时点及结果是否符合约定。',
    nextEn:'Review a scope negotiation or plan change; check the evidence, timing, and outcome against the agreement.'},
   {titleZh:'交接与知识沉淀',titleEn:'Handover and reusable knowledge',href:'#c21',
    lowZh:'补齐可执行的运行手册、检查项、已知限制、故障升级与回滚步骤，并安排接手人实操验证。',
    lowEn:'Create an actionable runbook covering checks, known limitations, escalation, and rollback; have the next owner test it hands-on.',
    nextZh:'让未参与原交付的同事独立完成部署、排障或回滚，并据此迭代文档。',
    nextEn:'Ask a colleague outside the original delivery to deploy, troubleshoot, or roll back independently, then improve the documentation.'}
 ];
 var domainChecklistGuidance=[
   {id:'d1',titleZh:'D1 场景与价值',titleEn:'D1 · Discovery and value',href:'#d1',critical:[],
    actionZh:'先让业务 Owner 确认问题、指标口径和验收人；补齐上线前基线、目标区间、数据来源与排除项，避免把模型指标误当成业务收益。',
    actionEn:'Have the business owner confirm the problem, metric definition, and acceptance owner. Record the baseline, target range, data source, and exclusions; do not treat model metrics as business value.'},
   {id:'d2',titleZh:'D2 现场诊断',titleEn:'D2 · Field discovery',href:'#d2',critical:[],
    actionZh:'补齐底座、系统、治理与人员四类现场证据。亲自验证关键接口、权限路径和部署约束；未知项要有责任人及关闭日期。',
    actionEn:'Gather evidence across infrastructure, systems, governance, and people. Test critical interfaces, access paths, and deployment constraints; assign an owner and due date to every unknown.'},
   {id:'d3',titleZh:'D3 数据与知识',titleEn:'D3 · Data and knowledge',href:'#d3',critical:[1,4],
    actionZh:'先锁定权威来源与冲突裁决机制，再验证来源、版本、时效、密级和责任人。对关键数据和已废止内容，必须能证明其隔离、更新或下线流程有效。',
    actionEn:'Confirm authoritative sources and conflict resolution first, then verify provenance, version, freshness, sensitivity, and ownership. Prove that controls for critical and retired data work.'},
   {id:'d4',titleZh:'D4 权限与安全',titleEn:'D4 · Access and security',href:'#d4',critical:[1,2,3,4,5,6],
    actionZh:'把建议、审批与执行分开，用最小权限、硬性限额、审计和到期回收约束写操作。缺少攻击测试、可追溯记录或已演练回滚时，不开放高影响操作。',
    actionEn:'Separate recommendation, approval, and execution. Constrain writes with least privilege, hard limits, audit, and expiring access. Do not enable high-impact actions without adversarial tests, traceable records, and a rehearsed rollback.'},
   {id:'d5-d6',titleZh:'D5–D6 方案与实现',titleEn:'D5–D6 · Solution and implementation',href:'#d5',critical:[],
    actionZh:'把方案取舍和高风险假设写下来，并在接近生产的环境逐条验证失败路径、调用轨迹、容量与成本；演示环境“能跑”不是交付证据。',
    actionEn:'Document trade-offs and risky assumptions. Verify failure paths, traces, capacity, and cost in a production-representative environment; a working demo is not delivery evidence.'},
   {id:'d7',titleZh:'D7 评测',titleEn:'D7 · Evaluation',href:'#d7',critical:[1,2,3,4,5],
    actionZh:'用真实业务样本建立版本化评测集，纳入困难与对抗案例；校准人工与模型评分的一致性，并让重要变更触发回归和明确的发布门槛。',
    actionEn:'Build a versioned evaluation set from real business cases, including difficult and adversarial examples. Calibrate model grading against human judgments and gate material changes on regression results.'},
   {id:'d8-d9',titleZh:'D8–D9 上线与运行',titleEn:'D8–D9 · Launch and operations',href:'#d8',critical:[1,2,3,4,5],
    actionZh:'上线前演练就绪检查、风险分层灰度、降级、监控和回滚，并由接手人独立验证。任一关键运行控制未验证时，保持人工兜底，不扩大影响面。',
    actionEn:'Rehearse readiness, risk-based rollout, degradation, monitoring, and rollback before launch; have the receiving owner verify them independently. Keep human fallback and limit exposure while a critical control remains unverified.'},
   {id:'d10',titleZh:'D10 沉淀',titleEn:'D10 · Reuse and institutionalization',href:'#d10',critical:[],
    actionZh:'为可复用组件指定维护人、依赖和适用边界，并在另一项目验证；把现场需求纳入可追踪的产品回流，用决策证据复盘而非只写过程。',
    actionEn:'Assign maintainers, dependencies, and boundaries to reusable components, then validate them in another project. Track product feedback and review decisions with evidence, not just process.'}
 ];
 var domainChecklistItems=[];
 var checklistStorageError=false;
 var domainChecklistStorageKey='fdebok-domain-checklist-v1';
 var domainChecklistOptInKey='fdebok-domain-checklist-local-opt-in';
 function checklistSaveStatus(){
   var saveToggle=document.getElementById('domain-check-save');
   var status=document.getElementById('domain-check-save-state');
   if(!saveToggle||!status)return;
   var isEnglish=document.documentElement.lang==='en';
   status.textContent=checklistStorageError
     ?(isEnglish?'Local saving is unavailable in this browser; this page remains usable, but progress will not persist.':'此浏览器当前无法保存到本机；清单仍可使用，但刷新后进度不会保留。')
     :(saveToggle.checked
       ?(isEnglish?'Enabled: selections are stored only in this browser on this device.':'已启用：勾选状态仅保存在此设备的当前浏览器中。')
       :(isEnglish?'Not saved by default; selections clear when you reload.':'默认不保存；刷新页面后勾选状态会清空。'));
 }
 function saveDomainChecklist(){
   var saveToggle=document.getElementById('domain-check-save');
   if(!saveToggle||!saveToggle.checked)return;
   try{
     var checked=domainChecklistItems.filter(function(item){return item.input.checked;}).map(function(item){return item.input.id;});
     localStorage.setItem(domainChecklistStorageKey,JSON.stringify({checked:checked}));
     checklistStorageError=false;
   }catch(error){
     checklistStorageError=true;
     saveToggle.checked=false;
   }
   checklistSaveStatus();
 }
 function renderDomainChecklist(){
   if(!domainChecklistItems.length)return;
   var isEnglish=document.documentElement.lang==='en';
   var verified=domainChecklistItems.filter(function(item){return item.input.checked;}).length;
   var pending=domainChecklistItems.length-verified;
   var criticalPending=domainChecklistItems.filter(function(item){return item.critical&&!item.input.checked;}).length;
   var verifiedOutput=document.getElementById('domain-check-verified');
   var pendingOutput=document.getElementById('domain-check-pending');
   var criticalOutput=document.getElementById('domain-check-critical');
   var progress=document.getElementById('domain-check-progress');
   var percent=document.getElementById('domain-check-percent');
   var status=document.getElementById('domain-check-status');
   var recommendations=document.getElementById('checklist-recommendations-list');
   var nextSteps=document.getElementById('checklist-next-steps');
   var total=domainChecklistItems.length;
   if(verifiedOutput)verifiedOutput.textContent=verified+' / '+total;
   if(pendingOutput)pendingOutput.textContent=String(pending);
   if(criticalOutput)criticalOutput.textContent=String(criticalPending);
   if(progress){progress.max=total;progress.value=verified;progress.setAttribute('aria-label',isEnglish?'Verified evidence coverage':'已有证据覆盖率');}
   if(percent)percent.textContent=Math.round(verified/total*100)+'%';
   domainChecklistGuidance.forEach(function(domain){
     var section=document.querySelector('#domain-check-form [data-check-domain="'+domain.id+'"]');
     if(!section)return;
     var items=domainChecklistItems.filter(function(item){return item.domain.id===domain.id;});
     var done=items.filter(function(item){return item.input.checked;}).length;
     var counter=section.querySelector('[data-domain-count]');
     if(counter)counter.textContent=done+' / '+items.length;
   });
   if(status)status.textContent=criticalPending
     ?(isEnglish
       ?criticalPending+' critical gate(s) still lack verified evidence. Keep high-impact writes and rollout expansion paused until these controls are checked and reviewed. Unchecked is not a failure finding, but it is not a pass.'
       :'仍有 '+criticalPending+' 项关键门槛缺少已核验证据。完成并复核前，先暂停高影响写操作和扩大灰度。未勾选不代表已判定失败，但不能视为通过。')
     :pending
       ?(isEnglish
         ?'Critical gates are marked verified; '+pending+' other item(s) remain open. Assign owners and due dates. Coverage alone is not a go-live decision.'
         :'关键门槛均已标记为有证据，但仍有 '+pending+' 项待核验。请明确责任人与期限；覆盖率不能代替上线决策。')
       :(isEnglish
         ?'All '+total+' items are marked as supported by evidence. This records your review; it does not independently validate artifacts or replace sign-off by business, security, and platform owners.'
         :'全部 '+total+' 项均已标记为有证据。这记录的是团队自查结果，并不代表工具已独立验证材料，也不替代业务、安全和平台责任人的正式评审。');
   if(recommendations)recommendations.textContent='';
   var domains=domainChecklistGuidance.map(function(domain,index){
     var items=domainChecklistItems.filter(function(item){return item.domain.id===domain.id;});
     return{domain:domain,index:index,pending:items.filter(function(item){return !item.input.checked;}).length,
       criticalPending:items.filter(function(item){return item.critical&&!item.input.checked;}).length,total:items.length};
   }).filter(function(result){return result.pending>0;}).sort(function(a,b){
     return b.criticalPending-a.criticalPending||b.pending-a.pending||a.index-b.index;
   }).slice(0,3);
   if(nextSteps)nextSteps.textContent=domains.length
     ?(isEnglish?'Prioritized by unresolved critical gates first, then by the number of unchecked items.':'先按未核验的关键门槛排序，再按各域待核验项数量列出优先行动。')
     :(isEnglish?'Before sign-off, spot-check the evidence with the accountable owners and confirm that project-specific regulatory and contractual controls are covered.':'签署前，请与责任人抽查原始证据，并确认项目特定的法规、合同与组织控制要求已纳入。');
   if(recommendations)domains.forEach(function(result){
     var domain=result.domain,li=document.createElement('li'),heading=document.createElement('strong');
     heading.textContent=(isEnglish?domain.titleEn:domain.titleZh)+' · '+result.pending+'/'+result.total+
       (isEnglish?' item(s) to verify':' 项待核验')+
       (result.criticalPending?(isEnglish?' · '+result.criticalPending+' critical':' · '+result.criticalPending+' 项关键门槛'):'');
     var advice=document.createElement('p');
     advice.textContent=isEnglish?domain.actionEn:domain.actionZh;
     var link=document.createElement('a');
     link.href=domain.href;
     link.textContent=isEnglish?'Review the related domain →':'查看对应知识域 →';
     li.appendChild(heading);li.appendChild(advice);li.appendChild(link);
     recommendations.appendChild(li);
   });
   checklistSaveStatus();
 }
 function initializeDomainChecklist(){
   var form=document.getElementById('domain-check-form');
   if(!form)return;
   domainChecklistItems=[];
   domainChecklistGuidance.forEach(function(domain){
     var section=form.querySelector('[data-check-domain="'+domain.id+'"]');
     var list=section&&section.querySelector('.ck');
     if(!list)return;
     list.classList.add('interactive');
     [].slice.call(list.querySelectorAll('li')).forEach(function(item,index){
       var checkbox=document.createElement('input');
       checkbox.type='checkbox';
       checkbox.id='domain-check-'+domain.id+'-'+(index+1);
       checkbox.setAttribute('aria-describedby','domain-check-instructions');
       var label=document.createElement('label');
       label.className='check-label';
       label.htmlFor=checkbox.id;
       var text=document.createElement('span');
       text.className='check-text';
       text.textContent=item.textContent.trim();
       label.appendChild(checkbox);
       label.appendChild(text);
       var critical=domain.critical.indexOf(index+1)!==-1;
       if(critical){
         checkbox.dataset.critical='true';
         var badge=document.createElement('span');
         badge.className='check-critical';
         badge.textContent='关键门槛';
         label.appendChild(badge);
       }
       item.textContent='';
       item.appendChild(label);
       domainChecklistItems.push({input:checkbox,domain:domain,critical:critical});
     });
   });
   var saveToggle=document.getElementById('domain-check-save');
   try{
     if(saveToggle&&localStorage.getItem(domainChecklistOptInKey)==='true'){
       saveToggle.checked=true;
       var saved=JSON.parse(localStorage.getItem(domainChecklistStorageKey)||'{}');
       var checkedIds=new Set(Array.isArray(saved.checked)?saved.checked:[]);
       domainChecklistItems.forEach(function(item){item.input.checked=checkedIds.has(item.input.id);});
     }
   }catch(error){
     checklistStorageError=true;
     if(saveToggle)saveToggle.checked=false;
   }
   form.addEventListener('change',function(event){
     if(event.target&&event.target.matches('input[type="checkbox"][id^="domain-check-"]')){
       var label=event.target.closest('label');
       if(label)label.classList.toggle('is-checked',event.target.checked);
       renderDomainChecklist();
       saveDomainChecklist();
     }
   });
   form.addEventListener('reset',function(){setTimeout(function(){
     domainChecklistItems.forEach(function(item){
       var label=item.input.closest('label');
       if(label)label.classList.toggle('is-checked',item.input.checked);
     });
     renderDomainChecklist();
     saveDomainChecklist();
   },0);});
   if(saveToggle)saveToggle.addEventListener('change',function(){
     try{
       if(saveToggle.checked){
         localStorage.setItem(domainChecklistOptInKey,'true');
         checklistStorageError=false;
         saveDomainChecklist();
       }else{
         localStorage.removeItem(domainChecklistOptInKey);
         localStorage.removeItem(domainChecklistStorageKey);
         checklistStorageError=false;
       }
     }catch(error){
       checklistStorageError=true;
       saveToggle.checked=false;
     }
     checklistSaveStatus();
   });
   domainChecklistItems.forEach(function(item){
     var label=item.input.closest('label');
     if(label)label.classList.toggle('is-checked',item.input.checked);
   });
   renderDomainChecklist();
 }
 function renderSelfAssessment(){
   var form=document.getElementById('self-check-form');
   if(!form)return;
   var isEnglish=document.documentElement.lang==='en';
   var selects=[].slice.call(form.querySelectorAll('select[data-self-check]'));
   var responses=selects.map(function(select,index){return {index:index,value:select.value};}).filter(function(item){return item.value!=='';});
   var scored=responses.filter(function(item){return /^\d$/.test(item.value);}).map(function(item){item.value=Number(item.value);return item;});
   var notApplicable=responses.length-scored.length;
   var count=document.getElementById('self-check-count');
   var progress=document.getElementById('self-check-progress');
   var scoreOutput=document.getElementById('self-check-score');
   var status=document.getElementById('self-check-status');
   var recommendationIntro=document.getElementById('self-check-recommendation-intro');
   var recommendationList=document.getElementById('self-check-recommendations-list');
   if(count)count.textContent=responses.length+' / '+selects.length;
   if(progress)progress.value=responses.length;
   if(recommendationList)recommendationList.textContent='';
   var score=null;
   if(scored.length>=8){
     var total=scored.reduce(function(sum,item){return sum+item.value;},0);
     score=Math.round(total/(scored.length*3)*100);
     var criticalLow=scored.filter(function(item){return (item.index===2||item.index===6)&&item.value<2;});
     var band=criticalLow.length
       ?(isEnglish?'Critical controls need attention':'关键控制待补齐')
       :(isEnglish
         ?(score<40?'Evidence base to build':score<65?'Independent delivery skills developing':score<85?'Stable delivery with emerging reuse':'Cross-context reuse and mentoring')
         :(score<40?'证据基础待建立':score<65?'独立交付能力在形成':score<85?'稳定交付并开始复用':'跨场景复用与带教能力'));
     if(scoreOutput)scoreOutput.textContent=score+' / 100';
     var summary=isEnglish
       ?'Reference band: '+band+'. Based on '+scored.length+' rated items; '+notApplicable+' marked not applicable. This is a self-reported reflection aid, not a standardized norm.'
       :'参考方向：'+band+'。按 '+scored.length+' 项评分计算，'+notApplicable+' 项标记不适用；这是自评复盘参考，不是标准常模或认证结论。';
     if(criticalLow.length)summary+=isEnglish
       ?' A critical evaluation or write-control item is below 2; address it before relying on the overall index.'
       :' 评测或写操作关键项存在低分，请优先处理，不要用总分抵消该缺口。';
     if(status)status.textContent=summary;
   }else{
     if(scoreOutput)scoreOutput.textContent='—';
     if(status)status.textContent=isEnglish
       ?'Answered '+responses.length+'/'+selects.length+' items; '+scored.length+' rated and '+notApplicable+' marked not applicable. Rate at least eight applicable items to see a reference index.'
       :'已选择 '+responses.length+'/'+selects.length+' 项：评分 '+scored.length+' 项、不适用 '+notApplicable+' 项。至少完成 8 项适用评分后才显示参考指数。';
   }
   if(!recommendationList||!recommendationIntro)return;
   if(!scored.length){
     recommendationIntro.textContent=isEnglish
       ?'No actions yet. Choose a rating to see up to three prioritized next steps.'
       :'暂无建议。选择评分后，会按关键控制和薄弱项排序给出最多三条可执行建议。';
     return;
   }
   recommendationIntro.textContent=isEnglish
     ?'Prioritized by critical controls first, then lower scores. Higher-scoring items suggest how to make individual practice repeatable.'
     :'关键控制优先，其余按分数由低到高排列；较高分项提示如何把单次实践升级为稳定机制。';
   scored.map(function(item){item.guidance=selfCheckGuidance[item.index];return item;}).sort(function(a,b){
     var aCritical=a.guidance.critical&&a.value<2,bCritical=b.guidance.critical&&b.value<2;
     if(aCritical!==bCritical)return aCritical?-1:1;
     return a.value-b.value||a.index-b.index;
   }).slice(0,3).forEach(function(item){
     var guidance=item.guidance,isLow=item.value<2;
     var li=document.createElement('li');
     var heading=document.createElement('strong');
     heading.textContent=(isEnglish?'Question '+(item.index+1)+' · '+guidance.titleEn:'第 '+(item.index+1)+' 项 · '+guidance.titleZh)+' · '+item.value+'/3';
     if(guidance.critical&&isLow)heading.textContent+=(isEnglish?' · Critical':' · 关键控制');
     var advice=document.createElement('p');
     advice.textContent=isEnglish?(isLow?guidance.lowEn:guidance.nextEn):(isLow?guidance.lowZh:guidance.nextZh);
     var link=document.createElement('a');
     link.href=guidance.href;
     link.textContent=isEnglish?'Read the related chapter →':'查看对应章节 →';
     li.appendChild(heading);li.appendChild(advice);li.appendChild(link);
     recommendationList.appendChild(li);
   });
 }
 var readingProgressKey='fdebok-reading-progress-v1';
 var readingBookmarkKey='fdebok-reading-bookmark-v1';
 var readingStatusState='ready';
 var readingStorageUnavailable=false;
 var savedReadingBookmark=null;
 var readingSaveTimer=null;
 var readingBookmarkHighlightTimer=null;
 var activeReadingBookmarkTarget=null;
 function setReadingStatus(state){
   readingStatusState=state;
   var status=document.getElementById('reading-panel-status');
   if(!status)return;
   status.dataset.state=state;
   var isEnglish=document.documentElement.lang==='en';
   var messages={
     ready:['阅读位置会在本机自动保存；下次打开时继续。','Your reading position is saved locally and restored next time.'],
     restored:['已从上次阅读位置继续。','Resumed from your last reading position.'],
     progressSaved:['阅读进度已保存在此设备。','Reading progress saved on this device.'],
     bookmarkSaved:['当前位置已保存为书签。','This position has been bookmarked.'],
     bookmarkOpened:['已跳转到保存的书签位置。','Moved to your saved bookmark.'],
     bookmarkCleared:['已移除书签；自动阅读进度仍会保留。','Bookmark removed; automatic reading progress is unchanged.'],
     storageError:['读取本机阅读数据失败或浏览器存储当前不可用；页面仍可正常阅读，但阅读位置和书签无法跨会话保存。','Reading data could not be read or local browser storage is unavailable. You can keep reading, but positions and bookmarks cannot persist between visits.']
   };
   status.textContent=messages[state][isEnglish?1:0];
 }
 function updateReadingControls(){
   var toggle=document.getElementById('reading-tools-toggle');
   var openBookmark=document.getElementById('reading-bookmark-open');
   var clearBookmark=document.getElementById('reading-bookmark-clear');
   var isEnglish=document.documentElement.lang==='en';
   if(openBookmark)openBookmark.hidden=!savedReadingBookmark;
   if(clearBookmark)clearBookmark.hidden=!savedReadingBookmark;
   if(toggle){
     toggle.classList.toggle('has-bookmark',!!savedReadingBookmark);
     toggle.setAttribute('aria-label',isEnglish
       ?(savedReadingBookmark?'Reading progress and bookmarks; a bookmark is saved':'Reading progress and bookmarks')
       :(savedReadingBookmark?'阅读进度与书签，已有书签':'阅读进度与书签'));
     toggle.title=isEnglish?'Reading progress and bookmarks':'阅读进度与书签';
   }
 }
 function updateVisitCounterLabel(){
   var counter=document.getElementById('page-visit-counter');
   var count=document.getElementById('page-visit-count');
   if(!counter||!count)return;
   var isEnglish=document.documentElement.lang==='en';
   var status=counter.dataset.status||'loading';
   var label=counter.querySelector('span:first-child');
   var suffix=counter.querySelector('span:last-child');
   if(status==='preview'){
     count.textContent=isEnglish?'Stats unavailable in this preview':'本地预览暂不可统计';
     if(label)label.hidden=true;
     if(suffix)suffix.hidden=true;
     counter.setAttribute('aria-label',count.textContent);
     return;
   }
   if(status==='error'){
     count.textContent=isEnglish?'Visit statistics temporarily unavailable':'访问统计暂不可用';
     if(label)label.hidden=true;
     if(suffix)suffix.hidden=true;
     counter.setAttribute('aria-label',count.textContent);
     return;
   }
   if(label){
     label.hidden=false;
     label.textContent=isEnglish?'Site visits:':'全站访问：';
   }
   if(suffix){
     suffix.hidden=false;
     suffix.textContent=isEnglish?'':'次';
   }
   counter.setAttribute('aria-label',status==='loaded'
     ?(isEnglish?'Site visits: '+count.textContent:'全站访问：'+count.textContent+' 次')
     :(isEnglish?'Site visit count is loading':'全站访问量加载中'));
 }
 function loadPageVisitCount(){
   var counter=document.getElementById('page-visit-counter');
   var count=document.getElementById('page-visit-count');
   if(!counter||!count||counter.dataset.requestStarted==='true')return;
   counter.dataset.requestStarted='true';
   if(window.location.origin!=='https://www.fdebok.com'){
     counter.dataset.status='preview';
     updateVisitCounterLabel();
     return;
   }
   counter.dataset.status='loading';
   updateVisitCounterLabel();
   var controller=typeof AbortController==='function'?new AbortController():null;
   var timeoutId=controller?window.setTimeout(function(){controller.abort();},3000):null;
   var requestOptions=controller?{signal:controller.signal}:{};
   fetch('/api/visits?path=global',requestOptions)
     .then(function(response){
       if(!response.ok)throw new Error('Visit counter request failed: HTTP '+response.status);
       return response.json();
     })
     .then(function(data){
       if(!data||data.path!=='global'||!Number.isSafeInteger(data.views)||data.views<0){
         throw new Error('Visit counter returned an invalid response');
       }
       count.textContent=String(data.views);
       counter.dataset.status='loaded';
       updateVisitCounterLabel();
     })
     .catch(function(error){
       counter.dataset.status='error';
       updateVisitCounterLabel();
       console.error('Failed to load page visit count',error);
     })
     .finally(function(){
       if(timeoutId!==null)window.clearTimeout(timeoutId);
     });
 }
 function currentReadingPoint(){
   var y=Math.max(0,window.scrollY||window.pageYOffset||0);
   var sections=[].slice.call(document.querySelectorAll('main article[id],main .part-band[id]'));
   var current=null;
   sections.forEach(function(section){
     if(section.getBoundingClientRect().top+y<=y+80)current=section;
   });
   var sectionTop=current?current.getBoundingClientRect().top+y:0;
   return{y:y,sectionId:current?current.id:'',offset:current?y-sectionTop:0,updatedAt:Date.now()};
 }
 function readStoredReadingPoint(key){
   try{
     var stored=localStorage.getItem(key);
     if(!stored)return null;
     var point=JSON.parse(stored);
     if(!point||!Number.isFinite(point.y)||point.y<0){
       readingStorageUnavailable=true;
       return null;
     }
     return{
       y:point.y,
       sectionId:typeof point.sectionId==='string'?point.sectionId:'',
       offset:Number.isFinite(point.offset)?point.offset:0
     };
   }catch(error){
     readingStorageUnavailable=true;
     return null;
   }
 }
 function readingPointY(point){
   var y=point.y;
   var section=point.sectionId&&document.getElementById(point.sectionId);
   if(section&&Number.isFinite(point.offset))y=section.getBoundingClientRect().top+window.scrollY+point.offset;
   return Math.max(0,Math.min(y,document.documentElement.scrollHeight-window.innerHeight));
 }
 function clearReadingBookmarkHighlight(){
   if(readingBookmarkHighlightTimer!==null){
     window.clearTimeout(readingBookmarkHighlightTimer);
     readingBookmarkHighlightTimer=null;
   }
   if(activeReadingBookmarkTarget){
     activeReadingBookmarkTarget.classList.remove('bookmark-target');
     activeReadingBookmarkTarget=null;
   }
 }
 function highlightReadingBookmark(){
   clearReadingBookmarkHighlight();
   if(!savedReadingBookmark||!savedReadingBookmark.sectionId)return;
   var target=document.getElementById(savedReadingBookmark.sectionId);
   if(!target||!target.matches('main article[id],main .part-band[id]'))return;
   activeReadingBookmarkTarget=target;
   target.classList.add('bookmark-target');
   readingBookmarkHighlightTimer=window.setTimeout(function(){
     if(activeReadingBookmarkTarget===target){
       target.classList.remove('bookmark-target');
       activeReadingBookmarkTarget=null;
     }
     readingBookmarkHighlightTimer=null;
   },2600);
 }
 function scrollToReadingPosition(top){
   var root=document.documentElement;
   var previous=root.style.scrollBehavior;
   root.style.scrollBehavior='auto';
   window.scrollTo(0,top);
   root.style.scrollBehavior=previous;
 }
 function saveReadingProgress(){
   if(readingSaveTimer){window.clearTimeout(readingSaveTimer);readingSaveTimer=null;}
   try{
     localStorage.setItem(readingProgressKey,JSON.stringify(currentReadingPoint()));
     readingStorageUnavailable=false;
     if(!document.getElementById('reading-panel').hidden)setReadingStatus('progressSaved');
   }catch(error){
     readingStorageUnavailable=true;
     setReadingStatus('storageError');
   }
 }
 function scheduleReadingProgressSave(){
   if(readingSaveTimer)window.clearTimeout(readingSaveTimer);
   readingSaveTimer=window.setTimeout(saveReadingProgress,800);
 }
 function setReadingPanelOpen(open,returnFocus){
   var panel=document.getElementById('reading-panel');
   var toggle=document.getElementById('reading-tools-toggle');
   if(!panel||!toggle)return;
   panel.hidden=!open;
   toggle.setAttribute('aria-expanded',String(open));
   if(open){
     setReadingStatus(readingStatusState);
     document.getElementById('reading-bookmark-save').focus();
   }else if(returnFocus){
     toggle.focus();
   }
 }
 function initializeColorTheme(){
   var root=document.documentElement;
   var themeMeta=document.querySelector('meta[name="theme-color"]');
   var status=document.getElementById('theme-status');
   var radios=[].slice.call(document.querySelectorAll('input[name="color-theme"]'));
   var options=[].slice.call(document.querySelectorAll('.theme-option[data-theme-value]'));
   var themes={
     classic:'#142238',
     forest:'#19372f',
     plum:'#272a3b'
   };
   if(!status||!radios.length)return;
   var theme=Object.prototype.hasOwnProperty.call(themes,root.dataset.theme)?root.dataset.theme:'classic';
   function setStatus(message){
     status.textContent=message;
   }
   function applyTheme(selected){
     if(!Object.prototype.hasOwnProperty.call(themes,selected))return false;
     root.dataset.theme=selected;
     if(themeMeta)themeMeta.content=themes[selected];
     radios.forEach(function(radio){radio.checked=radio.value===selected;});
     options.forEach(function(option){
       option.dataset.selected=String(option.dataset.themeValue===selected);
     });
     return true;
   }
   applyTheme(theme);
   if(root.dataset.themeStorage==='unavailable'){
     setStatus(document.documentElement.lang==='en'
       ?'Theme is active but could not be restored or saved on this device.'
       :'配色已应用，但无法读取本机保存状态。');
   }
   radios.forEach(function(radio){
     radio.addEventListener('change',function(){
       if(!radio.checked||!applyTheme(radio.value))return;
       try{
         localStorage.setItem('fdebok-color-theme-v1',radio.value);
         delete root.dataset.themeStorage;
         setStatus(document.documentElement.lang==='en'
           ?'Theme applied and saved on this device.'
           :'配色已应用并保存在本机。');
       }catch(error){
         root.dataset.themeStorage='unavailable';
         console.error('Could not save the selected color theme',error);
         setStatus(document.documentElement.lang==='en'
           ?'Theme applied, but could not be saved on this device.'
           :'配色已应用，但无法保存在本机。');
       }
     });
   });
 }
 function initializeReadingTools(){
   var toggle=document.getElementById('reading-tools-toggle');
   var panel=document.getElementById('reading-panel');
   var saveBookmark=document.getElementById('reading-bookmark-save');
   var openBookmark=document.getElementById('reading-bookmark-open');
   var clearBookmark=document.getElementById('reading-bookmark-clear');
   var closePanel=document.getElementById('reading-panel-close');
   if(!toggle||!panel||!saveBookmark||!openBookmark||!clearBookmark||!closePanel)return;
   savedReadingBookmark=readStoredReadingPoint(readingBookmarkKey);
   updateReadingControls();
   setReadingStatus(readingStorageUnavailable?'storageError':'ready');
   toggle.addEventListener('click',function(){
     setReadingPanelOpen(panel.hidden,true);
   });
   closePanel.addEventListener('click',function(){setReadingPanelOpen(false,true);});
   saveBookmark.addEventListener('click',function(){
     var point=currentReadingPoint();
     try{
       localStorage.setItem(readingBookmarkKey,JSON.stringify(point));
       savedReadingBookmark=point;
       readingStorageUnavailable=false;
       updateReadingControls();
       setReadingStatus('bookmarkSaved');
       highlightReadingBookmark();
     }catch(error){
       readingStorageUnavailable=true;
       setReadingStatus('storageError');
     }
   });
   openBookmark.addEventListener('click',function(){
     if(!savedReadingBookmark)return;
     var top=readingPointY(savedReadingBookmark);
     var reduceMotion=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
     window.scrollTo({top:top,behavior:reduceMotion?'auto':'smooth'});
     highlightReadingBookmark();
     setReadingStatus('bookmarkOpened');
   });
   clearBookmark.addEventListener('click',function(){
     try{
       localStorage.removeItem(readingBookmarkKey);
       savedReadingBookmark=null;
       clearReadingBookmarkHighlight();
       updateReadingControls();
       setReadingStatus('bookmarkCleared');
     }catch(error){
       readingStorageUnavailable=true;
       setReadingStatus('storageError');
     }
   });
   document.addEventListener('click',function(event){
     if(!panel.hidden&&!panel.contains(event.target)&&!toggle.contains(event.target)){
       setReadingPanelOpen(false,false);
     }
   });
   document.addEventListener('keydown',function(event){
     if(event.key==='Escape'&&!panel.hidden)setReadingPanelOpen(false,true);
   });
   window.addEventListener('scroll',scheduleReadingProgressSave,{passive:true});
   window.addEventListener('pagehide',saveReadingProgress);
   document.addEventListener('visibilitychange',function(){
     if(document.visibilityState==='hidden')saveReadingProgress();
   });
   function restoreReadingProgress(){
     if(window.location.hash)return;
     var point=readStoredReadingPoint(readingProgressKey);
     if(!point){
       setReadingStatus(readingStorageUnavailable?'storageError':'ready');
       return;
     }
     window.requestAnimationFrame(function(){
       window.requestAnimationFrame(function(){
         scrollToReadingPosition(readingPointY(point));
         setReadingStatus('restored');
       });
     });
   }
   if(document.readyState==='complete')window.setTimeout(restoreReadingProgress,0);
   else window.addEventListener('load',restoreReadingProgress,{once:true});
 }
 function nodes(){var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null,false),a=[],n;while(n=w.nextNode()){var p=n.parentNode;if(!p)continue;var tg=p.nodeName;if(tg==='SCRIPT'||tg==='STYLE'||p.closest('.langbar'))continue;if(n.nodeValue&&n.nodeValue.trim())a.push(n);}return a;}
 function setLang(lang){
   if(lang==='en'){nodes().forEach(function(n){var raw=n.nodeValue,t=raw.trim();if(ENG[t]!==undefined&&ENG[t]!==t){if(n._zh===undefined)n._zh=raw;var i=raw.indexOf(t);n.nodeValue=raw.slice(0,i)+ENG[t]+raw.slice(i+t.length);}});}
   else{nodes().forEach(function(n){if(n._zh!==undefined)n.nodeValue=n._zh;});}
   [].forEach.call(document.querySelectorAll('[placeholder]'),function(el){if(!el._ph)el._ph=el.getAttribute('placeholder');el.setAttribute('placeholder',lang==='en'?(ATTR[el._ph]||el._ph):el._ph);});
   var isEnglish=lang==='en';
   document.documentElement.lang=isEnglish?'en':'zh-CN';
   var pageTitle=isEnglish
     ?'FDEBOK: Forward Deployed Engineer Guide & Handbook'
     :'FDEBOK｜前线部署工程师知识体系指南（FDE 指南）';
   var pageDescription=isEnglish
     ?'The FDEBOK guide explains what a Forward Deployed Engineer (FDE) does, the role\'s skills and career paths, and how to deliver enterprise AI—from discovery and engineering through evaluation and operations.'
     :'FDEBOK：免费中英双语前线部署工程师知识体系指南与实践手册。介绍 Forward Deployed Engineer（FDE）是什么、岗位职责、能力模型、职业发展，以及企业 AI 项目交付、评测运维和现场模板。';
   var sharePageDescription=isEnglish
     ?'A 22-chapter guide to the Forward Deployed Engineer role, skills and career development, with practical enterprise AI delivery, evaluation, operations, and field templates.'
     :'FDE 是什么？FDEBOK 是面向前线部署工程师的中英双语知识体系指南与实践手册，覆盖岗位职责、能力模型、职业发展、企业 AI 交付、评测运维和现场模板。';
   document.title=pageTitle;
   var description=document.querySelector('meta[name="description"]');
   if(description)description.content=pageDescription;
   var shareTitle=document.querySelector('meta[property="og:title"]');
   var shareDescription=document.querySelector('meta[property="og:description"]');
   var twitterTitle=document.querySelector('meta[name="twitter:title"]');
   var twitterDescription=document.querySelector('meta[name="twitter:description"]');
   var openGraphLocale=document.querySelector('meta[property="og:locale"]');
   var openGraphAlternateLocale=document.querySelector('meta[property="og:locale:alternate"]');
   var canonical=document.querySelector('link[rel="canonical"]');
   var openGraphUrl=document.querySelector('meta[property="og:url"]');
   var openGraphImage=document.querySelector('meta[property="og:image"]');
   var openGraphSecureImage=document.querySelector('meta[property="og:image:secure_url"]');
   var twitterImage=document.querySelector('meta[name="twitter:image"]');
   var canonicalUrl=isEnglish?'https://www.fdebok.com/en/':'https://www.fdebok.com/';
   var shareImageUrl=isEnglish?'https://www.fdebok.com/share-card-en-v6.png':'https://www.fdebok.com/share-card-zh-v6.png';
   if(shareTitle)shareTitle.content=pageTitle;
   if(shareDescription)shareDescription.content=sharePageDescription;
   if(twitterTitle)twitterTitle.content=pageTitle;
   if(twitterDescription)twitterDescription.content=sharePageDescription;
   if(openGraphLocale)openGraphLocale.content=isEnglish?'en_US':'zh_CN';
   if(openGraphAlternateLocale)openGraphAlternateLocale.content=isEnglish?'zh_CN':'en_US';
   if(canonical)canonical.href=canonicalUrl;
   if(openGraphUrl)openGraphUrl.content=canonicalUrl;
   if(openGraphImage)openGraphImage.content=shareImageUrl;
   if(openGraphSecureImage)openGraphSecureImage.content=shareImageUrl;
   if(twitterImage)twitterImage.content=shareImageUrl;
   var nav=document.querySelector('nav.toc');
   var search=document.getElementById('tq');
   var topButton=document.getElementById('top');
   var readingToggle=document.getElementById('reading-tools-toggle');
   var readingClose=document.getElementById('reading-panel-close');
   var languageGroup=document.querySelector('.langbar');
   if(nav)nav.setAttribute('aria-label',isEnglish?'Chapter navigation':'章节导航');
   if(search)search.setAttribute('aria-label',isEnglish?'Filter chapters by keyword':'输入关键词筛选章节');
   if(topButton){
     topButton.setAttribute('aria-label',isEnglish?'Back to top':'返回顶部');
     topButton.title=isEnglish?'Back to top':'返回顶部';
   }
   if(readingToggle){
     readingToggle.setAttribute('aria-label',isEnglish?'Reading and display settings':'阅读与显示设置');
     readingToggle.title=isEnglish?'Reading and display settings':'阅读与显示设置';
   }
   if(readingClose){
     readingClose.setAttribute('aria-label',isEnglish?'Close reading panel':'关闭阅读面板');
     readingClose.title=isEnglish?'Close':'关闭';
   }
   if(languageGroup)languageGroup.setAttribute('aria-label',isEnglish?'Language selector':'语言切换');
   document.querySelectorAll('.tw').forEach(function(w){
     if(!w.dataset.labelZh)w.dataset.labelZh=w.getAttribute('aria-label')||'可横向滚动的数据表格';
     w.setAttribute('aria-label',isEnglish?(ENG[w.dataset.labelZh]||'Scrollable data table'):w.dataset.labelZh);
   });
   var zh=document.getElementById('btnzh'),en=document.getElementById('btnen');
   if(zh&&en){
     zh.classList.toggle('on',!isEnglish);en.classList.toggle('on',isEnglish);
     zh.setAttribute('aria-pressed',String(!isEnglish));en.setAttribute('aria-pressed',String(isEnglish));
     zh.setAttribute('aria-label',isEnglish?'中文 — Switch to Chinese':'中文 — 切换到中文');
     en.setAttribute('aria-label',isEnglish?'EN — Switch to English':'EN — 切换到英文');
   }
   var assessmentProgress=document.getElementById('self-check-progress');
   if(assessmentProgress)assessmentProgress.setAttribute('aria-label',isEnglish?'Self-assessment progress':'自查完成进度');
   updateReadingControls();
   setReadingStatus(readingStatusState);
   updateVisitCounterLabel();
   renderSelfAssessment();
   renderDomainChecklist();
 }
 function initializeSharing(){
   var trigger=document.getElementById('share-trigger');
   var panel=document.getElementById('share-panel');
   var close=document.getElementById('share-close');
   var nativeButton=document.getElementById('share-native');
   var copyTextButton=document.getElementById('share-copy-text');
   var copyLinkButton=document.getElementById('share-copy-link');
   var quickActions=document.getElementById('share-quick-actions');
   var quickCopyInput=document.getElementById('share-quick-copy');
   var quickCopyButton=document.getElementById('share-quick-copy-button');
   var openPlatform=document.getElementById('share-open-platform');
   var urlInput=document.getElementById('share-url');
   var status=document.getElementById('share-status');
   var qr=document.getElementById('share-qr-image');
   var caption=document.getElementById('share-preview-caption');
   var previewTitle=document.getElementById('share-preview-title');
   var previewKicker=document.getElementById('share-preview-kicker');
   var platformNote=document.getElementById('share-platform-note');
   var qrNote=document.getElementById('share-qr-note');
   var intro=document.getElementById('share-intro');
   var contentNode=document.getElementById('share-content-data');
   if(!trigger||!panel||!close||!nativeButton||!copyTextButton||!copyLinkButton||
      !quickActions||!quickCopyInput||!quickCopyButton||
      !openPlatform||!urlInput||!status||!qr||!caption||!previewTitle||
      !previewKicker||!platformNote||!qrNote||!intro||!contentNode)return;
   var isEnglish=document.documentElement.lang==='en';
   var locale=isEnglish?'en':'zh';
   var quickShareUrl=isEnglish
     ?'https://www.fdebok.com/en/?share=brand-v6'
     :'https://www.fdebok.com/?share=brand-v6';
   qr.src=isEnglish?'/share-qr-en.png':'/share-qr-zh.png';
   qr.alt=isEnglish?'QR code for the FDEBOK English guide':'扫码访问 FDEBOK 中文指南';
   nativeButton.hidden=typeof navigator.share!=='function';
   var content;
   try{content=JSON.parse(contentNode.textContent)[locale];}
   catch(error){
     console.error('Failed to read platform-specific sharing content',error);
     setStatus(isEnglish?'Share content is unavailable. Copy the page URL instead.':'分享内容暂不可用，请复制页面链接。');
     copyTextButton.disabled=true;
     copyLinkButton.disabled=true;
     return;
   }
   if(!content||typeof content!=='object'){
     console.error('Platform-specific sharing content is missing for locale',locale);
     setStatus(isEnglish?'Share content is unavailable. Copy the page URL instead.':'分享内容暂不可用，请复制页面链接。');
     copyTextButton.disabled=true;
     copyLinkButton.disabled=true;
     return;
   }
   var allowedPlatforms=Object.keys(content);
   var platformButtons=[].slice.call(panel.querySelectorAll('[data-share-platform]'));
   platformButtons.forEach(function(button){
     var enabled=allowedPlatforms.indexOf(button.dataset.sharePlatform)!==-1;
     button.hidden=!enabled;
     button.setAttribute('aria-pressed','false');
   });
   var selectedPlatform=locale==='zh'?'wechat':'linkedin';
   var selectedContent=null;
   var shareUrl='';
   var copyText='';
   function setStatus(message){status.textContent=message;}
   function setOpen(open,returnFocus,mode){
     if(open){
       panel.dataset.mode=mode||'full';
       quickActions.hidden=panel.dataset.mode!=='quick';
     }else{
       panel.dataset.mode='full';
       quickActions.hidden=true;
     }
     panel.hidden=!open;
     trigger.setAttribute('aria-expanded',String(open));
     if(open)close.focus();
     else if(returnFocus)trigger.focus();
   }
   function isMobileViewport(){
     return !!(window.matchMedia&&window.matchMedia('(max-width: 660px)').matches);
   }
   function openQuickFallback(message){
     quickCopyInput.value=copyText+'\n\n'+quickShareUrl;
     setOpen(true,false,'quick');
     setStatus(message);
   }
   function fallbackCopy(value){
     var textArea=document.createElement('textarea');
     textArea.value=value;
     textArea.readOnly=true;
     textArea.style.position='fixed';
     textArea.style.opacity='0';
     document.body.appendChild(textArea);
     var copied=false;
     try{
       textArea.select();
       copied=document.execCommand('copy');
     }catch(error){console.error('Fallback clipboard copy failed',error);}
     finally{textArea.remove();}
     return copied;
   }
   function selectForManualCopy(target){
     target.focus();
     if(target===caption&&window.getSelection&&document.createRange){
       var selection=window.getSelection();
       var range=document.createRange();
       range.selectNodeContents(caption);
       selection.removeAllRanges();
       selection.addRange(range);
     }else if(typeof target.select==='function')target.select();
   }
   function copyValue(value,successMessage,failureMessage,focusTarget){
     function reportCopy(copied){
       if(copied){setStatus(successMessage);return;}
       setStatus(failureMessage);
       try{selectForManualCopy(focusTarget);}
       catch(error){console.error('Could not select text for manual copying',error);}
     }
     if(navigator.clipboard&&window.isSecureContext){
       try{
         navigator.clipboard.writeText(value).then(function(){reportCopy(true);}).catch(function(){
           reportCopy(fallbackCopy(value));
         });
       }catch(error){
         console.error('Clipboard API failed',error);
         reportCopy(fallbackCopy(value));
       }
     }else reportCopy(fallbackCopy(value));
   }
   function updatePlatform(platform){
     selectedContent=content[platform];
     if(!selectedContent){
       console.error('Unknown sharing platform selected',platform);
       setStatus(isEnglish?'This share option is unavailable. Copy the share link instead.':'分享入口暂不可用，请复制分享链接。');
       return;
     }
     selectedPlatform=platform;
     shareUrl='https://www.fdebok.com/share/'+locale+'/'+platform+'/';
     copyText=selectedContent.caption;
     quickCopyInput.value=copyText+'\n\n'+quickShareUrl;
     platformButtons.forEach(function(button){
       button.setAttribute('aria-pressed',String(button.dataset.sharePlatform===platform));
     });
     previewTitle.textContent=selectedContent.title;
     caption.textContent=selectedContent.caption;
     previewKicker.textContent='FDEBOK · '+selectedContent.kicker;
     urlInput.value=shareUrl;
     platformNote.textContent=selectedContent.note;
     qrNote.textContent=selectedContent.qrNote;
     openPlatform.hidden=true;
     openPlatform.removeAttribute('href');
     if(platform==='facebook'){
       openPlatform.href='https://www.facebook.com/sharer/sharer.php?'+new URLSearchParams({u:shareUrl});
       openPlatform.textContent=isEnglish?'Share on Facebook':'分享到 Facebook';
       openPlatform.hidden=false;
     }else if(platform==='linkedin'){
       openPlatform.href='https://www.linkedin.com/sharing/share-offsite/?'+new URLSearchParams({url:shareUrl});
       openPlatform.textContent=isEnglish?'Share on LinkedIn':'分享到 LinkedIn';
       openPlatform.hidden=false;
     }else if(platform==='x'){
       openPlatform.href='https://twitter.com/intent/tweet?'+new URLSearchParams({url:shareUrl,text:copyText});
       openPlatform.textContent=isEnglish?'Post on X':'发布到 X';
       openPlatform.hidden=false;
     }
     setStatus('');
   }
   function shareFromDevice(quick){
     if(typeof navigator.share!=='function'){
       if(quick)openQuickFallback(isEnglish
         ?'Device sharing is unavailable. Copy the content and paste it into your app.'
         :'设备分享暂不可用，请复制内容后在应用中粘贴。');
       else setStatus(isEnglish?'System sharing is unavailable. Copy the link or scan the QR code.':'暂不支持系统分享，请复制链接或扫码。');
       return;
     }
     if(!selectedContent)return;
     if(quick)openQuickFallback(isEnglish
       ?'Opening device sharing. After choosing an app, select a recipient or feed and confirm the share in that app.'
       :'正在打开系统分享。选择目标 App 后，请在 App 内继续选择好友或朋友圈并确认发送。');
     var sharePromise;
     try{
       sharePromise=quick
         ?navigator.share({url:quickShareUrl})
         :navigator.share({
           title:'FDEBOK · '+selectedContent.title,
           text:copyText,
           url:shareUrl
         });
     }catch(error){
       console.error('System sharing failed',error);
       if(quick)openQuickFallback(isEnglish
         ?'Could not open device sharing. Copy the content and paste it into your app.'
         :'无法打开设备分享，请复制内容后在应用中粘贴。');
       else setStatus(isEnglish?'Could not open the share sheet. Copy the link or scan the QR code.':'无法打开系统分享，请复制链接或扫码。');
       return;
     }
     Promise.resolve(sharePromise).then(function(){
       setStatus(quick
         ?(isEnglish
           ?'Returned to the page. Only the target app can confirm whether it sent the share. If it did not, copy the content and try again.'
           :'已返回网页。分享结果由目标 App 确认；如未成功，可复制内容后重试。')
         :'');
     }).catch(function(error){
       if(error&&error.name==='AbortError'){
         if(quick)setStatus(isEnglish
           ?'Sharing was cancelled. Copy the message and link, then paste them into any app when ready.'
           :'分享已取消。你可以复制配文和链接，稍后在任意 App 粘贴。');
         return;
       }
       console.error('System sharing failed',error);
       if(quick)openQuickFallback(isEnglish
         ?'Could not open device sharing. Copy the content and paste it into your app.'
         :'无法打开设备分享，请复制内容后在应用中粘贴。');
       else setStatus(isEnglish?'Could not open the share sheet. Copy the link or scan the QR code.':'无法打开系统分享，请复制链接或扫码。');
     });
   }
   trigger.addEventListener('click',function(){
     if(isMobileViewport()){
       if(typeof navigator.share==='function'&&selectedContent)shareFromDevice(true);
       else openQuickFallback(isEnglish
         ?'Device sharing isn’t available here. Copy once, then paste into your preferred app.'
         :'当前浏览器不支持系统分享。复制后打开微信或抖音粘贴；网页无法代替 App 内转发。');
       return;
     }
     setOpen(panel.hidden,false,'full');
   });
   close.addEventListener('click',function(){setOpen(false,true);});
   platformButtons.forEach(function(button){
     button.addEventListener('click',function(){updatePlatform(button.dataset.sharePlatform);});
   });
   copyTextButton.addEventListener('click',function(){
     if(selectedContent)copyValue(copyText,isEnglish?'Post text copied.':'配文已复制。',
       isEnglish?'Copy failed. Select the post text and copy it manually.':'复制失败，请手动选择配文复制。',caption);
   });
   copyLinkButton.addEventListener('click',function(){
     if(selectedContent)copyValue(shareUrl,isEnglish?'Link copied.':'链接已复制。',
       isEnglish?'Copy failed. Select the URL and copy it manually.':'复制失败，请手动选择链接复制。',urlInput);
   });
   quickCopyButton.addEventListener('click',function(){
     if(selectedContent)copyValue(copyText+'\n\n'+quickShareUrl,
       isEnglish?'Message and link copied. Open your preferred app to paste them.':'分享内容已复制。打开微信或抖音即可粘贴。',
       isEnglish?'Copy failed. Select the share message and link and copy them manually.':'复制失败，请手动选择分享内容复制。',
       quickCopyInput);
   });
   nativeButton.addEventListener('click',function(){
     shareFromDevice(false);
   });
   if(!content[selectedPlatform])selectedPlatform=allowedPlatforms[0];
   if(selectedPlatform)updatePlatform(selectedPlatform);
   document.addEventListener('keydown',function(event){
     if(event.key==='Escape'&&!panel.hidden)setOpen(false,true);
   });
 }
 window.addEventListener('DOMContentLoaded',function(){
   initializeDomainChecklist();
   var zh=document.getElementById('btnzh'),en=document.getElementById('btnen');
   var isEnglishRoute=/^\/en(?:\/|$)/.test(window.location.pathname);
   if(zh)zh.addEventListener('click',function(){
     if(isEnglishRoute)window.location.assign('/');
     else setLang('zh');
   });
   if(en)en.addEventListener('click',function(){
     if(isEnglishRoute)setLang('en');
     else window.location.assign('/en/');
   });
   setLang(isEnglishRoute?'en':'zh');
   initializeColorTheme();
   initializeSharing();
   initializeReadingTools();
   loadPageVisitCount();
   var selfCheckForm=document.getElementById('self-check-form');
   if(selfCheckForm){
     selfCheckForm.addEventListener('change',renderSelfAssessment);
     selfCheckForm.addEventListener('reset',function(){setTimeout(renderSelfAssessment,0);});
     renderSelfAssessment();
   }
 });
 document.addEventListener('copy',function(event){
   var selection=window.getSelection();
   if(!selection||selection.isCollapsed||!selection.rangeCount||!event.clipboardData||
      !isBookContent(selection.anchorNode)||!isBookContent(selection.focusNode))return;
   var canonical=document.querySelector('link[rel="canonical"]');
   var sourceUrl=canonical?canonical.href:window.location.href.split('#')[0];
   var termsUrl=sourceUrl+'#rights';
   var licenseUrl='https://www.fdebok.com/LICENSE';
   var isEnglish=document.documentElement.lang==='en';
   var notice=isEnglish
     ?'© 2026 FDEBOK (fdebok.com). Licensed under the MIT License (SPDX: MIT). Use, modification, redistribution, and commercial sale are permitted. Copies or substantial portions must include the copyright and permission notice. Please note changes and do not imply official endorsement.'
     :'© 2026 FDEBOK（fdebok.com）。本内容采用 MIT 许可证（SPDX: MIT），允许使用、修改、再发布及商业销售。分发副本或实质部分时须附带版权与许可声明。建议注明改动，且勿暗示获得官方背书。';
   var plainText=selection.toString()+'\n\n---\n'+notice+
     '\n'+(isEnglish?'Source: ':'来源：')+sourceUrl+
     '\n'+(isEnglish?'License: ':'许可文本：')+licenseUrl+
     '\n'+(isEnglish?'License notes: ':'许可说明：')+termsUrl;
   var copied=document.createElement('div');
   copied.appendChild(selection.getRangeAt(0).cloneContents());
   copied.appendChild(document.createElement('hr'));
   var noticeLine=document.createElement('p');
   noticeLine.textContent=notice;
   copied.appendChild(noticeLine);
   var sourceLine=document.createElement('p');
   sourceLine.appendChild(document.createTextNode((isEnglish?'Source: ':'来源：')));
   var sourceLink=document.createElement('a');
   sourceLink.href=sourceUrl;sourceLink.rel='noopener noreferrer';sourceLink.textContent=sourceUrl;
   sourceLine.appendChild(sourceLink);copied.appendChild(sourceLine);
   var licenseLine=document.createElement('p');
   licenseLine.appendChild(document.createTextNode((isEnglish?'Full license: ':'完整许可文本：')));
   var licenseLink=document.createElement('a');
   licenseLink.href=licenseUrl;licenseLink.rel='noopener noreferrer';licenseLink.textContent=licenseUrl;
   licenseLine.appendChild(licenseLink);copied.appendChild(licenseLine);
   var termsLine=document.createElement('p');
   termsLine.appendChild(document.createTextNode((isEnglish?'License notes: ':'许可说明：')));
   var termsLink=document.createElement('a');
   termsLink.href=termsUrl;termsLink.rel='noopener noreferrer';termsLink.textContent=termsUrl;
   termsLine.appendChild(termsLink);copied.appendChild(termsLine);
   event.clipboardData.setData('text/plain',plainText);
   event.clipboardData.setData('text/html',copied.innerHTML);
   event.preventDefault();
 });
 function isBookContent(node){
   var element=node&&node.nodeType===1?node:node&&node.parentElement;
   return !!(element&&element.closest('.cover,main,footer.pg'));
 }
})();