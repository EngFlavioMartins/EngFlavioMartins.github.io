"""Build the shared header and footer into every page, and write the publications and CV pages.

Run from anywhere:  python3 tools/build_pages.py
- Every page gets the same painted header band (navigation plus that page's intro) and the same
  painted footer, between <!-- site:header --> / <!-- /site:header --> and <!-- site:footer --> /
  <!-- /site:footer --> markers. The homepage keeps its own masthead and research posts.
- publications/index.html and cv/index.html are written in full from the data below
  (sources: the academic CV, Academic_CV_2026.tex, and the professional CV, Flavio_Martins_CV.tex).
"""
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAIL = "f.m.martins@tudelft.nl"
GH = "https://github.com/EngFlavioMartins/"
STYLE = "/assets/styles.css?v=20261025"
PROFILES = [("GitHub", "https://github.com/EngFlavioMartins"),
            ("Google Scholar", "https://scholar.google.com/citations?user=WZXamCcAAAAJ&hl=en"),
            ("ORCID", "https://orcid.org/0000-0002-1374-5760"),
            ("LinkedIn", "https://www.linkedin.com/in/flavio-martins-8bb89772")]
PAINTING = ('Painting: Nicola Facchinetti, <i>Lagoa Rodrigo de Freitas, Rio de Janeiro</i>, c. 1884 · public domain, '
            '<a href="https://commons.wikimedia.org/wiki/File:Nicola_Facchinetti_-_Lagoa_Rodrigo_de_Freitas,_Rio_de_Janeiro,_ca._1884.jpg" '
            'rel="noreferrer">Wikimedia Commons</a>')


def a(text, url):
    rel = "" if url.startswith(("/", "mailto:")) else ' rel="noreferrer"'
    return f'<a href="{escape(url)}"{rel}>{text}</a>'


# ---------------------------------------------------------------- shared header and footer
def site_header(current, intro=""):
    here = ' aria-current="page"'
    nav = "".join(f'<a href="{href}"{here if key == current else ""}>{label}</a>'
                  for key, href, label in [("cv", "/cv/", "CV"), ("publications", "/publications/", "Publications")])
    return f"""    <!-- site:header -->
    <div class="hero-band">
      <header class="site-header">
        <a class="wordmark" href="/" aria-label="Flavio Martins, home"><img class="wordmark-mark" src="/assets/logo.svg" width="40" height="40" alt="FM logo" /><span>Flavio Martins</span></a>
        <nav class="site-nav" aria-label="Primary navigation">{nav}</nav>
      </header>
{intro}    </div>
    <!-- /site:header -->"""


def page_intro(title, lede, actions):
    def attrs(u):
        return " download" if u.endswith(".pdf") else (' rel="noreferrer"' if u.startswith("http") else "")
    buttons = "".join(f'<a class="button {"button-primary" if i == 0 else "button-ghost"}" href="{escape(u)}"{attrs(u)}>{t}</a>'
                      for i, (t, u) in enumerate(actions))
    return f"""      <section class="page-intro shell">
        <div>
          <h1>{title}</h1>
          <p class="page-lede">{lede}</p>
        </div>
        <div class="page-actions">{buttons}</div>
      </section>
"""


def site_footer():
    links = "".join(f"<li>{a(t, u)}</li>" for t, u in PROFILES)
    return f"""<!-- site:footer -->
    <footer class="site-footer">
      <div class="shell footer-inner">
        <div class="footer-id">
          <img src="/assets/logo.svg" width="36" height="36" alt="FM logo" />
          <div><p class="footer-name">Flavio A. C. Martins</p><p>PhD candidate · Wind Energy, TU Delft</p></div>
        </div>
        <ul class="footer-links" role="list">{links}<li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
      </div>
      <p class="shell footer-credit">{PAINTING}</p>
    </footer>
    <!-- /site:footer -->"""


