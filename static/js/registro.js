document.getElementById('formRegistro').addEventListener('submit', async function(e) {
    if (!this.checkValidity()) {
        // Mostrará automáticamente las burbujas nativas
        return;
    }

    e.preventDefault(); 

    const data = {
        nombre: this.nombre.value.trim(),
        correo: this.correo.value.trim(),
        usuario: this.usuario.value.trim(),
        contraseña: this.contraseña.value
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const resultado = await response.json();
        document.getElementById('mensaje').textContent = resultado.mensaje;

        // Limpia el formulario tras éxito
        this.reset();

    } catch (error) {
        document.getElementById('mensaje').textContent = 'Error al registrar.';
        console.error(error);
    }
});
