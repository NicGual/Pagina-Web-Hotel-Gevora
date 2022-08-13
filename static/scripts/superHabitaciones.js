const Descripcion=document.querySelectorAll('.descripcion');
const contPrecio=document.querySelectorAll('.contenidoPrecio');


const editarDescripcion=(i)=>{
    let h4= i.parentElement.parentElement

    try{
        let advertencia= document.querySelector('.editDescripcion')
        advertencia.remove()

    }catch{
        console.log('no hay elemento')
    }
    document.body.style.backgroundColor = "#dedede";
    document.body.style.opacity = " 0.7";
    console.log(h4.innerText)
    let divCont= document.createElement('div')
    divCont.classList.add('editDescripcion')
    let h3ha=document.createElement('h3')
    let h3de=document.createElement('h3')
    h3ha.classList.add('ha')
    h3ha.innerHTML='Habitacion 1 <span><i class="fa fa-window-close cerrar"></i></span>'
    h3de.classList.add('de')
    h3de.innerText='Descripcion'
    divCont.appendChild(h3ha)
    divCont.appendChild(h3de)

    let divEdit= document.createElement('div')
    divEdit.classList.add('contEditDescripcion')
    let p= document.createElement('p')
    p.innerText=h4.innerText
    divEdit.appendChild(p)
    divCont.appendChild(divEdit)
    let save=document.createElement('div')
    save.classList.add('saveCont')
    let btn=document.createElement('button')
    btn.classList.add('guardar','mt-2')
    btn.innerText='Guardar'
    save.appendChild(btn)
    divCont.appendChild(save)

    const content= document.querySelector('.content')

    content.appendChild(divCont)

    const cerrar=divCont.querySelector('.cerrar')
    cerrar.addEventListener('click',()=>{
        let advertencia= document.querySelector('.editDescripcion')
        advertencia.remove()
        document.body.style.backgroundColor = "var(--bs-body-bg)";
        document.body.style.opacity = "1";
    })
}


Descripcion.forEach((i)=>{
    i.addEventListener('click',()=>{
        editarDescripcion(i)
    })
})

contPrecio.forEach((i)=>{
    i.addEventListener('click',()=>{
        console.log('editar precio')
    })
})