def head(title, description, extra=""):
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="{description}" />
    <meta name="theme-color" content="#0b0e10" />
    <title>{title}</title>
    <link rel="icon" type="image/svg+xml" href="/assets/logo.svg" />
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png" />
    <link rel="apple-touch-icon" href="/assets/logo-180.png" />
    <link rel="stylesheet" href="{STYLE}" />
    <script src="/assets/site.js" defer></script>{extra}
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
"""


# ---------------------------------------------------------------- publications
TYPES = [("journal", "Journal articles"), ("preprint", "Preprints"),
         ("conference", "Conference papers and talks"), ("report", "Technical and academic reports")]
R = "/assets/work/thumbs/"
PUBLICATIONS = [
    dict(type="journal", year=2026, status="Accepted", title="OpenONDA: A Python Interface for In-Line Control of OpenFOAM Solvers",
         authors="Flavio A. C. Martins", venue="OpenFOAM Journal", url=GH + "OpenONDA", code=GH + "OpenONDA", tile=R + "openonda.webp"),
    dict(type="journal", year=2025, title="Proof of Concept for Multirotor Systems with Vortex-Generating Modes for Regenerative Wind Energy: A Study Based on Numerical Simulations and Experimental Data",
         authors="Flavio A. C. Martins, A. van Zuijlen, C. S. Ferreira", venue="Wind Energy Science, 10, 41–58", doi="10.5194/wes-10-41-2025",
         code=GH + "openfoam-actuator-surface", tile=R + "regenerative-wakes.webp"),
    dict(type="journal", year=2021, title="Detection of Vortical Structures in Sparse Lagrangian Data Using Coherent-Structure Colouring",
         authors="Flavio A. C. Martins, A. Sciacchitano, D. E. Rival", venue="Experiments in Fluids, 62(4), 69", doi="10.1007/s00348-021-03135-5",
         code=GH + "coherent-structure-colouring", tile=R + "coherent-structure-colouring.webp"),
    dict(type="journal", year=2019, title="A Linear Approach for Sizing Optimization of Isostatic Trussed Structures Subjected to External and Self-Weight Loads",
         authors="Flavio A. C. Martins, J. P. J. Avila, M. A. da Silva", venue="International Journal of Steel Structures, 19(4), 1146–1157",
         doi="10.1007/s13296-018-0194-8", code=GH + "truss-sizing-optimisation", tile=R + "truss-sizing.webp"),
    dict(type="journal", year=2019, title="Effects of the Reynolds Number and Structural Damping on Vortex-Induced Vibrations of an Elastically-Mounted Rigid Cylinder",
         authors="Flavio A. C. Martins, J. P. J. Avila", venue="International Journal of Mechanical Sciences, 156, 235–249",
         doi="10.1016/j.ijmecsci.2019.03.024", code=GH + "vortex-induced-vibration", tile=R + "vortex-induced-vibration.webp"),
    dict(type="journal", year=2019, title="Three-Dimensional CFD Analysis of Damping Effects on Vortex-Induced Vibrations of 2DOF Elastically-Mounted Circular Cylinders",
         authors="Flavio A. C. Martins, J. P. J. Avila", venue="Marine Structures, 65, 12–31", doi="10.1016/j.marstruc.2019.01.005",
         code=GH + "vortex-induced-vibration", tile=R + "viv-3d.webp"),
    dict(type="journal", year=2018, title="Mecânica Celeste e a Teoria dos Sistemas Dinâmicos: Uma Revisão do Problema Circular Restrito de Três Corpos",
         authors="Flavio A. C. Martins, M. Zanotello", venue="Revista Brasileira de Ensino de Física, 40(2), e2310",
         doi="10.1590/1806-9126-rbef-2017-0174", code=GH + "celestial-dynamics", tile=R + "three-body.webp"),
    dict(type="preprint", year=2026, title="Toward Meshless Turbulent Flow Simulation: LES-Integrated Vortex Particle Method",
         authors="Flavio A. C. Martins, A. van Zuijlen, C. S. Ferreira", venue="arXiv:2601.06942", url="https://arxiv.org/abs/2601.06942",
         tile=R + "vortex-leapfrog.webp"),
    dict(type="preprint", year=2021, title="A Voronoi-Tessellation-Based Approach for Detection of Coherent Structures in Sparsely-Seeded Flows",
         authors="Flavio A. C. Martins, D. E. Rival", venue="arXiv:2103.09884", url="https://arxiv.org/abs/2103.09884",
         code=GH + "voronoi-coherent-structures", tile=R + "voronoi-coherence.webp"),
    dict(type="conference", year=2026, title="Toward a 3D Hybrid Vortex Particle–Grid Approach for External Flows",
         authors="Flavio A. C. Martins, A. van Zuijlen, D. A. von Terzi", venue="Journal of Physics: Conference Series, 3224(4), 042069",
         doi="10.1088/1742-6596/3224/4/042069", tile=R + "hybrid-grid.webp"),
    dict(type="conference", year=2024, title="Numerical Investigation of Atmospheric Boundary Layer Control in Wind Farms with Multirotor Systems",
         authors="Flavio A. C. Martins, C. S. Ferreira, A. van Zuijlen", venue="Journal of Physics: Conference Series, 2767(7), 072006",
         doi="10.1088/1742-6596/2767/7/072006", tile=R + "wind-farm.webp"),
    dict(type="conference", year=2024, title="Enhancing Wind Farm Efficiency Through Active Control of the Atmospheric Boundary Layer’s Vertical Entrainment of Momentum",
         authors="C. S. Ferreira, D. Bensason, T. J. Broertjes, A. Sciacchitano, Flavio A. C. Martins, A. G. Ajay",
         venue="Journal of Physics: Conference Series, 2767(9), 092107", doi="10.1088/1742-6596/2767/9/092107",
         tile=R + "entrainment.webp"),
    dict(type="conference", year=2022, title="State-Observer-Based Data Assimilation for Real Flow Analysis: Integrating Computation and Measurement",
         authors="Flavio A. C. Martins, A. Alcântara, D. E. Rival", venue="NATO Unclassified technical meeting, Kingston, Canada", tile=R + "assimilation.webp"),
    dict(type="conference", year=2018, title="Three-Dimensional CFD Analysis of Damping Effects on Vortex-Induced Vibrations of 2DOF Cylinders",
         authors="Flavio A. C. Martins, J. P. J. Avila", venue="SIIC-USP, São Paulo, Brazil",
         url="https://uspdigital.usp.br/siicusp/siicPublicacao.jsp?codmnu=7210", tile=R + "viv-2dof.webp"),
    dict(type="conference", year=2018, title="Detection of Damage in Aerospace Structures Using Optimization Techniques on Impact Tests Results",
         authors="Flavio A. C. Martins, M. A. da Silva, R. M. L. R. F. Brasil",
         venue="Proceeding Series of the Brazilian Society of Computational and Applied Mathematics (CNMAC)",
         url="https://proceedings.sbmac.org.br/sbmac/article/download/1878/1896", tile=R + "plate-mode.webp"),
    dict(type="conference", year=2017, title="Topology Optimization of 2D Trussed Structures", authors="Flavio A. C. Martins, M. A. da Silva, R. M. L. R. F. Brasil",
         venue="CILAMCE, São José dos Campos, Brazil", doi="10.20906/cps/cilamce2017-0035", tile=R + "truss-topology.webp"),
    dict(type="conference", year=2017, title="Analysis of the Dynamic Response of the Internal Structure of the ONERA M6 Wing",
         authors="Flavio A. C. Martins, M. A. da Silva", venue="IX Workshop in Dynamic Systems, São Paulo, Brazil", tile=R + "onera-m6.webp"),
    dict(type="conference", year=2017, title="Identification of Damage in Aerospace Structures Using Optimization Techniques and Impact Tests",
         authors="Flavio A. C. Martins, M. A. da Silva", venue="ASCE Engineering Mechanics Institute Conference, Rio de Janeiro, Brazil", tile=R + "beam-mode.webp"),
    dict(type="report", year=2022, title="Calibration of Menter’s RANS γ-Model for Transonic, Transitional Flows",
         authors="Flavio A. C. Martins et al.", venue="RivalLab / Pratt & Whitney Canada (NDA-protected)", tile=R + "transition.webp"),
    dict(type="report", year=2018, title="Optimization of the Internal Structure of Statically and Dynamically Loaded Wings",
         authors="Flavio A. C. Martins, M. A. da Silva", venue="UFABC research report (CNPq-funded)",
         url="https://propes.ufabc.edu.br/simposios/index.php?conference=EIC&schedConf=8EIC2018&page=paper&op=view&path%5B%5D=3344", tile=R + "wing-ribs.webp"),
    dict(type="report", year=2017, title="Applications of Dynamical Systems Theory to Biological and Chemical Problems",
         authors="Flavio A. C. Martins, M. Zanotello", venue="UFABC research report (CNPq-funded)",
         url="https://propes.ufabc.edu.br/simposios/index.php?conference=EIC&schedConf=7EIC2017&page=paper&op=view&path%5B%5D=2966", tile=R + "brusselator.webp"),
    dict(type="report", year=2016, title="Celestial Mechanics and the Theory of Dynamic Systems: A Revision of the Circular Restricted Three-Body Problem",
         authors="Flavio A. C. Martins, M. Zanotello", venue="UFABC research report (CNPq-funded)",
         url="https://propes.ufabc.edu.br/simposios/index.php?conference=EIC&schedConf=6EIC2016&page=paper&op=view&path%5B%5D=2502",
         tile=R + "poincare.webp"),
]


TILE_ALT = {
    "openonda.webp": "Hybrid finite-volume and vortex-particle wake simulation around a cube",
    "regenerative-wakes.webp": "Wake of a rotor with four wing strips: velocity-deficit planes and streamlines",
    "coherent-structure-colouring.webp": "Measured particle tracks behind an Ahmed body coloured by coherent-structure colouring",
    "truss-sizing.webp": "The sized 37-member truss coloured by stress over admissible stress",
    "vortex-induced-vibration.webp": "Vortex cores shed behind an elastically mounted cylinder",
    "viv-3d.webp": "Vortex street behind an elastically mounted cylinder, one phase of its oscillation",
    "viv-2dof.webp": "Vortex street behind an elastically mounted cylinder, another phase of its oscillation",
    "three-body.webp": "Earth–Moon effective-potential landscape with an orbit",
    "poincare.webp": "Poincaré section of Earth–Moon orbits in the restricted three-body problem",
    "voronoi-coherence.webp": "Voronoi cells of double-gyre tracers coloured by coherence",
    "vortex-leapfrog.webp": "Paths of two vortex pairs leapfrogging, from point-vortex dynamics",
    "hybrid-grid.webp": "Illustration: a near-body grid around a square body and a particle wake",
    "wind-farm.webp": "Illustration: wake deficits behind a farm of multirotor systems, top view",
    "entrainment.webp": "Illustration: turbine wakes in a boundary layer, with streamlines bending down into them",
    "assimilation.webp": "Illustration: a vortex field with sparse sensor positions",
    "plate-mode.webp": "Illustration: a plate mode shape distorted by a damaged region",
    "truss-topology.webp": "A cantilever truss coloured by member axial force from a static solve",
    "onera-m6.webp": "ONERA M6 wing planform with spars and ribs, shaded by its first bending mode",
    "beam-mode.webp": "Illustration: cantilever mode shapes and the shape with a crack",
    "transition.webp": "Illustration: intermittency growing through a transitional boundary layer",
    "wing-ribs.webp": "ONERA M6 wing planform with ribs of varying size",
    "brusselator.webp": "Trajectories of the Brusselator converging to its limit cycle",
}


def authors_html(text):
    return re.sub(r"(Flavio A\. C\. Martins)", r"<strong>\1</strong>", escape(text))


def publication(p):
    url = p.get("url") or (f"https://doi.org/{p['doi']}" if p.get("doi") else None)
    title = a(escape(p["title"]), url) if url else escape(p["title"])
    kind = dict(TYPES)[p["type"]].rstrip("s").replace("Conference papers and talk", "Conference paper").replace(
        "Technical and academic report", "Report")
    label = f"{p['year']} · {kind}" + (f" · {p['status']}" if p.get("status") else "")
    meta = escape(p["venue"]) + (f" · DOI {p['doi']}" if p.get("doi") else "")
    links = []
    if url:
        links.append(a("Paper ↗" if p["type"] != "report" else "Read ↗", url))
    if p.get("code"):
        links.append(a("Code ↗", p["code"]))
    tile = f'<img class="pub-tile" src="{p["tile"]}?v=2" width="160" height="100" loading="lazy" alt="{TILE_ALT[p["tile"].rsplit("/", 1)[1]]}" />'
    return f"""          <li class="pub">
            {tile}
            <div class="pub-body">
              <p class="pub-label">{label}</p>
              <h3>{title}</h3>
              <p class="pub-authors">{authors_html(p["authors"])}</p>
              <p class="pub-meta">{meta}</p>
              {'<p class="pub-links">' + "".join(links) + "</p>" if links else ""}
            </div>
          </li>
