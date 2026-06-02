// Cambiar el display para por cada click
function caracteristicas_pie(){
    let nombres = document.getElementsByClassName("name_user_r");
    let pie_grafic = document.getElementById("pie-chart");
    let pie_date = document.getElementById("pieDate")

    let por_ocupado = 0;
    let disponibles = 0;

    // Si no hay nombres, evitamos que la división por cero rompa el cálculo
    if (nombres.length === 0) return;

    for(let j = 0; j < nombres.length; j++){
        if(nombres[j].innerText == "-"){
            disponibles ++;
        }
    }
    por_ocupado = Math.floor(((nombres.length - disponibles) / nombres.length) * 100);
    pie_date.innerText = `${por_ocupado}%`;
    pie_grafic.style.background = `conic-gradient( #00f2fe 0% ${por_ocupado}%, rgba(0,0,0,0) ${por_ocupado}% 100%)`;
}

function desplegar_tablero() {
    let dias_calen = document.getElementsByClassName("dia");
    let dashboard = document.getElementById("sectionDashboard");
    let tablero_informacion = document.getElementById("container-hide");

    for (let i = 0; i < dias_calen.length; i++ ){
        dias_calen[i].addEventListener("click", function(event) {
            tablero_informacion.style.display = "flex";
            dashboard.style.height = "100%";
        });
    }
}

function calendario_click() {
    const dias = document.getElementsByClassName("dia-normal");

    for (let i = 0; i < dias.length; i++) {
        dias[i].onclick = () => {
            // Evaluamos si el día clickeado actualmente está vacío/transparente
            let estabaTransparente = (dias[i].style.backgroundColor === "transparent" || dias[i].style.backgroundColor === "");

            // 1. LIMPIAR TODOS LOS DÍAS
            // Recorremos todos los días y los reseteamos a su color original
            for (let j = 0; j < dias.length; j++) {
                dias[j].style.backgroundColor = "transparent";
                dias[j].style.color = "";
            }

            // 2. PINTAR SOLO EL SELECCIONADO:
            // Si el que clickeamos estaba transparente, lo pintamos (si ya estaba pintado, el paso anterior lo despintó y funcionará como un botón para "apagarlo")
            if (estabaTransparente) {
                dias[i].style.backgroundColor = "#00f2fe";
                dias[i].style.color = "#0f172a";
            }

            // Llamamos a la función para que recalcule los porcentajes al instante
            caracteristicas_pie();
        }
    }
}

//Llamada a funciones iniciales
desplegar_tablero();
caracteristicas_pie();
calendario_click();