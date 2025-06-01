document.addEventListener('DOMContentLoaded', () => {
    const botonesFavorita = document.querySelectorAll('.favorita-btn');
    const botonesRentar = document.querySelectorAll('.rentar-btn');
    const botonGlobalRentar = document.getElementById('rentar-global-btn');
    const mensajeGeneral = document.getElementById('mensaje-renta');

    // Añadir a favoritas (solo añadir, no toggle)
    botonesFavorita.forEach(boton => {
        boton.addEventListener('click', async () => {
            const peliculaDiv = boton.closest('.pelicula');
            const peliculaId = peliculaDiv.getAttribute('data-id');
            const mensajeSpan = peliculaDiv.querySelector('.mensaje-favorita');

            try {
                const response = await fetch(`/usuario/favorita/${peliculaId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include'
                });

                const data = await response.json();
                mensajeSpan.textContent = response.ok ? 'Añadida a la lista ✅' : (data.mensaje || 'Error al agregar');
                if (response.ok) boton.disabled = true;

            } catch (error) {
                mensajeSpan.textContent = 'Error de conexión';
            }
        });
    });

    botonesRentar.forEach(boton => {
        boton.addEventListener('click', async () => {
            const peliculaDiv = boton.closest('.pelicula');
            const peliculaId = peliculaDiv.getAttribute('data-id');
            const agregadaActual = boton.getAttribute('data-agregada') === 'true';

            try {
                const response = await fetch(`/usuario/rentar/${peliculaId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Remove': agregadaActual ? 'true' : 'false'  // Para backend saber si quitar o agregar
                    },
                    credentials: 'include'
                });

                const data = await response.json();

                if (response.ok) {
                    if (agregadaActual) {
                        // Si estaba agregada, ahora la quitamos
                        boton.textContent = 'Añadir para renta';
                        boton.setAttribute('data-agregada', 'false');
                        mensajeGeneral.textContent = 'Película eliminada del carrito 🗑️';
                    } else {
                        // Si no estaba agregada, ahora la añadimos
                        boton.textContent = 'Eliminar de renta';
                        boton.setAttribute('data-agregada', 'true');
                        mensajeGeneral.textContent = 'Película añadida al carrito ✅';
                    }
                } else {
                    mensajeGeneral.textContent = data.mensaje || 'Error al procesar la solicitud';
                }

            } catch (error) {
                mensajeGeneral.textContent = 'Error de conexión';
            }

            // Limpia mensaje después de 3 segundos
            setTimeout(() => mensajeGeneral.textContent = '', 3000);
        });
    });

    // Botón global para ver resumen de renta
    if (botonGlobalRentar) {
        botonGlobalRentar.addEventListener('click', () => {
            window.location.href = '/usuario/rentar/resumen';
        });
    }
    const inputBusqueda = document.getElementById('busqueda-pelicula');
    const peliculasContainer = document.getElementById('peliculas-container');

    inputBusqueda.addEventListener('input', () => {
        const filtro = inputBusqueda.value.toLowerCase();

        const peliculas = peliculasContainer.querySelectorAll('.pelicula');

        peliculas.forEach(pelicula => {
            const titulo = pelicula.querySelector('h3').textContent.toLowerCase();
            const genero = pelicula.querySelector('p').textContent.toLowerCase(); // Asumiendo que es el primer <p> con género

        // Mostrar si el filtro coincide en título o género
            if (titulo.includes(filtro) || genero.includes(filtro)) {
                pelicula.style.display = '';
            } else {
                pelicula.style.display = 'none';
            }
    });
});

});