"""


def publications_page():
    groups = []
    chips = []
    for key, name in TYPES:
        items = sorted((p for p in PUBLICATIONS if p["type"] == key), key=lambda p: -p["year"])
        chips.append(f'<a href="#{key}">{name} <span>{len(items)}</span></a>')
        groups.append(f"""      <section class="pub-group" id="{key}" aria-labelledby="{key}-heading">
        <h2 id="{key}-heading">{name} <span>{len(items)}</span></h2>
        <ol class="pub-list" role="list">
{"".join(publication(p) for p in items)}        </ol>
      </section>
""")
    intro = page_intro("Publications", f"{len(PUBLICATIONS)} publications: journal articles, preprints, conference papers and reports, newest first in each group.",
                       [("Google Scholar ↗", PROFILES[1][1]), ("ORCID ↗", PROFILES[2][1])])
    return (head("Publications · Flavio A. C. Martins",
                 "Journal articles, preprints, conference papers and reports by Flavio A. C. Martins.")
            + site_header("publications", intro) + f"""

    <main id="main" class="page-light">
      <nav class="pub-toc shell" aria-label="Publication types">{"".join(chips)}</nav>
      <div class="pub-shell shell">
{"".join(groups)}      </div>
    </main>

    {site_footer()}
  </body>
</html>
""")


# ---------------------------------------------------------------- CV
def item(date, title, place, lines=(), extra=""):
    bullets = "".join(f"<li>{x}</li>" for x in lines)
    return f"""              <article class="cv-item">
                <p class="cv-date">{date}</p>
                <div>
                  <h4>{title}</h4>
                  <p class="cv-place">{place}</p>{extra}
                  {f'<ul>{bullets}</ul>' if bullets else ''}
                </div>
              </article>
