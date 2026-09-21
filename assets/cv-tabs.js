const tabs = [...document.querySelectorAll('[data-cv-tab]')];
const panels = [...document.querySelectorAll('[data-cv-panel]')];

function activateCvView(view, moveFocus = false) {
  const selected = tabs.find((tab) => tab.dataset.cvTab === view) ?? tabs[0];

  tabs.forEach((tab) => {
    const active = tab === selected;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
  });

  panels.forEach((panel) => {
    panel.hidden = panel.dataset.cvPanel !== selected.dataset.cvTab;
  });

  const url = new URL(window.location.href);
  if (selected.dataset.cvTab === 'professional') url.searchParams.delete('view');
  else url.searchParams.set('view', selected.dataset.cvTab);
  window.history.replaceState({}, '', url);

  if (moveFocus) selected.focus();
}

tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => activateCvView(tab.dataset.cvTab));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let nextIndex = index;
    if (event.key === 'ArrowRight') nextIndex = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') nextIndex = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = tabs.length - 1;
    activateCvView(tabs[nextIndex].dataset.cvTab, true);
  });
});

const requestedView = new URL(window.location.href).searchParams.get('view');
activateCvView(requestedView === 'academic' ? 'academic' : 'professional');
