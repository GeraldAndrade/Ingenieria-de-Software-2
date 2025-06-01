document.addEventListener('DOMContentLoaded', () => {
    console.log("Script cargado correctamente");

    const form = document.getElementById('formLogin');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const data = {
            correo: form.correo.value.trim(),
            contraseña: form.contraseña.value
        };

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const resultado = await response.json();
            console.log("Respuesta del servidor:", resultado);

            if (resultado.success) {
                if (resultado.admin) {
                    window.location.href = '/admin';
                } else {
                    window.location.href = '/bienvenida';
                }
            } else {
                document.getElementById('mensaje').textContent = resultado.mensaje;
            }
        } catch (error) {
            console.error("Error en login:", error);
            document.getElementById('mensaje').textContent = 'Error al iniciar sesión.';
        }
    });
});