"""


def section(title, body, sid=None):
    return f"""            <section class="cv-section"{f' id="{sid}"' if sid else ''}>
              <h3>{title}</h3>
{body}            </section>
"""


LANG_SHORT = '              <p class="cv-plain">Portuguese (native) · English (C2) · Dutch (B1)</p>\n'
LANG_LONG = '              <p class="cv-plain">Portuguese (native) · English (fluent, C2) · Dutch (intermediate, B1)</p>\n'


def numbered(entries):
    return '              <ol class="cv-list">' + "".join(f"<li>{e}</li>" for e in entries) + "</ol>\n"


EDUCATION = [
    ("2023 – present", "PhD in Aerospace Engineering (in progress)", "TU Delft, Delft, the Netherlands",
     ["Thesis: 3D unsteady CFD model for multi-rotor body fluid–structure interaction.",
      "Promotor: Prof. Dr. ir. Carlos Simão Ferreira · Supervisor: Dr. Alexander van Zuijlen."]),
    ("2019 – 2021", "MASc in Mechanical &amp; Materials Engineering · GPA 4.2/4.3", "Queen’s University, Kingston, Canada",
     ["Thesis: Detecting Lagrangian coherent structures in realistic experimental fluid-flow data sets "
      "(" + a("read online", "https://qspace.library.queensu.ca/handle/1974/28695") + ").",
      "Supervisor: Dr. David E. Rival."]),
    ("2016 – 2018", "BSc in Aerospace Engineering (honours, valedictorian) · GPA 3.7/4.0", "Federal University of ABC (UFABC), Santo André, Brazil",
     ["Thesis: Vibration analysis and FSI effects of two-dimensional aeroelastic aeronautical structures.",
      "Supervisor: Dr. Marcelo S. Araujo."]),
    ("2012 – 2016", "BSc in Science &amp; Technology (honours) · GPA 3.6/4.0", "Federal University of ABC (UFABC), Santo André, Brazil", []),
]


def cv_page():
    # ---- professional (concise)
    prof_experience = "".join([
        item("2023 – present", "PhD candidate · computational aerodynamics", "TU Delft, Wind Energy section",
             ["Designed and built OpenONDA, an open-source Python/C++ framework coupling a GPU-accelerated vortex-particle solver with OpenFOAM; accepted in the OpenFOAM Journal (2026).",
              "Added large-eddy simulation to the particle solver and applied it to multirotor wind turbines and wind-farm momentum entrainment; published in Wind Energy Science (2025).",
              "Co-supervised an MSc thesis (GPU fast multipole method); supervise BSc project teams."]),
        item("2021 – 2022", "Research engineer", "RivalLab, Queen’s University · project with Pratt &amp; Whitney Canada",
             ["Calibrated a transition-sensitive RANS model (k–ω–γ) against experiments for transonic turbine flows; delivered an NDA-protected report.",
              "Designed and built towing-tank rigs with actuation and instrumentation; acquired and processed PIV/PTV and force data."]),
        item("2019 – 2021", "Graduate researcher (MASc) · fluid dynamics", "Queen’s University, Kingston, Canada",
             ["Developed graph-based methods to detect coherent structures in sparse particle-tracking data; published in Experiments in Fluids (2021).",
              "Evaluated a marine propulsion and energy-harvesting concept with CFD, towing-tank tests and force measurements."]),
        item("2018 – 2019", "Research associate · fluid–structure interaction", "Federal University of ABC, Santo André, Brazil",
             ["Modelled vortex-induced vibration of elastically mounted cylinders in 2D and 3D CFD, quantifying the effects of damping and Reynolds number; published in Marine Structures and the International Journal of Mechanical Sciences (2019)."]),
        item("2017 – 2018", "Mechanical engineering intern", "Civil Structural Engineering Ltd, São Paulo, Brazil",
             ["Supported civil and steel-structure projects: site visits, load estimation, CAD drawings, reports and client presentations.",
              "Developed a real-time data-acquisition system for vibration monitoring of machine foundations, with sensors and spectral analysis."]),
    ])
    skills = [("Programming", "Python · C++ · CUDA · MATLAB · Git · Linux · GPU computing"),
              ("CFD and numerical methods", "OpenFOAM · RANS · LES · finite-volume and vortex-particle methods · mesh generation · FSI"),
              ("Structures", "FEM/FEA · Abaqus · ANSYS · structural dynamics · SolidWorks · load estimation · optimisation"),
              ("Experiments and data", "PIV/PTV · data acquisition · wind tunnels and towing tanks · force and pressure measurements · signal and statistical analysis · model calibration · data assimilation")]
    skill_html = '              <dl class="cv-skills">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in skills) + "</dl>\n"
    prof_education = "".join(item(d, t, p) for d, t, p, _ in EDUCATION)
    prof_side = "".join([
        section("Leadership and community", numbered([
            "<strong>Chair, Aerospace Engineering PhD Council</strong>, TU Delft (2025–2026; member since 2023): redesigned the annual PhD symposium (nearly 200 attendees), cut its budget from EUR 20,000 to 5,000 and secured industry sponsorship.",
            "<strong>Member, University PhD Council</strong>, TU Delft (2026): university-wide events, budgets and stakeholder coordination.",
            "<strong>TU Delft representative, Dutch OpenFOAM user community</strong> (2023–2026): co-organised the national user meetings."])),
        section("Teaching and outreach", numbered([
            "Teaching assistant, experimental fluid-dynamics labs, Queen’s University (2019–2021); MATLAB and Abaqus workshops (2017–2018).",
            "OffshoreWind4Kids team leader (2024–2026); developed Wind for Kids teaching materials for primary schools (2024–2025)."])),
        section("Languages", LANG_SHORT),
    ])
    professional = f"""        <article id="panel-professional" class="cv-panel" role="tabpanel" aria-labelledby="tab-professional" data-cv-panel="professional">
          <p class="cv-summary">Computational engineer with over seven years of experience in CFD, fluid–structure interaction and scientific software for wind energy, marine and aerospace applications: from numerical method to validated result, with GPU-accelerated solvers (Python, C++, CUDA), coupling with OpenFOAM and validation against experiments.</p>
          <div class="cv-columns">
            <div>
{section("Experience", prof_experience)}{section("Education", prof_education)}            </div>
            <div>
{section("Technical skills", skill_html)}{prof_side}            </div>
          </div>
        </article>
