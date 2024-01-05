var themeIcon = $('#themeIcon');
function setTheme(theme) {
    if (theme === 'dark') {
        $('html').attr('data-bs-theme', 'dark');
        $('#themeIcon').attr('class', 'bi-moon-stars-fill');
    } else if (theme === 'light') {
        $('html').attr('data-bs-theme', 'light');
        $('#themeIcon').attr('class', 'bi-brightness-high-fill');
    } else if (theme == 'os') {
        $('html').attr('data-bs-theme', (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
            ? 'dark'
            : 'light');
        $('#themeIcon').attr('class', 'bi-circle-half');
    }
    localStorage.setItem('theme', theme);
}

var siteTheme = (localStorage.getItem('theme') != null)
    ? localStorage.getItem('theme')
    : 'os';
setTheme(siteTheme);