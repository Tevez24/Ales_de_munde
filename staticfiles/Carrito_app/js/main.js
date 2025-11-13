document.addEventListener('DOMContentLoaded', () => { 
  const searchButton = document.querySelector('.search-bar button');
  const searchInput = document.querySelector('.search-bar input');

  if (searchButton) {
    searchButton.addEventListener('click', () => {
      const query = searchInput.value.trim();
      if (query) {
        alert(`Buscando viajes a: ${query}`);
      } else {
        alert('Por favor ingresa un destino.');
      }
    });
  }

  const loginForm = document.querySelector('#login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const email = loginForm.querySelector('input[type="email"]').value;
      const password = loginForm.querySelector('input[type="password"]').value;

      if (email === 'admin@viajespro.com' && password === '1234') {
        alert('Inicio de sesión exitoso.');
        window.location.href = djangoInicioUrl;
      } else {
        alert('Credenciales incorrectas.');
      }
    });
  }
});
