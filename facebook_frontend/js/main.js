window.addEventListener('DOMContentLoaded', () => {
    const bell = document.querySelector('.bell')
    const leftBox = document.querySelector('.left_box')
    const rightBox = document.querySelector('.right_box')
    const feed = document.querySelector('#contents_container')

    leftBox.style.right = `${innerWidth*0.5 + 430}px`
    rightBox.style.left = `${innerWidth*0.5 + 90}px`

    function resizeFunc(){
        leftBox.style.right = `${innerWidth*0.5 + 430}px`
        rightBox.style.left = `${innerWidth*0.5 + 90}px`
    }
    function notification(){
        this.classList.toggle('on')
    }
    function scrollFunc() {
        let documentHeight = document.body.scrollHeight
        let scrollHeight = pageYOffset + innerHeight

        if(scrollHeight >= documentHeight){
            // console.log(scrollHeight)
        }
    }
    function delegation(e){
        let elem = e.target

        while(!elem.getAttribute('data-name')){
            elem = elem.parentNode

            if(elem.nodeName === 'BODY'){
                elem = null
                return;
            }
        }

        if(elem.matches('[data-name="like"]')){
            // console.log('좋아요!')
            elem.classList.toggle('active')

            let pk = elem.getAttribute('data-name')
            $.ajax({
                type: 'POST',
                url: 'data/like.json',
                data: {pk},
                dataType: 'json',
                success: (response) => {
                    let likeCount = document.querySelector('#like-count-37')
                    likeCount.innerHTML = response.like_count
                },
                error: () => {
                    alert('로그인이 필요합니다.')
                    window.location.replace('https://www.naver.com')
                }

            })
        }else if(elem.matches('[data-name="more"]')){
            // console.log('more!!')
            elem.classList.toggle('active')
        }
    }

    bell.addEventListener('click', notification)
    feed.addEventListener('click', delegation)

    window.addEventListener('scroll', scrollFunc)
    window.addEventListener('resize', resizeFunc)
})