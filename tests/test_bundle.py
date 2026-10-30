import ast
import csv
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class BundleTests(unittest.TestCase):
    def test_app_syntax_and_encoding(self):
        source = (ROOT / 'app.py').read_text(encoding='utf-8')
        ast.parse(source)
        self.assertIn('encoding="utf-8-sig"', source)
        self.assertNotIn('reports.split(marker)[1]', source)

    def test_metrics_and_reports(self):
        with (ROOT/'data/model_summary.csv').open(encoding='utf-8', newline='') as f:
            summary = list(csv.DictReader(f))
        with (ROOT/'data/fold_results.csv').open(encoding='utf-8', newline='') as f:
            folds = list(csv.DictReader(f))
        self.assertEqual(len(summary), 4)
        self.assertEqual(len(folds), 48)
        reports = (ROOT/'data/reports.txt').read_text(encoding='utf-8-sig')
        for row in summary:
            name = row['Model']
            self.assertIn(name + ' — pooled out-of-fold classification report', reports)
            self.assertEqual({int(r['Fold']) for r in folds if r['Model']==name}, set(range(1,13)))
            for key, value in row.items():
                if key != 'Model': self.assertTrue(0 <= float(value) <= 1)

    def test_notebook_fingerprint(self):
        meta=json.loads((ROOT/'data/provenance.json').read_text(encoding='utf-8'))
        content=(ROOT/'finished_assignment_corrected.ipynb').read_bytes()
        self.assertEqual(hashlib.sha256(content).hexdigest(), meta['notebook_sha256'])
        nb=json.loads(content)
        self.assertFalse(any(o.get('output_type')=='error' for c in nb['cells'] for o in c.get('outputs',[])))

if __name__ == '__main__': unittest.main()
