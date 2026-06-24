/*Modal generico*/
function abrirModalConfirm(mensaje) {
    var modal = document.getElementById('modal-confirm');
    document.getElementById('modal-confirm-msg').innerHTML = mensaje.replace(/\n/g, '<br>');
    document.getElementById('modal-confirm-cancel').style.display = 'inline-block';

    var resolverConfirmacion;
    var promesaConfirmacion = new Promise(function(r) { resolverConfirmacion = r; });

    function cerrarModal(respuesta) {
        modal.style.display = 'none';
        document.getElementById('modal-confirm-ok').removeEventListener('click', onAceptar);
        document.getElementById('modal-confirm-cancel').removeEventListener('click', onCancelar);
        modal.removeEventListener('click', onFondo);
        resolverConfirmacion(respuesta);
    }

    function onAceptar() { cerrarModal(true); }
    function onCancelar() { cerrarModal(false); }
    function onFondo(e) { if (e.target === modal) cerrarModal(false); }

    document.getElementById('modal-confirm-ok').addEventListener('click', onAceptar);
    document.getElementById('modal-confirm-cancel').addEventListener('click', onCancelar);
    modal.addEventListener('click', onFondo);
    modal.style.display = 'flex';

    return promesaConfirmacion;
}

function abrirModalAlerta(mensaje) {
    var modal = document.getElementById('modal-confirm');
    document.getElementById('modal-confirm-msg').innerHTML = mensaje.replace(/\n/g, '<br>');
    document.getElementById('modal-confirm-cancel').style.display = 'none';

    var resolverAlerta;
    var promesaAlerta = new Promise(function(r) { resolverAlerta = r; });

    function cerrarModal() {
        modal.style.display = 'none';
        document.getElementById('modal-confirm-ok').removeEventListener('click', onAceptar);
        modal.removeEventListener('click', onFondo);
        resolverAlerta();
    }

    function onAceptar() { cerrarModal(); }
    function onFondo(e) { if (e.target === modal) cerrarModal(); }

    document.getElementById('modal-confirm-ok').addEventListener('click', onAceptar);
    modal.addEventListener('click', onFondo);
    modal.style.display = 'flex';

    return promesaAlerta;
}

/* modal de perfil para agregar mapas favoritos*/
function abrirModalMapas() {
    document.getElementById('modal-mapas').style.display = 'flex';
}

function cerrarModalMapas() {
    document.getElementById('modal-mapas').style.display = 'none';
}

function agregarFavorito(mapId) {
    cerrarModalMapas();
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = '/perfil/favoritos/agregar/' + mapId;
    document.body.appendChild(form);
    form.submit();
}

function eliminarFavorito(mapId) {
    document.getElementById('modal-confirm-eliminar').dataset.mapId = mapId;
    document.getElementById('modal-confirm-eliminar').style.display = 'flex';
}

function confirmarEliminar() {
    var mapId = document.getElementById('modal-confirm-eliminar').dataset.mapId;
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = '/perfil/favoritos/eliminar/' + mapId;
    document.body.appendChild(form);
    form.submit();
}

function cerrarConfirmEliminar() {
    document.getElementById('modal-confirm-eliminar').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    var botones = document.querySelectorAll('.tab-btn');
    var secciones = document.querySelectorAll('.tab-seccion');

    botones.forEach(function(boton) {
        boton.addEventListener('click', function() {
            botones.forEach(function(b) { b.classList.remove('active'); });
            secciones.forEach(function(s) { s.classList.remove('active'); });
            this.classList.add('active');
            document.querySelector(this.dataset.target).classList.add('active');
        });
    });

    var modalMapas = document.getElementById('modal-mapas');
    if (modalMapas) {
        modalMapas.addEventListener('click', function(e) {
            if (e.target === this) cerrarModalMapas();
        });
    }
});
