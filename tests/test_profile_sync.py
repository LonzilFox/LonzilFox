"""Offline end-to-end checks for a new repository and changing Topics."""
from pathlib import Path
import tempfile, subprocess, sys, json, unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'sync_repos.py'
README = Path(__file__).resolve().parents[1] / 'README.md'
WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/sync-profile.yml'

class ProfileSyncTests(unittest.TestCase):
    def test_new_repo_and_topics_are_reflected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'scripts').mkdir()
            (root/'scripts/sync_repos.py').write_bytes(SCRIPT.read_bytes())
            (root/'README.md').write_bytes(README.read_bytes())
            fixture=root/'repositories.json'
            command=[sys.executable,str(root/'scripts/sync_repos.py'),'--target','profile','--fixture',str(fixture)]
            fixture.write_text(json.dumps([{'name':'First','topics':['category-tools'],'description':'Original tool'}]),encoding='utf-8')
            subprocess.run(command,check=True,capture_output=True,text=True)
            original=(root/'README.md').read_text(encoding='utf-8')
            self.assertIn('First',original)
            self.assertNotIn('Second',original)
            fixture.write_text(json.dumps([{'name':'First','topics':['category-tools'],'description':'Original tool'}, {'name':'Second','topics':['category-ai','category-web'],'description':'New repository'}]),encoding='utf-8')
            result=subprocess.run(command,check=True,capture_output=True,text=True)
            updated=(root/'README.md').read_text(encoding='utf-8')
            self.assertIn('Collected 2 public repositories',result.stdout)
            self.assertEqual(updated.count('**[Second]'),2)
            self.assertIn('AI & Vision',updated)
            self.assertIn('Web & Apps',updated)
            self.assertIn('LonzilFox / Tiasmi',updated)
            subprocess.run(command,check=True,capture_output=True,text=True)
            self.assertEqual(updated,(root/'README.md').read_text(encoding='utf-8'))
            fixture.write_text(json.dumps([{'name':'First','topics':['category-tools']}, {'name':'Second','topics':['category-game']}]), encoding='utf-8')
            subprocess.run(command,check=True,capture_output=True,text=True)
            modified=(root/'README.md').read_text(encoding='utf-8')
            self.assertEqual(modified.count('**[Second]'),1)
            self.assertIn('Games & Mods',modified)
            self.assertNotIn('AI & Vision',modified)
    def test_schedule_is_quarter_hour_and_manual_trigger_exists(self):
        content=WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('workflow_dispatch:',content)
        self.assertIn("'7,22,37,52 * * * *'",content)
        self.assertIn('contents: write',content)
        self.assertIn('git push origin',content)

if __name__ == '__main__': unittest.main()
