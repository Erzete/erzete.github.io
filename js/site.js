/* Progressive enhancements: links, content and screenshot scrolling work without JS. */
const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('#nav-links');
if (menuButton && menu) {
    function closeMenu(returnFocus = false) {
        menuButton.setAttribute('aria-expanded', 'false');
        menu.classList.remove('is-open');
        menuButton.querySelector('.menu-symbol').textContent = '+';
        if (returnFocus) menuButton.focus();
    }
    menuButton.addEventListener('click', () => {
        const open = menuButton.getAttribute('aria-expanded') !== 'true';
        menuButton.setAttribute('aria-expanded', String(open));
        menu.classList.toggle('is-open', open);
        menuButton.querySelector('.menu-symbol').textContent = open ? '−' : '+';
    });
    menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
    document.addEventListener('click', event => { if (!event.target.closest('.nav')) closeMenu(); });
    window.matchMedia('(min-width: 761px)').addEventListener('change', () => closeMenu());
}
document.querySelectorAll('[data-gallery]').forEach(gallery => {
    const track = gallery.querySelector('.gallery-track');
    const slides = Array.from(gallery.querySelectorAll('.gallery-slide'));
    const controls = gallery.querySelector('.gallery-controls');
    const previous = gallery.querySelector('[data-previous]');
    const next = gallery.querySelector('[data-next]');
    const count = gallery.querySelector('[data-count]');
    if (!track || !slides.length) return;
    controls.hidden = false;
    let index = 0;
    let frame = 0;
    function update() {
        const slideWidth = slides[0].getBoundingClientRect().width;
        index = slideWidth ? Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / slideWidth))) : 0;
        previous.disabled = index === 0;
        next.disabled = index === slides.length - 1;
        count.textContent = `${index + 1} / ${slides.length}`;
    }
    function goTo(target) {
        const bounded = Math.max(0, Math.min(slides.length - 1, target));
        track.scrollTo({ left: slides[0].getBoundingClientRect().width * bounded, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    }
    previous.addEventListener('click', () => goTo(index - 1));
    next.addEventListener('click', () => goTo(index + 1));
    track.addEventListener('keydown', event => {
        if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
            event.preventDefault();
            goTo(index + (event.key === 'ArrowRight' ? 1 : -1));
        }
        if (event.key === 'Home' || event.key === 'End') {
            event.preventDefault();
            goTo(event.key === 'Home' ? 0 : slides.length - 1);
        }
    });
    track.addEventListener('scroll', () => { cancelAnimationFrame(frame); frame = requestAnimationFrame(update); }, { passive: true });
    new ResizeObserver(() => {
        track.scrollTo({ left: slides[0].getBoundingClientRect().width * index, behavior: 'instant' });
        update();
    }).observe(track);
    update();
});
