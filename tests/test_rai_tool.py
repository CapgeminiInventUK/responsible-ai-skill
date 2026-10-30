"""Explicitly synthetic technical fixtures; no real policy controls."""
import copy, hashlib, importlib.util, json, tempfile, unittest, zipfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rai_tool',ROOT/'scripts/rai_tool.py');tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
def fixture():
 p=tool.load(ROOT/'assets/policy-pack/public-sector-rai.json');p.update(status='Draft',owner='Synthetic owner',jurisdiction='Synthetic jurisdiction',scope='Synthetic technical fixture',effective_date='2020-01-01',review_date='2099-12-31',sources=[dict(source_id='S1',title='Synthetic source',version_or_date='1',locator='Synthetic section 1')])
 p['controls']=[dict(control_id='C1',title='Synthetic control',domain='Synthetic',mandatory=True,high_impact=True,requirement_type='Mandatory requirement',source_id='S1',source_locator='Section 1',applicability_rule='Synthetic only',expected_evidence=['Synthetic evidence'],evidence_status_criteria={s:'Synthetic '+s for s in tool.STATUSES},rule_ids=['R'+str(i) for i in range(5)])]
 p['severity_rules']=[dict(rule_id='R'+str(i),control_id='C1',when_evidence_status=s,severity='None' if i==0 else 'High',hard_gate='Not triggered',rationale='Synthetic mapping') for i,s in enumerate(tool.STATUSES)]
 a=tool.load(ROOT/'assets/assessment.template.json');a['metadata']={k:'Synthetic supplied fact' for k in a['metadata']};now=datetime.now(timezone.utc).isoformat();a['metadata'].update(run_id='RUN-SYN',project_id='P1',project_name='Synthetic project',assessment_time=now,created_at=now,skill_version='0.1.0',review_context='Self-assessment',assessor_independent='No',pack_id=p['pack_id'],pack_version=p['version'],pack_status='Draft',baseline_label='Design test - unapproved baseline',design_test_authorisation='Explicit synthetic test authorisation',completion_status='Complete')
 a['evidence_manifest']=[dict(evidence_id='E1',filename='synthetic.txt',project_id='P1',version_or_date='1',owner='Not supplied',classification='Synthetic',source_locator='Uploaded synthetic fixture',processing_result='Reviewed',coverage='Section 1',limitations=[],sha256=None)]
 a['control_results']=[dict(control_id='C1',applicability='Applicable',applicability_reason='Synthetic',applicability_decision_id=None,evidence_status='Supported',evidence_refs=[dict(evidence_id='E1',locator='Section 1',locator_reliable=True)],source_facts='Synthetic fact',interpretation='Synthetic interpretation',finding='Synthetic finding',rationale='Synthetic rationale',limitations=[],severity='None',rule_id='R0',hard_gate='Not triggered')]
 return a,p
def concern(a):
 a['control_results'][0].update(evidence_status='Not evidenced',severity='High',rule_id='R2')
 a['concerns']=[dict(concern_id='N1',control_id='C1',rule_id='R2',severity='High',hard_gate='Not triggered',finding='Synthetic gap',rationale='Synthetic',evidence_refs=[],evidence_gap='Synthetic gap',state='Open',action='Supply synthetic evidence',proposed_owner='TBC',due_date='TBC',closure_evidence_required='Reviewed evidence',closure_evidence_ids=[],closure_decision_id=None,history=[])]
