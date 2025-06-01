document.addEventListener('DOMContentLoaded', () => {
  const btnAgregar = document.getElementById('btn-agregar-pelicula');
  const modal = document.getElementById('formulario-container');
  const form = document.getElementById('formPelicula');
  const posterInput = document.getElementById('poster');
  const preview = document.getElementById('preview');
  const mensaje = document.getElementById('mensaje');

  let posterBase64 = '';
  let modoEdicion = false;
  let idPeliculaEditar = null;

  // Mostrar modal para agregar
  btnAgregar.addEventListener('click', () => {
    modal.style.display = 'flex';
    modoEdicion = false;
    form.reset();
    preview.src = '';
    posterBase64 = '';
    mensaje.textContent = '';
  });

  // Cerrar modal al hacer clic fuera
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      form.reset();
      preview.src = '';
      posterBase64 = '';
      mensaje.textContent = '';
      modoEdicion = false;
    }
  });

  // Vista previa del póster
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

  // Enviar formulario
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

    if (!modoEdicion && !posterBase64) {
      mensaje.textContent = 'Por favor selecciona una imagen para el póster.';
      mensaje.className = 'mensaje error';
      return;
    }

    try {
      const url = modoEdicion ? `/admin/editar_pelicula/${idPeliculaEditar}` : '/admin/agregar_pelicula';
      const method = modoEdicion ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
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
        mensaje.textContent = result.mensaje || 'Error al guardar la película.';
        mensaje.className = 'mensaje error';
      }
    } catch (error) {
      console.error(error);
      mensaje.textContent = 'Error de conexión.';
      mensaje.className = 'mensaje error';
    }
  });

  // Botones de editar
  document.querySelectorAll('.btn-editar').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;

      try {
        const res = await fetch(`/admin/obtener_pelicula/${id}`);
        const data = await res.json();

        if (res.ok) {
          form.titulo.value = data.titulo;
          form.año.value = data.año;
          form.genero.value = data.genero;
          form.director.value = data.director;
          form.precio.value = data.precio;
          preview.src = data.poster;
          posterBase64 = data.poster;
          idPeliculaEditar = id;
          modoEdicion = true;
          modal.style.display = 'flex';
        } else {
          alert('No se pudo cargar la información de la película.');
        }
      } catch (err) {
        console.error(err);
        alert('Error al obtener la película.');
      }
    });
  });

  // Botones de eliminar
  document.querySelectorAll('.btn-eliminar').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      const confirmar = confirm('¿Estás seguro de eliminar esta película?');

      if (!confirmar) return;

      try {
        const res = await fetch(`/admin/eliminar_pelicula/${id}`, {
          method: 'DELETE'
        });

        const data = await res.json();

        if (res.ok) {
          alert(data.mensaje);
          location.reload();
        } else {
          alert(data.mensaje || 'Error al eliminar la película.');
        }
      } catch (err) {
        console.error(err);
        alert('Error de conexión.');
      }
    });
  });
});
