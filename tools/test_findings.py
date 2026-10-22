"""Regression checks for the requested unified findings section."""
import re
import subprocess
from collections import Counter
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
        # Links may be added. Papers whose homepage post was removed (no public code) must still be
        # listed on the publications page.
        missing = Counter(references(before)) - Counter(references(after))
        publications = (ROOT / 'assets/publications.js').read_text()  # the publications page renders this list
        lost = [link for link in missing
                if re.sub(r'^https://(doi.org/|arxiv.org/abs/)', '', link) not in publications]
        self.assertFalse(lost, f'links removed: {sorted(lost)}')

    def test_consolidated_cards_and_question_titles(self):
        html = (ROOT / 'index.html').read_text()
        headings = re.findall(r'<h3>(.*?)</h3>', html)
        self.assertEqual(len(headings), 11)
        statements = {'Lid-driven cavity flow', 'From OpenFOAM fields to Python arrays',  # software cards
                      'Lifting-line model of a wind-turbine rotor', 'Vortex wakes of pitching and plunging airfoils'}
        self.assertTrue(all(title.endswith('?') or title in statements for title in headings))
        self.assertTrue(statements.issubset(headings))
        cards = re.findall(r'<article\b.*?</article>', html, re.S)
        # Every post links its repository; posts without public code are not shown.
        for card in cards:
            self.assertIn('https://github.com/EngFlavioMartins/', card)
        for repository, paper in [
            ('openfoam-actuator-surface', '10.5194/wes-10-41-2025'),
            ('voronoi-coherent-structures', '2103.09884'),
            ('celestial-dynamics', '10.1590/1806-9126-rbef-2017-0174'),
            ('coherent-structure-colouring', '10.1007/s00348-021-03135-5'),
            ('vortex-induced-vibration', '10.1016/j.ijmecsci.2019.03.024'),
            ('vortex-induced-vibration', '10.1016/j.marstruc.2019.01.005'),
            ('truss-sizing-optimisation', '10.1007/s13296-018-0194-8'),
            ('openfoam-postprocessing', '10.5194/wes-10-41-2025'),
        ]:
            matches = [c for c in cards if 'github.com/EngFlavioMartins/'+repository+'"' in c]
            self.assertEqual(len(matches), 1, repository)
            self.assertIn(paper, matches[0])
        voronoi = next(c for c in cards if 'github.com/EngFlavioMartins/voronoi-coherent-structures' in c)
        self.assertIn('renders/voronoi-coherence.webp', voronoi)
        csc = next(c for c in cards if 'github.com/EngFlavioMartins/coherent-structure-colouring' in c)
        self.assertIn('renders/coherent-structure-colouring.webp', csc)
        self.assertNotIn('sparse-lagrangian-tracks.svg', html)
        self.assertIn('id="voronoi-coherence"', html)
        self.assertIn('id="openfoam-actuator-surface"', html)

    def test_one_visible_grid(self):
        html = (ROOT / 'index.html').read_text()
        self.assertEqual(html.count('class="research-stories"'), 1)
        self.assertEqual(html.count('class="research-story"'), 11)
        self.assertIn('>Research and code</h2>', html)
        for obsolete in ['role="tab', ' hidden', 'Additional studies', 'Research summaries', 'featured-work.js']:
            self.assertNotIn(obsolete, html)

    def test_research_field_tags(self):
        html = (ROOT / 'index.html').read_text()
        cards = re.findall(r'<article\b.*?</article>', html, re.S)
        vocabulary = {'CFD', 'Numerical methods', 'Scientific computing', 'Fluid mechanics',
                      'Fluid–structure interaction', 'Structural mechanics', 'Optimisation',
                      'Dynamical systems', 'Flow diagnostics', 'Wind energy', 'Aerodynamics',
                      'Flow control', 'Atmospheric flows', 'Vortex methods', 'Classical mechanics',
                      'Celestial mechanics', 'Turbulence'}
        for card in cards:
            groups = re.findall(r'<ul class="research-tags" aria-label="Research fields" role="list">(.*?)</ul>', card, re.S)
            self.assertEqual(len(groups), 1)
            tags = re.findall(r'<li>(.*?)</li>', groups[0])
            self.assertGreaterEqual(len(tags), 2)
            self.assertLessEqual(len(tags), 4)
            self.assertEqual(len(tags), len(set(tags)))
            self.assertTrue(set(tags).issubset(vocabulary))
            self.assertNotIn('<a', groups[0])  # labels, not nonfunctional filters

    def test_new_art_is_vector(self):
        for name in ['regenerative-wakes', 'wake-validation', 'vertical-momentum',
                     'cylinder-wake', 'truss-sizing', 'sparse-lagrangian-tracks', 'hybrid-vortex-grid']:
            root = ET.parse(ROOT / 'assets/work' / f'{name}.svg').getroot()
            self.assertTrue(root.tag.endswith('svg'))
            self.assertFalse(root.findall('.//{http://www.w3.org/2000/svg}image'))

    def test_painted_masthead_then_light_research_section(self):
        html = (ROOT / 'index.html').read_text()
        band = html[html.index('<div class="hero-band">'):html.index('<main id="main">')]
        # Navigation and masthead share the darkened painting; the light research section follows.
        self.assertIn('class="site-header"', band)
        self.assertIn('class="masthead shell"', band)
        self.assertIn('class="hero-credit', band)          # the painting is credited
        self.assertIn('commons.wikimedia.org', band)
        self.assertIn('class="research-findings section-light"', html)
        self.assertNotIn('flow-divider', html)
        self.assertEqual(html.count('<h1>'), 1)
        css = (ROOT / 'assets/styles.css').read_text()
        self.assertIn('.hero-band::before', css)
        self.assertTrue((ROOT / 'assets/hero/facchinetti-lagoa-2400.webp').exists())
        self.assertNotIn('environmental-flow.svg', css)
        for page in ['index.html', 'cv/index.html', 'publications/index.html', 'projects/index.html']:
            self.assertIn('href="/assets/logo.svg"', (ROOT / page).read_text())

    def test_main_palette_contrast(self):
        def luminance(colour):
            c = [int(colour[i:i+2], 16)/255 for i in (1,3,5)]
            c = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in c]
            return sum(a*b for a,b in zip(c,[.2126,.7152,.0722]))
        css = (ROOT / 'assets/styles.css').read_text()
        token = lambda name: re.search(rf'--{name}: (#[0-9a-f]{{6}})', css)[1]  # noqa: E731
        ratio = lambda a, b: (max(luminance(a), luminance(b)) + .05) / (min(luminance(a), luminance(b)) + .05)  # noqa: E731
        for ink in ['ink', 'ink-soft', 'muted', 'violet']:
            self.assertGreater(ratio(token('paper'), token(ink)), 4.5, ink)
        for ink in ['dark-ink', 'dark-muted', 'dark-accent']:
            self.assertGreater(ratio(token('dark-card'), token(ink)), 4.5, ink)


if __name__ == '__main__':
    unittest.main()
