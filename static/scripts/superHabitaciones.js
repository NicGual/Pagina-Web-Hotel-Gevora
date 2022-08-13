const Descripcion=document.querySelectorAll('.descripcion');
const contPrecio=document.querySelectorAll('.contenidoPrecio');
const gesUs= document.getElementById('gesUs')
const stats=document.querySelectorAll('.changeStatus')
const buscar = document.querySelector('.addButton3')

function myFunction(id,desc){
    let modalContent=document.getElementById('changeDescHab')
    let modalBody = modalContent.querySelector('.modal-body')
    let textArea = modalBody.querySelector('.descripcionHab')
    let myModal = new bootstrap.Modal(modalContent)
    textArea.value = desc
    myModal.show()
    let confirmChange = modalContent.querySelector('.changeDesc')
    confirmChange.addEventListener('click',()=>{
        let descripcionOld= desc
        let descripcionNew= textArea.value
        window.location.href = '/habDescripcion/' + descripcionOld + '/' + descripcionNew 
    })
}

stats.forEach(element =>{
    element.addEventListener('click',()=>{
        let modalContent=document.getElementById('changeStatusHab')
        let myModal = new bootstrap.Modal(modalContent)
        myModal.show()
        
        let confirm= modalContent.querySelector('.confir')
        
        confirm.addEventListener('click',()=>{
            if(element.innerHTML == 'Ocupado'){

                elementSt='libre'
            }else{
                elementSt='ocupado'
            }
            
            window.location.href = '/habStatus/' + element.getAttribute('id') + '/' + elementSt
        })
        
        
    })
})

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

gesUs.addEventListener('click',()=>{
    window.location.href = "/SuperAdminUsers";
})



buscar.addEventListener('click',()=>{
    let inputValue=document.getElementById('inputHabitacion')
    window.location.href = '#'+inputValue.value
    try{
        
        let habitacion=document.getElementById(inputValue.value)
        let idTag=habitacion.querySelector('.nombre')
        
        idTag.style.color='red'
        setTimeout(()=>{
            idTag.style.color='black'
        },700)
    }catch{
        window.alert('Habitacion no encontrada')
        
    }
    

})