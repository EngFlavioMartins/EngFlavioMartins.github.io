const workTabs = [...document.querySelectorAll('[data-work-tab]')];
const workPanels = [...document.querySelectorAll('[data-work-panel]')];

function selectWork(key, moveFocus = false) {
  workTabs.forEach((tab) => {
    const selected = tab.dataset.workTab === key;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
    if (selected && moveFocus) tab.focus();
  });

  workPanels.forEach((panel) => {
    panel.hidden = panel.dataset.workPanel !== key;
  });
}

workTabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectWork(tab.dataset.workTab));
  tab.addEventListener('keydown', (event) => {
    let nextIndex;

    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (index + 1) % workTabs.length;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (index - 1 + workTabs.length) % workTabs.length;
    if (event.key === 'Home') nextIndex = 0;
    if (event.key === 'End') nextIndex = workTabs.length - 1;

    if (nextIndex === undefined) return;
    event.preventDefault();
    selectWork(workTabs[nextIndex].dataset.workTab, true);
  });
});
