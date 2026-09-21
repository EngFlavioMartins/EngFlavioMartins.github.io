const categories = [
  { id: 'software-methods', name: 'Scientific software & numerical methods' },
  { id: 'fluid-mechanics', name: 'Fluid mechanics & wind energy' },
  { id: 'structures', name: 'Structures & optimisation' },
  { id: 'dynamical-systems', name: 'Dynamical systems' }
];

const publications = [
  { category: 'software-methods', year: 2026, kind: 'Journal article', status: 'Accepted', title: 'OpenONDA: A Python Interface for In-Line Control of OpenFOAM Solvers', authors: ['Flavio A. C. Martins'], venue: 'OpenFOAM Journal', url: 'https://github.com/EngFlavioMartins/OpenONDA' },
  { category: 'software-methods', year: 2026, kind: 'Preprint', title: 'Toward Meshless Turbulent Flow Simulation: LES-Integrated Vortex Particle Method', authors: ['Flavio A. C. Martins', 'A. van Zuijlen', 'C. S. Ferreira'], venue: 'arXiv', doi: '10.48550/arXiv.2601.06942', url: 'https://arxiv.org/abs/2601.06942' },
  { category: 'software-methods', year: 2026, kind: 'Conference paper', title: 'Toward a 3D Hybrid Vortex Particle–Grid Approach for External Flows', authors: ['Flavio A. C. Martins', 'A. van Zuijlen', 'D. A. von Terzi'], venue: 'Journal of Physics: Conference Series, 3224(4), 042069', doi: '10.1088/1742-6596/3224/4/042069', url: 'https://doi.org/10.1088/1742-6596/3224/4/042069' },
  { category: 'software-methods', year: 2022, kind: 'Conference contribution', title: 'State-Observer-Based Data Assimilation for Real Flow Analysis: Integrating Computation and Measurement', authors: ['Flavio A. C. Martins', 'A. Alcântara', 'D. E. Rival'], venue: 'NATO Unclassified technical meeting' },

  { category: 'fluid-mechanics', year: 2025, kind: 'Journal article', title: 'Proof of Concept for Multirotor Systems with Vortex-Generating Modes for Regenerative Wind Energy: A Study Based on Numerical Simulations and Experimental Data', authors: ['Flavio A. C. Martins', 'A. van Zuijlen', 'C. S. Ferreira'], venue: 'Wind Energy Science, 10, 41–58', doi: '10.5194/wes-10-41-2025', url: 'https://doi.org/10.5194/wes-10-41-2025' },
  { category: 'fluid-mechanics', year: 2024, kind: 'Conference paper', title: 'Numerical Investigation of Atmospheric Boundary Layer Control in Wind Farms with Multirotor Systems', authors: ['Flavio A. C. Martins', 'C. S. Ferreira', 'A. van Zuijlen'], venue: 'Journal of Physics: Conference Series, 2767(7), 072006', doi: '10.1088/1742-6596/2767/7/072006', url: 'https://doi.org/10.1088/1742-6596/2767/7/072006' },
  { category: 'fluid-mechanics', year: 2024, kind: 'Conference paper', title: 'Enhancing Wind Farm Efficiency Through Active Control of the Atmospheric Boundary Layer’s Vertical Entrainment of Momentum', authors: ['C. S. Ferreira', 'D. Bensason', 'T. J. Broertjes', 'A. Sciacchitano', 'Flavio A. C. Martins', 'A. G. Ajay'], venue: 'Journal of Physics: Conference Series, 2767(9), 092107', doi: '10.1088/1742-6596/2767/9/092107', url: 'https://doi.org/10.1088/1742-6596/2767/9/092107' },
  { category: 'fluid-mechanics', year: 2021, kind: 'Journal article', title: 'Detection of Vortical Structures in Sparse Lagrangian Data Using Coherent-Structure Colouring', authors: ['Flavio A. C. Martins', 'A. Sciacchitano', 'D. E. Rival'], venue: 'Experiments in Fluids, 62(4), 69', doi: '10.1007/s00348-021-03135-5', url: 'https://doi.org/10.1007/s00348-021-03135-5' },
  { category: 'fluid-mechanics', year: 2021, kind: 'Preprint', title: 'A Voronoi-Tessellation-Based Approach for Detection of Coherent Structures in Sparsely-Seeded Flows', authors: ['Flavio A. C. Martins', 'D. E. Rival'], venue: 'arXiv', doi: '10.48550/arXiv.2103.09884', url: 'https://arxiv.org/abs/2103.09884' },
  { category: 'fluid-mechanics', year: 2019, kind: 'Journal article', title: 'Effects of the Reynolds Number and Structural Damping on Vortex-Induced Vibrations of an Elastically-Mounted Rigid Cylinder', authors: ['Flavio A. C. Martins', 'J. P. J. Avila'], venue: 'International Journal of Mechanical Sciences, 156, 235–249', doi: '10.1016/j.ijmecsci.2019.03.024', url: 'https://doi.org/10.1016/j.ijmecsci.2019.03.024' },
  { category: 'fluid-mechanics', year: 2019, kind: 'Journal article', title: 'Three-Dimensional CFD Analysis of Damping Effects on Vortex-Induced Vibrations of 2DOF Elastically-Mounted Circular Cylinders', authors: ['Flavio A. C. Martins', 'J. P. J. Avila'], venue: 'Marine Structures, 65, 12–31', doi: '10.1016/j.marstruc.2019.01.005', url: 'https://doi.org/10.1016/j.marstruc.2019.01.005' },
  { category: 'fluid-mechanics', year: 2018, kind: 'Conference contribution', title: 'Three-Dimensional CFD Analysis of Damping Effects on Vortex-Induced Vibrations of 2DOF Cylinders', authors: ['Flavio A. C. Martins', 'J. P. J. Avila'], venue: 'SIIC-USP' },

  { category: 'structures', year: 2019, kind: 'Journal article', title: 'A Linear Approach for Sizing Optimization of Isostatic Trussed Structures Subjected to External and Self-Weight Loads', authors: ['Flavio A. C. Martins', 'J. P. J. Avila', 'M. A. da Silva'], venue: 'International Journal of Steel Structures, 19(4), 1146–1157', doi: '10.1007/s13296-018-0194-8', url: 'https://doi.org/10.1007/s13296-018-0194-8' },
  { category: 'structures', year: 2018, kind: 'Conference paper', title: 'Detection of Damage in Aerospace Structures Using Optimization Techniques on Impact Tests Results', authors: ['Flavio A. C. Martins', 'M. A. da Silva', 'R. M. L. R. F. Brasil'], venue: 'Proceeding Series of the Brazilian Society of Computational and Applied Mathematics', url: 'https://proceedings.sbmac.org.br/sbmac/article/download/1878/1896' },
  { category: 'structures', year: 2017, kind: 'Conference paper', title: 'Topology Optimization of 2D Trussed Structures', authors: ['Flavio A. C. Martins', 'M. Araujo', 'R. Brasil'], venue: 'CILAMCE', doi: '10.20906/cps/cilamce2017-0035', url: 'https://doi.org/10.20906/cps/cilamce2017-0035' },
  { category: 'structures', year: 2017, kind: 'Conference contribution', title: 'Analysis of the Dynamic Response of the Internal Structure of the ONERA M6 Wing', authors: ['Flavio A. C. Martins', 'M. da Silva'], venue: 'IX Workshop in Dynamic Systems' },
  { category: 'structures', year: 2017, kind: 'Conference contribution', title: 'Identification of Damage in Aerospace Structures Using Optimization Techniques and Impact Tests', authors: ['Flavio A. C. Martins', 'M. da Silva'], venue: 'ASCE Engineering Mechanics Institute Conference' },

  { category: 'dynamical-systems', year: 2018, kind: 'Journal article', title: 'Mecânica Celeste e a Teoria dos Sistemas Dinâmicos: Uma Revisão do Problema Circular Restrito de Três Corpos', authors: ['Flavio A. C. Martins', 'M. Zanotello'], venue: 'Revista Brasileira de Ensino de Física, 40(2), e2310', doi: '10.1590/1806-9126-rbef-2017-0174', url: 'https://doi.org/10.1590/1806-9126-rbef-2017-0174' }
];

