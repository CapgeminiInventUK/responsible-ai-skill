"""Offline structural checks and fixed-rule execution, not policy approval."""
import argparse, hashlib, json, re, sys, uuid, zipfile
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
STATUSES=['Supported','Partly supported','Not evidenced','Conflicting evidence','Not assessed']
UNKNOWN={'','TBC','Not supplied','Unknown'}
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def schema_errors(d,n):
    return [str(list(e.path))+': '+e.message for e in Draft202012Validator(load(ROOT/'assets/schemas'/n),format_checker=FormatChecker()).iter_errors(d)]
def unique(rows,key,errors):
    if len(rows)!=len({r[key] for r in rows}):errors.append('Duplicate '+key)
    return {r[key]:r for r in rows}
def pack_errors(p):
    e=schema_errors(p,'policy-pack.schema.json')
    if e:return e
    if p['status']=='Blocked':e.append('Pack is Blocked; supply completed authorised baseline.')
    for k in ['owner','jurisdiction','scope']:
        if p[k] in UNKNOWN:e.append('Missing pack '+k)
    if not p['effective_date'] or not p['review_date']:e.append('Missing effective/review dates')
    elif not date.fromisoformat(p['effective_date'])<=datetime.now(timezone.utc).date()<=date.fromisoformat(p['review_date']):e.append('Pack outside effective/review window')
    ss=unique(p['sources'],'source_id',e);cs=unique(p['controls'],'control_id',e);rs=unique(p['severity_rules'],'rule_id',e)
    if not cs or not ss:e.append('Controls and sources required')
    if p['status']=='Approved':
        for kind in ['Policy','Severity rules']:
            if not any(a['kind']==kind and a['approver'] not in UNKNOWN and a['decision_locator'] not in UNKNOWN for a in p['approvals']):e.append('Missing approval: '+kind)
    for cid,c in cs.items():
        if c['source_id'] not in ss:e.append(cid+': unknown source')
        if not c['expected_evidence']:e.append(cid+': missing evidence criteria')
        if len(c['rule_ids'])!=len(set(c['rule_ids'])):e.append(cid+': duplicate rule links')
        for rid in c['rule_ids']:
            if rid not in rs or rs[rid]['control_id']!=cid:e.append(cid+': invalid rule link')
        for status in STATUSES:
            if len([r for r in rs.values() if r['control_id']==cid and r['when_evidence_status']==status and r['rule_id'] in c['rule_ids']])!=1:e.append(cid+': exactly one rule needed for '+status)
    for r in rs.values():
        if r['control_id'] not in cs or r['rule_id'] not in cs[r['control_id']]['rule_ids']:e.append('Orphan rule')
        if r['hard_gate']=='Triggered' and r['severity']=='None':e.append('Triggered gate needs severity')
    return e
def apply_rule(p,cid,status):
    allowed=next((c['rule_ids'] for c in p['controls'] if c['control_id']==cid),[])
    rows=[r for r in p['severity_rules'] if r['control_id']==cid and r['when_evidence_status']==status and r['rule_id'] in allowed]
    return {k:rows[0][k] for k in ['severity','rule_id','hard_gate']} if len(rows)==1 else dict(severity='Unassigned',rule_id=None,hard_gate='Unassigned')
