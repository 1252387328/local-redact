import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(project):
    spec = importlib.util.spec_from_file_location(project.replace('-', '_'), ROOT / 'cli.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProjectTests(unittest.TestCase):
    def test_all_help_and_invalid_arguments(self):
        for path in [ROOT / 'cli.py']:
            with self.subTest(project=path.parent.name):
                result = subprocess.run([sys.executable, str(path), '--help'], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                result = subprocess.run([sys.executable, str(path), '--not-a-real-option'], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn('Traceback', result.stderr)

    def test_redact_patterns(self):
        module = load('local-redact')
        source = 'demo@example.com 13800138000 +1 415-555-0123 ghp_' + 'x' * 30 + ' PROJECT-Z'
        result, counts = module.redact(source, ['PROJECT-Z'])
        self.assertNotIn('example.com', result)
        self.assertNotIn('13800138000', result)
        self.assertNotIn('415-555', result)
        self.assertNotIn('ghp_', result)
        self.assertNotIn('PROJECT-Z', result)
        self.assertEqual(counts['PHONE'], 2)

    def test_redact_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'existing.txt'
            output.write_text('keep')
            result = subprocess.run([sys.executable, str(ROOT / 'cli.py'), str(ROOT / 'examples/contact.txt'), '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_text(), 'keep')

if __name__ == '__main__':
    unittest.main()
