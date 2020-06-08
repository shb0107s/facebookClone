window.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector("#id_photo")
    const submit = document.querySelector('#submitBtn')
    const canvas = document.querySelector('#imageCanvas')
    let ctx = canvas.getContext('2d')

    function handleImage(){
        let fileList = fileInput.files
        let reader = new FileReader()

        submit.disabled = false

        reader.readAsDataURL(fileList[0])
        reader.onload = event => {
            let img = new Image()
            img.onload = () => {
                canvas.width = 100
                canvas.height = 100
                ctx.drawImage(img, 0, 0, 100, 100)

                submit.parentNode.style.display = 'block'
            }

            // 이미지 로딩 지시. 이미지 로딩이 완료될때 onload 호출
            img.src = event.target.result
        }
    }

    fileInput.addEventListener('change', handleImage)
})