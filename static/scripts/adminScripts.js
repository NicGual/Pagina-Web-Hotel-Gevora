
function urlPaginas() {
    document.getElementsByName("pagina").forEach(
        (element, index) => element.addEventListener("click",
            function (event) {
                event.preventDefault()
                fetchUsuarios(index + 1)
                window.localStorage.setItem('paginaActual', index + 1)
            }
        ))
}

function urlPaginasHabitaciones(f) {
    document.getElementsByName("pagina").forEach(
        (element, index) => element.addEventListener("click",
            function (event) {
                event.preventDefault()
                f(index + 1)
                window.localStorage.setItem('paginaActualHabitaciones', index + 1)
            }
        ))
}

function agregarNotificacion(id, mensaje, tipo) {
    document.getElementById(id).insertAdjacentHTML('afterbegin',
        `<div class='alert alert-${tipo} alert-dismissible fade show' id='alert' role='alert'> ${mensaje} <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button></div>`)
}

async function fetchContent(url) {
    document.getElementById("ventanaContenido").remove()
    try {
        let response = await fetch(url)
        resultados = await response.text()
        document.getElementById("contenidoCuerpo").insertAdjacentHTML('beforeend', '<div id="ventanaContenido"></div>')
        document.getElementById("ventanaContenido").insertAdjacentHTML('beforeend', resultados)


    } catch (err) {
        document.getElementById("contenidoCuerpo").insertAdjacentHTML('beforeend', '<p class="d-flex justify-content-center">Algo salio mal, intente mas tarde</p>')

    }

}

async function gestionUsuarios(pagina) {
    const gestionHabitaciones = document.getElementById('gestionHabitaciones')
    const gestionUsuarios = document.getElementById('gestionUsuarios')
    window.localStorage.setItem('paginaActual', pagina)
    if (gestionHabitaciones.classList.contains("activado")) {
        gestionHabitaciones.classList.replace("activado", "desactivado")
    }
    gestionUsuarios.classList.replace("desactivado", "activado");

    await fetchUsuarios(pagina)
}

async function fetchUsuarios(pagina) {
    const usuarios = document.getElementById('listaUsuarios')
    const paginacion = document.getElementById('paginacion')
    if (usuarios) {
        usuarios.remove()
        paginacion.remove()
    }

    await fetchContent('http://127.0.0.1:5000/administrador/gestionar-usuarios/' + pagina)

    urlPaginas()

    paginaActual = window.localStorage.getItem('paginaActual')
    document.getElementById("pagina" + paginaActual).classList.add("active")

    document.getElementById("paginaAnterior").addEventListener('click', function (event) {
        event.preventDefault()
        fetchUsuarios(paginaActual - 1)
        window.localStorage.setItem('paginaActual', paginaActual - 1)
    })

    document.getElementById("paginaSiguiente").addEventListener('click', function (event) {
        event.preventDefault()
        fetchUsuarios(Number.parseInt(paginaActual) + 1)
        window.localStorage.setItem('paginaActual', Number.parseInt(paginaActual) + 1)
    })
    document.getElementById("crearUsuarioBoton").addEventListener("click", function (event) {
        event.preventDefault()
        crearUsuario()
        console.log(event.detail)
    });

    document.querySelectorAll(".userEdit").forEach(element => {
        element.addEventListener("click", e => {
            const id = e.target.getAttribute("id");
            editarUsuario(id)
        });
    });


}

async function crearUsuario() {

    let nombreUsuario = document.getElementById("nombreUsuario").value
    let correoUsuario = document.getElementById("correoUsuario").value
    let contrasenaUsuario = document.getElementById("contrasenaUsuario").value
    let tipoUsuario = document.getElementById("tipoUsuario").value
    const datos = {
        "nombre": nombreUsuario,
        "correo": correoUsuario,
        "contrasena": contrasenaUsuario,
        "tipoUsuario": tipoUsuario
    }
    url = 'http://127.0.0.1:5000/administrador/crear-usuario'

    requestOptions = {
        method: 'POST',
        body: JSON.stringify(datos),
        headers: {
            'Content-Type': 'application/json'
        }
    }

    try {
        let result = await fetch(url, requestOptions)
        if (result.ok) {
            document.getElementById("crearUsuarioForm").reset()
            agregarNotificacion("contenedorAlerta","Usuario creado exitosamente","success")
        } else {
            agregarNotificacion("contenedorAlerta","Algo ocurrio mal, el usuario no pudo ser creado", "danger")
        }
    } catch (err) {
        console.log(err)
    }

}

async function editarUsuario(id) {

    url = 'http://127.0.0.1:5000/administrador/editar-usuario/' + id

    await fetchContent(url)


    document.getElementById("guardarUsuario").addEventListener("click", function (e) {
        e.preventDefault()
        guardarUsuario(url)

    })


}

