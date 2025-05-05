// static/js/theme-toggle.js

// Плавный переход фона и текста
document.documentElement.style.transition =
  'background-color 0.3s ease, color 0.3s ease';

// Иконки
const btn = document.getElementById('theme-toggle');
const iconLight = document.getElementById('icon-light');
const iconDark  = document.getElementById('icon-dark');

// Устанавливаем тему и обновляем иконки
function setTheme(theme) {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  localStorage.setItem('theme', theme);
  iconDark.classList.toggle('hidden', theme !== 'dark');
  iconLight.classList.toggle('hidden', theme === 'dark');
}

// При клике переключаем
btn.addEventListener('click', () => {
  const next = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
  setTheme(next);
});

// При загрузке: сначала из localStorage, потом из prefers-color-scheme
window.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark' || saved === 'light') {
    setTheme(saved);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    setTheme('dark');
  } else {
    setTheme('light');
  }
});
