// Size the homepage portrait to the text block beside it (name, role and summary), so the photo
// runs from the top of the name to the last line of the summary. Without JS the CSS size applies.
const portraitText = document.querySelector('.masthead-text');
const portrait = document.querySelector('.masthead-portrait');

if (portraitText && portrait && 'ResizeObserver' in window) {
  new ResizeObserver(() => {
    portrait.style.setProperty('--portrait-size', `${Math.round(portraitText.getBoundingClientRect().height)}px`);
  }).observe(portraitText);
}