def assessment_errors(a,p):
    e=schema_errors(a,'assessment.schema.json')+pack_errors(p)
    if e:return e
    m=a['metadata'];ev=unique(a['evidence_manifest'],'evidence_id',e);rr=unique(a['control_results'],'control_id',e);cc=unique(a['concerns'],'concern_id',e);dd=unique(a['decisions'],'decision_id',e);unique(a['open_questions'],'question_id',e)
    cs={c['control_id']:c for c in p['controls']}
    if set(rr)!=set(cs):e.append('Control coverage mismatch')
    if not ev:e.append('Evidence manifest empty')
    for k in ['run_id','project_id','project_name','purpose','users_and_impacts','lifecycle_stage','jurisdiction','evidence_boundary','handling_confirmation','output_location','assessor']:
        if m[k] in UNKNOWN:e.append('Unconfirmed required intake: '+k)
    if m['assessor_independent']=='Not supplied':e.append('Independence not confirmed')
    for ak,pk in [('pack_id','pack_id'),('pack_version','version'),('pack_status','status')]:
        if m[ak]!=p[pk]:e.append('Pack metadata mismatch: '+ak)
    label='Design test - unapproved baseline' if p['status']=='Draft' else 'Approved baseline - draft assessment'
    if m['baseline_label']!=label:e.append('Baseline label mismatch')
    if p['status']=='Draft' and m['design_test_authorisation'] in UNKNOWN:e.append('Design-test authorisation required')
    for row in ev.values():
        if row['project_id']!=m['project_id']:e.append('Cross-project evidence')
    def ids(values,mapping):
        for v in values:
            if v not in mapping:e.append('Unknown reference: '+str(v))
    def refs(values):
        for r in values:
            ids([r['evidence_id']],ev)
            if r['evidence_id'] in ev and ev[r['evidence_id']]['processing_result'] not in ['Reviewed','Partly reviewed']:e.append('Citation to unreviewed evidence')
    def human(did,kind,key,value):
        d=dd.get(did)
        return bool(d and d['actor_type']=='Human decision' and d['kind']==kind and value in d[key] and d['decision_maker'] not in UNKNOWN and d['authority_as_supplied'] not in UNKNOWN)
    for d in dd.values():ids(d['control_ids'],cs);ids(d['concern_ids'],cc);ids(d['evidence_ids'],ev)
    for q in a['open_questions']:
        ids(q['affected_control_ids'],cs)
        if q['decision_id'] is not None:ids([q['decision_id']],dd)
        if q['state']=='Resolved' and q['answer'] in UNKNOWN:e.append('Resolved question lacks answer')
    for cid,r in rr.items():
        refs(r['evidence_refs'])
        if cid not in cs:continue
        if r['applicability']=='Applicable':
            if any(r[k]!=v for k,v in apply_rule(p,cid,r['evidence_status']).items()):e.append(cid+': fixed rule mismatch')
            if r['evidence_status'] in ['Supported','Partly supported','Conflicting evidence'] and not r['evidence_refs']:e.append(cid+': citations required')
            if (r['severity']!='None' or r['hard_gate']=='Triggered') and not any(c['control_id']==cid for c in cc.values()):e.append(cid+': concern required')
        else:
            if r['evidence_status']!='Not assessed' or r['severity']!='None' or r['rule_id'] is not None or r['hard_gate']!='Not applicable':e.append(cid+': pending/excluded outcome invalid')
            if r['applicability']=='Not applicable' and (cs[cid]['mandatory'] or cs[cid]['high_impact']) and not human(r['applicability_decision_id'],'Applicability exception','control_ids',cid):e.append(cid+': exclusion needs human confirmation')
        if r['applicability_decision_id'] is not None:ids([r['applicability_decision_id']],dd)
    for nid,c in cc.items():
        refs(c['evidence_refs']);r=rr.get(c['control_id'])
        if not r or any(c[k]!=r[k] for k in ['severity','rule_id','hard_gate']):e.append(nid+': concern/control mismatch')
        if not c['evidence_refs'] and c['evidence_gap'] in UNKNOWN:e.append(nid+': evidence or explicit gap required')
        ids(c['closure_evidence_ids'],ev)
        if c['closure_decision_id'] is not None:ids([c['closure_decision_id']],dd)
        for h in c['history']:
            ids(h['evidence_ids'],ev)
            if h['decision_id'] is not None:ids([h['decision_id']],dd)
        if c['state']=='Closed':
            if not c['closure_evidence_ids'] or not human(c['closure_decision_id'],'Closure','concern_ids',nid):e.append(nid+': closure requires evidence and human decision')
            else:
                if not set(c['closure_evidence_ids']).issubset(dd[c['closure_decision_id']]['evidence_ids']):e.append(nid+': closure evidence absent from decision')
                if any(ev[x]['processing_result'] not in ['Reviewed','Partly reviewed'] for x in c['closure_evidence_ids'] if x in ev):e.append(nid+': closure evidence unreviewed')
    if m['completion_status']=='Complete':
        if any(q['blocking'] and q['state']=='Open' for q in a['open_questions']):e.append('Complete run has blocking questions')
        if any(r['applicability']=='Pending review' or (r['applicability']=='Applicable' and r['evidence_status']=='Not assessed') for r in rr.values()):e.append('Complete run has unassessed controls')
    if a['comparison']['mode']=='Compared' and not a['comparison']['previous_run_id']:e.append('Previous run ID required')
    return e
def scalar(v):
    if isinstance(v,(dict,list)):return json.dumps(v,ensure_ascii=False)
    return 'Not supplied' if v is None else str(v).replace('\n',' / ')
