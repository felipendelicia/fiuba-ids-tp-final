// Cambiar el display para por cada click
function caracteristicas_pie(_){   
    nombres = document.getElementsByClassName("name_user_r");
    pie_grafic = document.getElementById("pie-chart");
    pie_date = document.getElementById("pieDate")
    
    por_ocupado = 0; 
    disponibles = 0; 
    for(let j = 0; j < nombres.length; j++){
        if(nombres[j].innerText == "-"){
            disponibles ++;
        }
    }
    por_ocupado = ((nombres.length - disponibles)/nombres.length)*100;
    pie_date.innerText = `${por_ocupado}%`;
    pie_grafic.style.background = `conic-gradient(orange 0% ${por_ocupado}%, white ${por_ocupado}% 100%)`;
}

function desplegar_tablero() {
    dias_calen = document.getElementsByClassName("dia");
    dashboard = document.getElementById("sectionDashboard");

    tablero_informacion = document.getElementById("container-hide");

    for (let i = 0; i < dias_calen.length; i++ ){
        dias_calen[i].addEventListener("click", function(event) {
            tablero_informacion.style.display = "flex";
            dashboard.style.height = "100%";
        } );
    }
}

// llamda a funciones
desplegar_tablero();
caracteristicas_pie();