"""
    # ---- academic (extensive)
    research = "".join([
        item("2023 – present", "PhD candidate", "TU Delft Wind Energy Institute · supervisors Prof. Dr. ir. C. Simão Ferreira and Dr. A. van Zuijlen",
             ["Developed a 3D hybrid CFD model for multi-rotor fluid–structure interaction, resolving wake–structure coupling in multi-rotor wind-energy systems.",
              "Investigated vortex-generating multirotor configurations for regenerative wind energy and their effect on atmospheric-boundary-layer entrainment in wind farms.",
              "Wrote a GPU-based particle solver with an integrated LES methodology for meshless turbulent-flow simulation of external flows."]),
        item("2019 – 2022", "MASc student and research engineer", "Queen’s University, Kingston, Canada · supervisor Dr. David E. Rival",
             ["Developed a graph-theory-based technique for detecting coherent motion in tracer data.",
              "Designed and benchmarked a hybrid propulsion and energy-harvesting system for marine applications using CFD.",
              "Ran towing-tank experiments on unsteady airfoil and delta-wing flows, collecting and analysing PIV, PTV and force data at high Reynolds numbers."]),
        item("2018 – 2019", "Research associate", "UFABC Fluid–Structure Interaction Lab, Santo André, Brazil · supervisor Dr. Juan Avila",
             ["Conducted 2D and 3D CFD studies of vortex-induced vibration of elastically mounted cylinders, with relevance to offshore riser dynamics.",
              "Investigated the influence of mechanical parameters and damping on the cylinder’s vibration response."]),
        item("2016 – 2018", "Undergraduate research fellow (CNPq)", "UFABC, Santo André, Brazil · supervisor Dr. Marcelo S. Araujo",
             ["Optimised the internal structure of statically and dynamically loaded wings."]),
        item("2015 – 2017", "Undergraduate research fellow (CNPq)", "UFABC, Santo André, Brazil · supervisor Prof. Dr. Marcelo Zanotello",
             ["Studied celestial mechanics through the circular restricted three-body problem.",
              "Applied dynamical-systems theory to biological and chemical problems."]),
    ])
    professional_exp = "".join([
        item("2021 – 2022", "Research engineer", "RivalLab, partnership with Pratt &amp; Whitney Canada, Kingston, Canada",
             ["Calibrated a transitional RANS turbulence model (k–ω–γ) against experimental data to improve aircraft-turbine simulations.",
              "Designed and built towing-tank set-ups for aerodynamic surface analysis, integrating actuation and measurement systems.",
              "Acquired and post-processed PIV and PTV data to characterise unsteady surface-flow fields."]),
        item("2017 – 2018", "Mechanical engineering intern", "Civil Structural Engineering Ltd, São Paulo, Brazil · manager Dr. Marcelo Araujo",
             ["Contributed to civil-engineering projects from client site visits and load estimation to structural modelling and reporting.",
              "Developed a real-time data-acquisition and spectral-analysis system for vibration measurements in machine foundations."]),
    ])
    academic_education = "".join(item(d, t, p, lines) for d, t, p, lines in EDUCATION)
    counts = {k: sum(p["type"] == k for p in PUBLICATIONS) for k, _ in TYPES}
    pubs_by_type = ""
    for key, name in TYPES:
        entries = [f'{authors_html(p["authors"])} ({p["year"]}). {a(escape(p["title"]), p.get("url") or ("https://doi.org/" + p["doi"] if p.get("doi") else "#")) if (p.get("url") or p.get("doi")) else escape(p["title"])}. <i>{escape(p["venue"])}</i>.'
                   for p in sorted((p for p in PUBLICATIONS if p["type"] == key), key=lambda p: -p["year"])]
        pubs_by_type += f'              <h4 class="cv-subhead">{name} ({counts[key]})</h4>' + "\n" + numbered(entries)
    teaching = "".join([
        item("2025 – 2026", "Project supervisor · Test, Analysis and Simulation", "TU Delft",
             ["Used student-led explanations and technical questioning to assess understanding of project methods, assumptions and results."]),
        item("2026", "MSc thesis co-supervisor", "TU Delft · with Dr. Alexander van Zuijlen",
             ["GPU-accelerated Cartesian fast multipole method for particle-based flow simulation (" +
              a("read online", "https://repository.tudelft.nl/record/uuid:f9db5fcd-e277-4e11-9b27-a3f2d2b2dc44") + ")."]),
        item("2019 – 2021", "Teaching assistant · experimental fluid dynamics", "Queen’s University, Kingston, Canada",
             ["Taught undergraduate laboratory sessions and supported courses on experimental fluid dynamics."]),
        item("2017 – 2018", "Lecturer, Workshop in Mechanical Engineering (WEM)", "UFABC, São Paulo, Brazil",
             ["Implementation of finite-element codes in MATLAB (2018).",
              "Introduction to structural analysis with the finite-element software Abaqus (2017 and 2018)."]),
    ])
    academic = f"""        <article id="panel-academic" class="cv-panel" role="tabpanel" aria-labelledby="tab-academic" data-cv-panel="academic" hidden>
          <p class="cv-summary">I study unsteady flows, turbulence and fluid–structure interaction, combining numerical methods with experimental flow measurements. My work spans wind-energy wakes, marine dynamics and coherent structures in particle-tracking data. I develop hybrid Eulerian–Lagrangian methods and scientific software to connect physical models with measurements across scales.</p>
          <div class="cv-single">
{section("Education", academic_education)}{section("Research experience", research)}{section("Professional experience", professional_exp)}{section("Open-source software", item("2023 – present", "OpenONDA · hybrid CFD framework", a("github.com/EngFlavioMartins/OpenONDA", GH + "OpenONDA"), ["Modular Python/C++ framework that unifies a GPU-accelerated vortex-particle method (Lagrangian) with a finite-volume method (Eulerian) and an OpenFOAM interface."]) + item("2018 – 2026", "Research codes", a("github.com/EngFlavioMartins", PROFILES[0][1]), ["Ten open repositories accompanying the papers: wake actuators in OpenFOAM, coherent-structure detection, vortex-induced vibration, truss sizing, three-body dynamics, lifting-line and vortex-panel solvers. See the " + a("homepage", "/") + "."]))}{section("Publications", pubs_by_type, "publications")}{section("Teaching and supervision", teaching)}{section("Honours and awards", numbered(["Institute of Engineering Award (2018), for ranking among the top three graduates of UFABC’s aerospace engineering programme.", "Second-highest GPA in the history of UFABC’s aerospace engineering programme, as of 2018."]))}{section("Academic leadership and service", numbered([
        "<strong>Chair, Aerospace Engineering PhD Council</strong>, TU Delft (member 2023–2024; chair 2025–2026). Redesigned the annual PhD symposium as a talk-show-format event with expert panels (nearly 200 attendees) while cutting its budget by about 75% (EUR 20k to 5k); secured industry funding for internal events; introduced council-rotation rules and PhD office hours.",
        "<strong>Member, TU Delft University PhD Council</strong> (2026). Designed and delivered university-wide events connecting PhD candidates across faculties: budgets, schedules, stakeholder coordination and fundraising.",
        "<strong>TU Delft representative, Dutch OpenFOAM User Community</strong> (2023–2026). Co-organised the national user meetings, curating tutorial content and recruiting speakers.",
        "<strong>Student journalist, DUWIND</strong>, WindEurope Annual Event 2025 (Copenhagen). Produced a specialist interview series (12 interviews, 4 reports) and joined a panel with a policymaker on engineering education and a unified European engineering CV.",
        "<strong>Q&amp;A volunteer, TU Delft Start-up Module A</strong> (2023). Supported incoming PhD candidates across nine editions of the course."]))}{section("Outreach and public engagement", numbered([
        "Volunteer instructor (2023) and team leader (2024–2026), " + a("OffshoreWind4Kids", "https://www.offshorewind4kids.com/") + ": wind-energy beach demonstrations with model turbines for children and parents.",
        "Educational materials developer, Wind for Kids (2024–2025): booklets, games and classroom activities for primary-school teachers, refined through trials with schoolchildren.",
        "Faculty open-day volunteer, TU Delft (2023–2025), for the Wind Energy section.",
        "Instructor volunteer, 015 Duurzaam programme, Delft public library (2023): water management and wind energy for children.",
        "Volunteer lecturer, UFABC VII Workshop on Mechanical and Marine Engineering (2018): mini-courses on finite-element structural analysis."]))}{section("Media and public visibility", numbered([
        "Panellist at three TU Delft events: the " + a("Safety Beyond Boundaries", "https://www.tudelft.nl/en/events/2024/lr/tu-delft-ae-diversity-inclusion-safety-beyond-boundaries-panel") + " D&amp;I panel on aerospace and LGBTIQ+ safety (2024), the AE D&amp;I Week panel representing visible minorities (2024), and TU Delft for Life, on the PhD as a career path.",
        "Interview in TU Delft Aerospace Engineering news on the Triangle Tuning programme (2024).",
        "Academic profile featured in the Institute of Engineering yearly magazine (2019)."]))}{section("Languages", LANG_LONG)}          </div>
        </article>
