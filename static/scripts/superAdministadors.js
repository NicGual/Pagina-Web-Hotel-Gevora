const eliminar= document.querySelectorAll('.opciones')


const eliminarPersona = (elemento)=>{
    try{
        let advertencia= document.querySelector('.advertencia')
        advertencia.remove()

    }catch{
        console.log('no hay elemento')
    }
    document.body.style.backgroundColor = "#dedede";
    document.body.style.opacity = " 0.7";
    let parent=elemento.parentElement;
    let nombre = parent.querySelector('.nombre').innerText
    let advertencia= document.createElement('div')
    advertencia.classList.add('advertencia')
    let icon = document.createElement('i')
    icon.addEventListener('click',()=>{
        advertencia.remove()
        document.body.style.backgroundColor = "var(--bs-body-bg)";
        document.body.style.opacity = "1";

    })
    icon.classList.add('fa','fa-window-close','cerrar')
    advertencia.appendChild(icon)
    let p= document.createElement('p')
    p.innerText=`Está seguro que desea eliminar el usuario: ${nombre}`
    advertencia.appendChild(p)
    let div= document.createElement('div')
    let buttonCancelar= document.createElement('button')
    let buttonAceptar=document.createElement('button')
    buttonAceptar.classList.add('aceptar')
    buttonCancelar.classList.add('cancelar')
    buttonAceptar.innerText='Aceptar'
    buttonCancelar.innerText='Cancelar'
    buttonCancelar.addEventListener('click',()=>{
        advertencia.remove()
        document.body.style.backgroundColor = "var(--bs-body-bg)";
        document.body.style.opacity = "1";

    })
    buttonAceptar.addEventListener('click',()=>{
        
        advertencia.innerHTML='<h4>Usuario Eliminado satisfactoriamente</h4>'
        setTimeout(()=>{
            advertencia.remove()
            document.body.style.backgroundColor = "var(--bs-body-bg)";
            document.body.style.opacity = "1";
        },1000)
    })
    div.appendChild(buttonCancelar)
    div.appendChild(buttonAceptar)
    advertencia.appendChild(div)
    let content=document.querySelector('.content')
    
    content.appendChild(advertencia)

    
    


}

for(let i=0;i<eliminar.length;i++){
        boton=eliminar[i].querySelector('.eliminar')
        boton.addEventListener('click',()=>{
            eliminarPersona(eliminar[i])
        })
}