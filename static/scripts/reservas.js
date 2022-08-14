const fecha_entrada = document.getElementById("fechaEntrada").value
const fecha_salida = document.getElementById("fechaSalida").value
const usuarioActivo = document.getElementById("usuario_activo").value




const seleccionarHabitacion = document.getElementsByClassName("boton_sel")



document.getElementsByName("seleccionarHabitacion").forEach(
    (element, index) => element.addEventListener("click",
        function (event) {
            event.preventDefault()
            // document.getElementById()
            console.log("hola")
             fetch('http://127.0.0.1:5000/reservas')
                .then(response => response.json())
                .then(data => console.log(data));

            }
        ))
function get_id() {
    document.on('click', 'input[type="button"]', function(event) {
        let id = this.id;
        console.log("Se presionó el Boton con Id :"+ id)
    });
};

function ProcesarIdReserva(seleccionarHabitacion){
    let id = seleccionarHabitacion.id;
    console.log(id);
    console.log("usuario activo es:" + usuarioActivo);
    fetch('http://127.0.0.1:5000/habitaciones/' + id)
        .then(response => response.json())
        .then(data => console.log(data));
    const precio = fetch('http://127.0.0.1:5000/habitaciones/' + id)
                    .then(response => response.json())
                    .then(data => console.log(data.habitacion.precio));
    console.log(precio);
    const post = fetch('http://127.0.0.1:5000/habitaciones/' + id)
                    .then(response => response.json())
                    .then(data => console.log('{ "user_id": ' + '"' + usuarioActivo + '"' + ', "habitacion_id": ' + '"' + data.habitacion._id + '"' + ', "fecha_entrada": ' + '"' + document.getElementById("fechaEntrada").value + '"' + "," + ' "fecha_salida": ' + '"' + document.getElementById("fechaSalida").value + '"' + " }"));
    console.log(post);
}


    
fetch('http://127.0.0.1:5000/habitaciones/1')
  .then(response => response.json())
  .then(data => console.log(data));