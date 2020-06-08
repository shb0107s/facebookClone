window.addEventListener('DOMContentLoaded', () => {
    const bell = document.querySelector('.bell')
    const leftBox = document.querySelector('.left_box')
    const rightBox = document.querySelector('.right_box')
    const feed = document.querySelector('#contents_container')
    const txt = document.querySelector('#comment37')

    leftBox.style.right = `${innerWidth*0.5 + 430}px`
    rightBox.style.left = `${innerWidth*0.5 + 90}px`

    function resizeFunc(){
        leftBox.style.right = `${innerWidth*0.5 + 430}px`
        rightBox.style.left = `${innerWidth*0.5 + 90}px`
    }
    function notification(){
        this.classList.toggle('on')
    }
    function addMorePostAjax(data){
        feed.insertAdjacentHTML('beforeend', data)
    }
    function callMorePostAjax(pageValue){
        if(pageValue > 5) return

        $.ajax({
            type: 'POST',
            url: 'data/post.html',
            data: pageValue,
            dataType: 'json',
            success: addMorePostAjax,
            error: () => {
                alert('문제가 발생했습니다')
            }
        })

    }
    function scrollFunc() {
        let documentHeight = document.body.scrollHeight
        let scrollHeight = pageYOffset + innerHeight

        if(scrollHeight >= documentHeight){
            let pager = document.querySelector('#page')

            // querySelector는 살아있는 컬렉션을 반환하지 않으므로 다시 찾아서 value를 반환한다.
            let pageValue = document.querySelector('#page').value

            pager.value = parseInt(pageValue) + 1

            callMorePostAjax(pageValue)

            if(pageValue > 5) return
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
        }else if(elem.matches('[data-name="send"]')){
            $.ajax({
                type: 'POST',
                url: 'data/comment.html',
                data: '',
                dataType: 'html',
                success: (res) => {
                    document.querySelector('.comment_container').insertAdjacentHTML('beforeend', res)
                },
                error: () => {
                    alert('로그인이 필요합니다.')
                    window.location.replace('https://www.naver.com')
                }
            })
            // 댓글 작성창 비우기
            txt.value = ''
        }else if(elem.matches('[data-name="delete"]')){
            if(confirm("정말 삭제하시겠습니까?") === true){
                $.ajax({
                    type: 'POST',
                    url: 'data/delete.json',
                    data: '',
                    dataType: 'json',
                    success: (res) => {
                        if(res.status){
                            let comt = document.querySelector('.comment-37')
                            comt.remove()
                        }
                    },
                    error: () => {

                    }
                })
            }
        }
    }

    bell.addEventListener('click', notification)
    feed.addEventListener('click', delegation)

    window.addEventListener('scroll', scrollFunc)
    window.addEventListener('resize', resizeFunc)
})