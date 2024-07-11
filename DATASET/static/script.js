document.getElementById('form-verificacion').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar el envío del formulario por defecto

    const numeroCedula = document.getElementById('cedula').value.trim();

    if (numeroCedula === '') {
        alert('Por favor ingrese su número de cédula.');
        return;
    }

    // Enviar el número de cédula al backend
    fetch('/verificar_permiso', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ numero_cedula: numeroCedula })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('resultado').innerText = data.mensaje;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultado').innerText = 'Error al verificar el permiso.';
    });
});
