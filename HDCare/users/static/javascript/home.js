const slideImges = document.querySelectorAll('.slider');
let currentCounter = 0 ;

slideImges[currentCounter].style.opacity = 1;

setInterval(nextImage , 3000);

function nextImage(){
    slideImges[currentCounter].style.zIndex = -2 ;
    const changeCounter = currentCounter ;

    setTimeout(()=>{
    slideImges[changeCounter].style.opacity = 0;
    }, 1000)

    currentCounter = (currentCounter + 1)% slideImges.length;
    slideImges[currentCounter].style.opacity = 1 ;
    slideImges[currentCounter].style.zIndex = -1 ;
}