class Tests(unittest.TestCase):
 def test_valid(self):
  a,p=fixture();self.assertEqual(tool.assessment_errors(a,p),[])
 def test_blocked_pack(self):self.assertTrue(tool.pack_errors(tool.load(ROOT/'assets/policy-pack/public-sector-rai.json')))
 def test_ambiguous_rule(self):
  a,p=fixture();r=copy.deepcopy(p['severity_rules'][0]);r['rule_id']='EXTRA';p['severity_rules'].append(r);p['controls'][0]['rule_ids'].append('EXTRA');self.assertTrue(tool.pack_errors(p));self.assertEqual(tool.apply_rule(p,'C1','Supported')['severity'],'Unassigned')
 def test_rule_tamper(self):
  a,p=fixture();a['control_results'][0]['severity']='Low';self.assertTrue(tool.assessment_errors(a,p))
 def test_duplicate_ids(self):
  a,p=fixture();a['evidence_manifest']*=2;self.assertTrue(tool.assessment_errors(a,p))
 def test_unknown_citation(self):
  a,p=fixture();a['control_results'][0]['evidence_refs'][0]['evidence_id']='missing';self.assertTrue(tool.assessment_errors(a,p))
 def test_unreviewed_citation(self):
  a,p=fixture();a['evidence_manifest'][0]['processing_result']='Unreadable';self.assertTrue(tool.assessment_errors(a,p))
 def test_missing_control(self):
  a,p=fixture();a['control_results']=[];self.assertTrue(tool.assessment_errors(a,p))
 def test_cross_project(self):
  a,p=fixture();a['evidence_manifest'][0]['project_id']='OTHER';self.assertTrue(tool.assessment_errors(a,p))
 def test_draft_authorisation(self):
  a,p=fixture();a['metadata']['design_test_authorisation']='TBC';self.assertTrue(tool.assessment_errors(a,p))
 def test_approval_missing(self):
  a,p=fixture();p['status']='Approved';self.assertTrue(tool.pack_errors(p))
 def test_closure_blocked(self):
  a,p=fixture();concern(a);a['concerns'][0]['state']='Closed';self.assertTrue(tool.assessment_errors(a,p))
 def test_human_closure(self):
  a,p=fixture();concern(a);a['concerns'][0].update(state='Closed',closure_evidence_ids=['E1'],closure_decision_id='D1');a['decisions']=[dict(decision_id='D1',kind='Closure',actor_type='Human decision',decision_maker='Synthetic reviewer',authority_as_supplied='Synthetic authority',timestamp=a['metadata']['assessment_time'],rationale='Synthetic closure',control_ids=['C1'],concern_ids=['N1'],evidence_ids=['E1'])];self.assertEqual(tool.assessment_errors(a,p),[]);a['decisions'][0]['actor_type']='Model proposal';self.assertTrue(tool.assessment_errors(a,p))
 def test_exclusion(self):
  a,p=fixture();a['control_results'][0].update(applicability='Not applicable',evidence_status='Not assessed',severity='None',rule_id=None,hard_gate='Not applicable');self.assertTrue(tool.assessment_errors(a,p))
 def test_question(self):
  a,p=fixture();a['open_questions']=[dict(question_id='Q1',step='5',issue='Synthetic ambiguity',affected_control_ids=['C1'],material_effect='Synthetic effect',blocking=True,required_answer='Synthetic answer',respondent='TBC',state='Open',answer='Not supplied',decision_id=None)];self.assertTrue(tool.assessment_errors(a,p));a['metadata']['completion_status']='Partial';self.assertEqual(tool.assessment_errors(a,p),[])
 def test_export(self):
  a,p=fixture()
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'out.zip';m=tool.export_package(a,p,path)
   with zipfile.ZipFile(path) as z:
    self.assertEqual(len(z.namelist()),4)
    for n,h in m['files'].items():self.assertEqual(hashlib.sha256(z.read(n)).hexdigest(),h)
    self.assertEqual(z.read('assessment-report.md').decode(),tool.render(a))
   with self.assertRaises(ValueError):tool.export_package(a,p,path)
 def test_references(self):
  text=(ROOT/'SKILL.md').read_text();refs=sorted((ROOT/'references').glob('*.md'));self.assertEqual(len(refs),10)
  for i,p in enumerate(refs,1):self.assertTrue(p.name.startswith(f'{i:02d}-'));self.assertIn('references/'+p.name,text)
 def test_score_rejected(self):
  a,p=fixture();a['trust_score']=99;self.assertTrue(tool.assessment_errors(a,p))
if __name__=='__main__':unittest.main()