async function guardarUsuario(url) {

    let nombre = document.getElementById("nombreEditarUsuario").value
    let correo = document.getElementById("correoEditarUsuario").value

    datos = {
        "nombre": nombre,
        "correo": correo
    }

    requestOptions = {
        method: 'UPDATE',
        body: JSON.stringify(datos),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    
    if (!(nombre == '' || correo == "")) {

        try {
            let resultado = await fetch(url, requestOptions)

            if (resultado.ok) {
                console.log("usuario actualizado")
                agregarNotificacion("contenedorAlerta","Usuario actualizado exitosamente", "success")
            }
        }
        catch {
            console.log("algo salio mal")
            agregarNotificacion("contenedorAlerta","Algo salio mal, intentelo nuevamente","danger")
        }
    }
    else {
        agregarNotificacion("contenedorAlerta","Revise los campos ingresados, no se aceptan campos vacios", "danger")
    }
}





// Gestion de Habitaciones---------------------------------------------------------------------------------------------
async function gestionHabitaciones() {
    const gestionHabitaciones = document.getElementById('gestionHabitaciones')
    const gestionUsuarios = document.getElementById('gestionUsuarios')

    if (gestionUsuarios.classList.contains("activado")) {
        gestionUsuarios.classList.replace("activado", "desactivado");
    }
    gestionHabitaciones.classList.replace("desactivado", "activado");

    fetchHabitaciones("1")

}

async function fetchHabitaciones (pagina) {
    const habitaciones = document.getElementById('listaHabitaciones')
    const paginacion = document.getElementById('paginacion')
    if (habitaciones) {
        habitaciones.remove()
        paginacion.remove()
    }

    await fetchContent('http://127.0.0.1:5000/administrador/gestionar-habitaciones/' + pagina)
    
    urlPaginasHabitaciones(fetchHabitaciones)

    paginaActual = window.localStorage.getItem('paginaActualHabitaciones')
    document.getElementById("pagina" + paginaActual).classList.add("active")

    document.getElementById("paginaAnterior").addEventListener('click', function (event) {
        event.preventDefault()
        fetchHabitaciones(paginaActual - 1)
        window.localStorage.setItem('paginaActualHabitaciones', paginaActual - 1)
    })

    document.getElementById("paginaSiguiente").addEventListener('click', function (event) {
        event.preventDefault()
        fetchHabitaciones(Number.parseInt(paginaActual) + 1)
        window.localStorage.setItem('paginaActualHabitaciones', Number.parseInt(paginaActual) + 1)
    })

    document.getElementById('crearHabitacionBoton').addEventListener('click', crearHabitacion)

    const estado=document.querySelectorAll('.changeStatus')
    estado.forEach(element =>{
        element.addEventListener('click',()=>{
            let modalContent=document.getElementById('changeStatusHab')
            let myModal = new bootstrap.Modal(modalContent)
            myModal.show()
            let confirm= modalContent.querySelector('.confir')
            
            confirm.addEventListener('click',async ()=>{
                if(element.innerHTML == 'Ocupado'){
    
                    elementSt='libre'
                }else{
                    elementSt='ocupado'
                }
                
                url = 'http://127.0.0.1:5000/administrador/editar-estado-habitacion/'+ element.getAttribute('id') + '/' + elementSt
                requestOptions = {
                    method: 'UPDATE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
                await fetch(url,requestOptions)
                myModal.hide()
                gestionHabitaciones()
                
            })
            
            
        })
    })

}

async function crearHabitacion (e) {
    e.preventDefault()

    let descripcion = document.getElementById("descripcionHabitacion").value
    let precio = document.getElementById("precioHabitacion").value
    let id = document.getElementById("idHabitacion").value
    url = 'http://127.0.0.1:5000/administrador/crear-habitaciones'
    datos ={
        "descripcion": descripcion,
        "precio": precio,
        "id": id
    }
    requestOptions = {
        method: 'POST',
        body: JSON.stringify(datos),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    
    try {
        let result = await fetch(url, requestOptions)
        if (result.ok) {
            document.getElementById("crearHabitacionForm").reset()
            agregarNotificacion("contenedorAlerta","Habitacion creado exitosamente","success")
        } else {
            agregarNotificacion("contenedorAlerta","Algo ocurrio mal, el usuario no pudo ser creado", "danger")
        }
    } catch (err) {
        console.log(err)
    }

    if ((datos["descripcion"] || datos["precio"] || datos["id"]) == "") 
    {
        agregarNotificacion("contenedorAlerta","Todos los campos deben ser llenados", "danger")
    }



    console.log(datos)
}

async function editarHabitacion (idHabitacion) {

    
    descripcion = document.getElementById("descripcion"+idHabitacion).textContent
    precio = document.getElementById("precio"+idHabitacion).textContent
    id = document.getElementById("habitacion"+idHabitacion).textContent

    document.getElementById("editarDescripcion").value = descripcion
    document.getElementById("editarPrecio").value = precio
    document.getElementById("editarId").value = id

    document.getElementById("editarHabitacionBoton").addEventListener("click", function (e) {
        e.preventDefault()
        guardarCambios()})  
}

async function guardarCambios () {
   
    descripcionEditada = document.getElementById("editarDescripcion").value
    precioEditado = document.getElementById("editarPrecio").value 
    id = document.getElementById("editarId").value 
    console.log(descripcionEditada)
    datos = {
        "descripcion": descripcionEditada,
        "precio": precioEditado
    }

    url = '/administrador/editar-habitacion/' + id

    requestOptions = {
        method: 'UPDATE',
        body: JSON.stringify(datos),
        headers: {
            'Content-Type': 'application/json'
        }
    }

    if (!(descripcionEditada == '' || precioEditado == "")) {

        try {
            let resultado = await fetch(url, requestOptions)

            if (resultado.ok) {
                agregarNotificacion("contenedorAlertaEditar","habitacion actualizada exitosamente", "success")
            }
        }
        catch {
            agregarNotificacion("contenedorAlertaEditar","Algo salio mal, intentelo nuevamente","danger")
        }
    }
    else {
        agregarNotificacion("contenedorAlertaEditar","Revise los campos ingresados, no se aceptan campos vacios", "danger")
    }

}

function salir() {
    window.location.href = "/logout"
}