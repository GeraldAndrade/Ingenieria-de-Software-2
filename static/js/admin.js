document.addEventListener('DOMContentLoaded', () => {
  const btnAgregar = document.getElementById('btn-agregar-pelicula');
  const modal = document.getElementById('formulario-container');
  const form = document.getElementById('formPelicula');
  const posterInput = document.getElementById('poster');
  const preview = document.getElementById('preview');
  const mensaje = document.getElementById('mensaje');

  let posterBase64 = '';

  btnAgregar.addEventListener('click', () => {
    modal.style.display = 'flex';
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      form.reset();
      preview.src = '';
      posterBase64 = '';
      mensaje.textContent = '';
    }
  });

  posterInput.addEventListener('change', () => {
    const file = posterInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      posterBase64 = reader.result;
      preview.src = posterBase64;
    };
    reader.readAsDataURL(file);
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      titulo: form.titulo.value.trim(),
      año: form.año.value.trim(),
      genero: form.genero.value.trim(),
      director: form.director.value.trim(),
      precio: parseFloat(form.precio.value.trim()), 
      poster: posterBase64
    };

    if (!posterBase64) {
      mensaje.textContent = 'Por favor selecciona una imagen para el póster.';
      mensaje.className = 'mensaje error';
      return;
    }

    try {
      const response = await fetch('/admin/agregar_pelicula', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        mensaje.textContent = result.mensaje;
        mensaje.className = 'mensaje';
        form.reset();
        preview.src = '';
        posterBase64 = '';
        setTimeout(() => location.reload(), 1000);
      } else {
        mensaje.textContent = result.mensaje || 'Error al agregar la película.';
        mensaje.className = 'mensaje error';
      }
    } catch (error) {
      console.error(error);
      mensaje.textContent = 'Error de conexión.';
      mensaje.className = 'mensaje error';
    }
  });
});
