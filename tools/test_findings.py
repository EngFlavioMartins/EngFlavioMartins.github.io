"""Regression checks for the requested unified findings section."""
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '5006ea53fb5a589b77347d386fd563382ea464a0'


class FindingsTests(unittest.TestCase):
    def test_all_publication_and_code_links_survive(self):
        before = subprocess.check_output(['git', 'show', f'{BASELINE}:index.html'], cwd=ROOT).decode()
        after = (ROOT / 'index.html').read_text()
        def references(html):
            return re.findall(r'href="(https://(?:doi.org|arxiv.org|github.com/EngFlavioMartins/)[^"]+)"', html)
        self.assertCountEqual(references(before), references(after))

    def test_consolidated_cards_and_question_titles(self):
        html = (ROOT / 'index.html').read_text()
        headings = re.findall(r'<h3>(.*?)</h3>', html)
        self.assertEqual(len(headings), 13)
        self.assertTrue(all(title.endswith('?') for title in headings))
        cards = re.findall(r'<article\b.*?</article>', html, re.S)
        for repository, paper in [
            ('openfoam-actuator-surface', '10.5194/wes-10-41-2025'),
            ('voronoi-coherent-structures', '2103.09884'),
            ('celestial-dynamics', '10.1590/1806-9126-rbef-2017-0174'),
        ]:
            matches = [c for c in cards if 'github.com/EngFlavioMartins/'+repository in c]
            self.assertEqual(len(matches), 1)
            self.assertIn(paper, matches[0])
        flow = next(c for c in cards if 'github.com/EngFlavioMartins/voronoi-coherent-structures' in c)
        self.assertIn('10.1007/s00348-021-03135-5', flow)
        self.assertIn('Two studies', flow)
        self.assertIn('voronoi-neighbours.svg', flow)
        self.assertNotIn('sparse-lagrangian-tracks.svg', html)
        self.assertIn('id="voronoi-coherence"', html)
        self.assertIn('id="openfoam-actuator-surface"', html)

    def test_one_visible_grid(self):
        html = (ROOT / 'index.html').read_text()
        self.assertEqual(html.count('class="research-stories"'), 1)
        self.assertEqual(html.count('class="research-story"'), 13)
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
