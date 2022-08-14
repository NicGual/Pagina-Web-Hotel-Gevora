var fecha_entrada;
var fecha_salida;
const usuarioActivo = document.getElementById("usuario_activo").value

var Vector = [];
var Vector_post = [];
var Precio = [];
var Conteo = [];
var Datos = "";
var Suma = 0;
var TotalConteo = 0;
var Ultimo_precio;
var Size_vector;

const seleccionarHabitacion = document.getElementsByClassName("boton_sel")

function ProcesarFechas(){
    const f_entrada = document.getElementById("fechaEntrada").value
    const date = f_entrada;
    const [year, month, day] = date.split('-');
    fecha_entrada = [day, month, year].join('/');
    // console.log(fecha_entrada);
    document.getElementById("f_ent").innerHTML = fecha_entrada;
    const f_salida = document.getElementById("fechaSalida").value
    const date_out = f_salida;
    const [ano, mes, dia] = date_out.split('-');
    fecha_salida = [dia, mes, ano].join('/');
    // console.log(fecha_salida);
    document.getElementById("f_sal").innerHTML = fecha_salida;
    // procesar fechas
    var fechaInicio = new Date(f_entrada).getTime();
    var fechaFin    = new Date(f_salida).getTime();
    var diff = fechaFin - fechaInicio;
    // console.log(diff/(1000*60*60*24) );
    document.getElementById("noches").innerHTML = ((diff/(1000*60*60*24))+1) + " dias y " + (diff/(1000*60*60*24)) + " Noches";
    // comprobar que selecciono fechas
    if ( fecha_entrada == "//" || fecha_salida == "//" ){

    } else{
        document.getElementById("user_title").style.display = "block";
        document.getElementById("separacion").style.display = "block";
        document.getElementById("contenedor").style.display = "block";
    }
}

function ProcesarIdReserva(seleccionarHabitacion){
    fetch('http://127.0.0.1:5000/habitaciones')
            .then(response => response.json())
            .then(data => {
                const json = (data);
                const tamano_vector = json;
                Size_vector = Object.keys(tamano_vector.Habitaciones).length;
                // console.log(Size_vector);
                // console.log(Object.keys(json.Habitaciones).length);
    });
    let id = seleccionarHabitacion.id;
    var estado_button = 0;
    var uno = document.getElementById(id);
    if (uno.innerHTML == 'Seleccionar'){
        uno.innerHTML = 'Seleccionado';
        uno.style.backgroundColor = "green";
        estado_button = 1;
    }
    else {
        uno.innerHTML = 'Seleccionar';
        uno.style.backgroundColor = "#FF725E";
        estado_button = 0;
    }

    console.log("estado de boton: " + estado_button)
         
    console.log("id de habitacion: " + id);
    console.log("usuario activo es:" + usuarioActivo);
    // fetch('http://127.0.0.1:5000/habitaciones/' + id)
    //     .then(response => response.json())
    //     .then(data => console.log(data));

    //conteo Habitacion
    fetch('http://127.0.0.1:5000/habitaciones/' + id)
            .then(response => response.json())
            .then(data => {
                if (estado_button == 1){
                    const conteoMas = 1;
                    Conteo[[data.habitacion._id]] = conteoMas;
                }
                else{
                    const conteoMenos = -1;
                    Conteo[[data.habitacion._id]] = conteoMenos;
                    }
                TotalConteo = TotalConteo + Conteo[[data.habitacion._id]];
                console.log(TotalConteo);
                // procesar fechas
                var fechaInicio = new Date(fecha_entrada).getTime();
                var fechaFin    = new Date(fecha_salida).getTime();
                var diff = fechaFin - fechaInicio;
                // console.log(diff/(1000*60*60*24) );
                document.getElementById("Conteo").innerHTML = TotalConteo + " Habitacion";
            });
    //

    // precio Total
    fetch('http://127.0.0.1:5000/habitaciones/' + id)
            .then(response => response.json())
            .then(data => {
                if (estado_button == 1){
                    const precioMas = (data.habitacion.precio);
                    Precio[[data.habitacion._id]] = parseInt(precioMas);
                    // console.log(Precio[[data.habitacion._id]]);
                }
                else{
                    const precioMenos = (data.habitacion.precio);
                    Precio[[data.habitacion._id]] = (parseInt(precioMenos)*-1);
                    // console.log(Precio[[data.habitacion._id]]);
                    }
                Suma = Suma + Precio[[data.habitacion._id]];
                console.log(Suma);
                // document.getElementById("Total_pagar").innerHTML = "$" + Suma;
                document.getElementById("Total_pagar").innerHTML = "$" + Intl.NumberFormat('de-DE', {style: 'decimal'}).format(Suma);
            });
    //
    fetch('http://127.0.0.1:5000/habitaciones/' + id)
            .then(response => response.json())
            .then(data => {
                if (estado_button == 1){
                    const json = ('{ "reserva": ' + '{ "user_id": ' + '"' + usuarioActivo + '"' + ', "habitacion_id": ' + '"' + data.habitacion._id + '"' + ', "fecha_entrada": ' + '"' + fecha_entrada + '"' + "," + ' "fecha_salida": ' + '"' + fecha_salida + '"' + " }" + ", " + '"estado_boton": ' + estado_button + " }");
                    Datos = JSON.parse(json);
                    console.log(Datos.reserva);
                    Vector[data.habitacion._id] = Datos.reserva;
                    Vector_post[data.habitacion._id] = Vector[data.habitacion._id];
                }
                else {
                    Datos = null;
                    Vector[data.habitacion._id] = Datos;
                    Vector_post[data.habitacion._id] = Vector[data.habitacion._id];
                    console.log(Datos);
                } 
            });
    // console.log(Vector);
    
     
     
    // var filtrados = Vector.filter(valor != null);
    // console.log(filtrados)
}


function ProcesarPago(){
    console.log("pague");
    for (var i = 0; i < Size_vector ; i++) {
        console.log("for")
        console.log(Vector_post[i])
        if (Vector_post[i] != null){
            console.log("if")
            fetch('http://127.0.0.1:5000/reservas', {
                method: 'POST',
                body: JSON.stringify(Vector_post[i]),
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                }
            })
            .then(function(response){ 
                return response.json()})
                .then(function(data)
                {console.log(data)
                }).catch(error => console.error('Error:', error)); 
                // console.log(Vector_post[i]);
            } else { console.log("else") }
        }
        Swal.fire({
            icon: 'success',
            title: 'Reserva Exitosa!',
            text: "De click en el boton OK",
            confirmButtonText: 'OK',
          }).then((result) => {
            if (result.isConfirmed) {
                location.reload()
            } 
          })
          
    }
