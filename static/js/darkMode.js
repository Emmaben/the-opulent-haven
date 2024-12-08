const themeToggleBtns = document.querySelectorAll('#theme-toggle');

// State
const theme = localStorage.getItem('theme');

// On Mount
theme && document.body.classList.add(theme);

// Handlers
const handleThemeToggle = () => {
    document.body.classList.toggle('light-mode');
    if (document.body.classList.contains('light-mode')) {
        localStorage.setItem('theme', 'light-mode');
    } else {
        localStorage.removeItem('theme');
        document.body.removeAttribute('class');
    }
};

// Events
themeToggleBtns.forEach(btn =>
    btn.addEventListener('click', handleThemeToggle)
);

/* This JavaScript code implements a theme toggle functionality that allows
    users to switch between a default theme (dark mode) and a light mode.
    It uses localStorage to remember the user's preferred theme across sessions
    and dynamically updates the webpage styling based on the chosen theme.
*/