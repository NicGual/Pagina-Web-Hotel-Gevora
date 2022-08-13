const eliminar= document.querySelectorAll('.opciones')
const gesHab= document.getElementById('gesHab')
let inputGroup=document.querySelector('.buscarEspecifico')
let buscar = document.querySelector('.addButton3')





eliminar.forEach(element =>{
    element.addEventListener('click',()=>{
        const modalBody = element.querySelector('.modal-body')
        modalBody.addEventListener('click',()=>{
            
            delUser= modalBody.querySelector('.delUser')
            window.location.href = '/eliminar/' + delUser.getAttribute('idUser')
            
        })
    })
})

buscar.addEventListener('click',()=>{
    let inputValue=document.getElementById('inputBuscar')
    window.location.href = '#'+inputValue.value
    try{
        
        let usuario=document.getElementById(inputValue.value)
        let nombreTag=usuario.querySelector('.nombre')
        console.log(nombreTag)
        nombreTag.style.color='red'
        setTimeout(()=>{
            nombreTag.style.color='black'
        },700)
    }catch{
        window.alert('Usuario no encontrado')
        
    }
    

})




gesHab.addEventListener('click',()=>{
    window.location.href = "/superHabita";
})