const list = document.querySelector('#publication-list');
const count = document.querySelector('#publication-count');
const categoryNav = document.querySelector('#publication-categories');

function emphasiseFlavio(authors) {
  const fragment = document.createDocumentFragment();

  authors.forEach((author, index) => {
    const isFlavio = /flavio|f\.\s*a\.\s*c\.\s*martins/i.test(author);
    const node = isFlavio ? document.createElement('strong') : document.createTextNode(author);
    if (isFlavio) node.textContent = author;
    fragment.append(node);
    if (index < authors.length - 1) fragment.append(document.createTextNode(', '));
  });

  return fragment;
}

function createEntry(item) {
  const article = document.createElement('article');
  article.className = 'publication-entry';

  const year = document.createElement('p');
  year.className = 'publication-year';
  year.textContent = String(item.year);

  const body = document.createElement('div');
  const type = document.createElement('p');
  type.className = 'publication-kind';
  type.textContent = item.status ? `${item.kind} · ${item.status}` : item.kind;

  const title = document.createElement('h3');
  if (item.url) {
    const link = document.createElement('a');
    link.href = item.url;
    link.rel = 'noreferrer';
    link.textContent = item.title;
    title.append(link);
  } else {
    title.textContent = item.title;
  }

  const authors = document.createElement('p');
  authors.className = 'publication-authors';
  authors.append(emphasiseFlavio(item.authors));

  const meta = document.createElement('p');
  meta.className = 'publication-meta';
  const metadata = [item.venue];
  if (item.doi) metadata.push(`DOI ${item.doi}`);
  meta.textContent = metadata.filter(Boolean).join(' · ');

  body.append(type, title, authors, meta);
  article.append(year, body);
  return article;
}

function render() {
  count.textContent = String(publications.length);
  list.replaceChildren();
  categoryNav.replaceChildren();

  categories.forEach((category, index) => {
    const records = publications
      .filter((publication) => publication.category === category.id)
      .sort((a, b) => b.year - a.year || a.title.localeCompare(b.title));

    const navLink = document.createElement('a');
    navLink.href = `#${category.id}`;
    navLink.textContent = `${category.name} (${records.length})`;
    categoryNav.append(navLink);

    const section = document.createElement('section');
    section.id = category.id;
    section.className = 'publication-category';
    section.setAttribute('aria-labelledby', `${category.id}-heading`);

    const header = document.createElement('header');
    const number = document.createElement('p');
    number.className = 'category-number';
    number.textContent = String(index + 1).padStart(2, '0');
    const heading = document.createElement('h2');
    heading.id = `${category.id}-heading`;
    heading.textContent = category.name;
    const total = document.createElement('p');
    total.className = 'category-total';
    total.textContent = `${records.length} ${records.length === 1 ? 'publication' : 'publications'}`;
    header.append(number, heading, total);

    const entries = document.createElement('div');
    entries.className = 'publication-entries';
    records.forEach((record) => entries.append(createEntry(record)));

    section.append(header, entries);
    list.append(section);
  });
}

render();
