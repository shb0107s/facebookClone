window.addEventListener('DOMContentLoaded', () => {
    const bell = document.querySelector('.bell')

    function notification(){
        this.classList.toggle('on')
    }

    bell.addEventListener('click', notification)
})