def md(v, depth=0):
    indent='  '*depth
    if isinstance(v,dict):
        rows=[]
        for k,x in v.items():
            label=k.replace('_',' ').capitalize()
            if isinstance(x,(dict,list)) and x:
                rows.append(indent+'- **'+label+':**\n'+md(x,depth+1))
            else:
                rows.append(indent+'- **'+label+':** '+('None recorded.' if x==[] else scalar(x)))
        return '\n'.join(rows)
    if isinstance(v,list):
        return '\n'.join(indent+'- Record '+str(i+1)+'\n'+md(x,depth+1) if isinstance(x,dict) else indent+'- '+scalar(x) for i,x in enumerate(v)) or indent+'None recorded.'
    return indent+scalar(v)
def render(a):
    counts={'control_count':len(a['control_results']),'applicable':sum(r['applicability']=='Applicable' for r in a['control_results']),'evidence_status_counts':dict(Counter(r['evidence_status'] for r in a['control_results'] if r['applicability']=='Applicable')),'unresolved_concerns_by_severity':dict(Counter(c['severity'] for c in a['concerns'] if c['state']!='Closed')),'triggered_hard_gates':[r['control_id'] for r in a['control_results'] if r['hard_gate']=='Triggered']}
    values=dict(a,counts=counts)
    return re.sub(r'\{\{([a-z_]+)\}\}',lambda m:md(values[m.group(1)]),(ROOT/'assets/report.template.md').read_text())
def export_package(a,p,out):
    errors=assessment_errors(a,p)
    if errors:raise ValueError('\n'.join(errors))
    blobs={'assessment.json':(json.dumps(a,indent=2,ensure_ascii=False)+'\n').encode(),'assessment-report.md':render(a).encode(),'policy-pack.json':(json.dumps(p,indent=2,ensure_ascii=False)+'\n').encode()}
    manifest={'schema_version':'1.0.0','run_id':a['metadata']['run_id'],'created_at':datetime.now(timezone.utc).isoformat(),'files':{k:hashlib.sha256(v).hexdigest() for k,v in blobs.items()}}
    blobs['package-manifest.json']=json.dumps(manifest,indent=2).encode()
    if Path(out).exists():raise ValueError('Refusing to overwrite existing output')
    with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for k,v in blobs.items():z.writestr(k,v)
    with zipfile.ZipFile(out) as z:
        if z.testzip() is not None or any(hashlib.sha256(z.read(k)).hexdigest()!=v for k,v in manifest['files'].items()):raise ValueError('Export integrity failure')
    return manifest
def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='cmd',required=True)
    sub.add_parser('new-id')
    h=sub.add_parser('hash');h.add_argument('path')
    v=sub.add_parser('validate-pack');v.add_argument('pack')
    v=sub.add_parser('validate-assessment');v.add_argument('assessment');v.add_argument('--pack',required=True);v.add_argument('--report')
    r=sub.add_parser('rules');r.add_argument('pack');r.add_argument('control_id');r.add_argument('evidence_status',choices=STATUSES)
    r=sub.add_parser('render');r.add_argument('assessment');r.add_argument('output')
    x=sub.add_parser('export');x.add_argument('assessment');x.add_argument('pack');x.add_argument('output')
    a=parser.parse_args();errors=[]
    if a.cmd=='new-id':print('RUN-'+str(uuid.uuid4()));return 0
    if a.cmd=='hash':
        h=hashlib.sha256()
        with open(a.path,'rb') as f:
            for b in iter(lambda:f.read(1048576),b''):h.update(b)
        print(h.hexdigest());return 0
    if a.cmd=='validate-pack':errors=pack_errors(load(a.pack))
    elif a.cmd=='validate-assessment':
        data=load(a.assessment);errors=assessment_errors(data,load(a.pack))
        if not errors and a.report and Path(a.report).read_text()!=render(data):errors.append('Report differs from canonical rendered data')
    elif a.cmd=='rules':
        p=load(a.pack);errors=pack_errors(p)
        if not errors:print(json.dumps(apply_rule(p,a.control_id,a.evidence_status),indent=2));return 0
    elif a.cmd=='render':
        data=load(a.assessment);errors=schema_errors(data,'assessment.schema.json')
        if not errors:
            with open(a.output,'x',encoding='utf-8') as f:f.write(render(data))
            print('Rendered draft; full validation still required.');return 0
    elif a.cmd=='export':export_package(load(a.assessment),load(a.pack),a.output);print('Validated export created: '+a.output);return 0
    print(json.dumps({'valid':not errors,'errors':errors,'scope':'Implemented structural/semantic checks only; not policy approval or reasoning evaluation.'},indent=2));return int(bool(errors))
if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:print('Failed: '+str(exc),file=sys.stderr);sys.exit(1)