"""
    intro = page_intro("Curriculum vitae", "A two-page professional summary and the full academic record. Both are available as PDF.",
                       [("Professional PDF ↓", "/downloads/flavio-martins-professional-cv.pdf"),
                        ("Academic PDF ↓", "/downloads/flavio-martins-academic-cv.pdf")])
    return (head("CV · Flavio A. C. Martins",
                 "Professional and academic CV of Flavio A. C. Martins: CFD, fluid–structure interaction, wind energy and scientific software.",
                 '\n    <script src="/assets/cv-tabs.js" defer></script>\n    <noscript><style>.cv-panel[hidden]{display:block}.cv-tabs{display:none}</style></noscript>')
            + site_header("cv", intro) + f"""

    <main id="main" class="page-light">
      <section class="cv-shell shell">
        <div class="cv-tabs" role="tablist" aria-label="CV version">
          <button id="tab-professional" role="tab" aria-selected="true" aria-controls="panel-professional" data-cv-tab="professional">Professional</button>
          <button id="tab-academic" role="tab" aria-selected="false" aria-controls="panel-academic" data-cv-tab="academic" tabindex="-1">Academic</button>
        </div>
{professional}{academic}      </section>
    </main>

    {site_footer()}
  </body>
</html>
""")


# ---------------------------------------------------------------- homepage: shared pieces only
def update_home():
    path = ROOT / "index.html"
    s = path.read_text()
    masthead = re.search(r'      <section class="masthead shell".*?</section>\n', s, re.S).group(0)
    start = s.index('    <div class="hero-band">') if "<!-- site:header -->" not in s else s.index("<!-- site:header -->")
    end = s.index('    <main id="main">')
    s = s[:start] + site_header("home", masthead).lstrip() + "\n\n" + s[end:]
    fstart = s.index("<!-- site:footer -->") if "<!-- site:footer -->" in s else s.index('    <footer class="site-footer">')
    fend = s.index("  </body>")
    s = s[:fstart] + ("    " if not s[:fstart].endswith("    ") else "") + site_footer() + "\n" + s[fend:]
    s = re.sub(r'/assets/styles\.css\?v=[^"]+', STYLE, s)
    if 'src="/assets/site.js"' not in s:
        s = s.replace(f'<link rel="stylesheet" href="{STYLE}" />', f'<link rel="stylesheet" href="{STYLE}" />\n    <script src="/assets/site.js" defer></script>')
    path.write_text(s.replace("\n<!-- site:header -->", "\n    <!-- site:header -->"))


if __name__ == "__main__":
    update_home()
    (ROOT / "publications" / "index.html").write_text(publications_page())
    (ROOT / "cv" / "index.html").write_text(cv_page())
    print("built index.html, publications/index.html, cv/index.html")
