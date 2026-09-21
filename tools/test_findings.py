"""Regression checks for the requested unified findings section."""
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '5006ea53fb5a589b77347d386fd563382ea464a0'


class FindingsTests(unittest.TestCase):
    def test_all_studies_and_summaries_survive(self):
        before = subprocess.check_output(['git', 'show', f'{BASELINE}:index.html'], cwd=ROOT).decode()
        after = (ROOT / 'index.html').read_text()
        def summaries(html):
            return re.findall(r'<h3>.*?</h3>\s*<p>.*?</p>', html, re.S)
        self.assertEqual(len(summaries(after)), 15)
        self.assertCountEqual(summaries(before), summaries(after))

    def test_one_visible_grid(self):
        html = (ROOT / 'index.html').read_text()
        self.assertEqual(html.count('class="research-stories"'), 1)
        self.assertEqual(html.count('class="research-story"'), 15)
        self.assertIn('>Research findings</h2>', html)
        for obsolete in ['role="tab', ' hidden', 'Additional studies', 'Research summaries', 'featured-work.js']:
            self.assertNotIn(obsolete, html)

    def test_new_art_is_vector(self):
        for name in ['regenerative-wakes', 'wake-validation', 'vertical-momentum',
                     'cylinder-wake', 'truss-sizing', 'sparse-lagrangian-tracks']:
            root = ET.parse(ROOT / 'assets/work' / f'{name}.svg').getroot()
            self.assertTrue(root.tag.endswith('svg'))
            self.assertFalse(root.findall('.//{http://www.w3.org/2000/svg}image'))

    def test_main_palette_contrast(self):
        def luminance(colour):
            c = [int(colour[i:i+2], 16)/255 for i in (1,3,5)]
            c = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in c]
            return sum(a*b for a,b in zip(c,[.2126,.7152,.0722]))
        for ink in ['#182e32', '#526568', '#256d66', '#376c67']:
            self.assertGreater((luminance('#f8f9f5')+.05)/(luminance(ink)+.05), 4.5)


if __name__ == '__main__':
    unittest.main()
