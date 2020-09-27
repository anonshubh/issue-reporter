//Toggle of Upvote and Downvote
document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll('.vote').forEach((div)=>{
        let id_ = div.dataset.id;
        const data_ = {id:id_};
        const csrftoken = getCookie('csrftoken');
        let child = div.childNodes; 
        fetch('/get-vote/',{
            method: "POST",
            headers:{
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data_),
        })
        .then(response => response.json())
        .then(data=>{
            const type = data.type;
            if(type=='none'){
                child[1].style.display = 'inline-block';
                child[3].style.display = 'inline-block';
            }
            else if(type=='upvoted'){
                child[5].style.display = 'inline-block';
            }
            else if(type=='downvoted'){
                child[7].style.display = 'inline-block';
            }
        })
    });

    document.querySelectorAll('.upvote').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            const data_ = {id:id_,type:'upvote'};
            voteUpdateApiCall(data_);
            let children = button.parentNode.childNodes;
            children[1].style.display = 'none';
            children[3].style.display = 'none';
            children[5].style.display = 'inline-block';
        }
    });
    document.querySelectorAll('.downvote').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            const data_ = {id:id_,type:'downvote'};
            voteUpdateApiCall(data_);
            let children = button.parentNode.childNodes;
            children[1].style.display = 'none';
            children[3].style.display = 'none';
            children[7].style.display = 'inline-block';
        }
    });
    document.querySelectorAll('.upvoted').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            const data_ = {id:id_,type:'upvoted'};
            voteUpdateApiCall(data_);
            let children = button.parentNode.childNodes;
            children[1].style.display = 'inline-block';
            children[3].style.display = 'inline-block';
            children[5].style.display = 'none';
        }
    });
    document.querySelectorAll('.downvoted').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            const data_ = {id:id_,type:'downvoted'};
            voteUpdateApiCall(data_);
            let children = button.parentNode.childNodes;
            children[1].style.display = 'inline-block';
            children[3].style.display = 'inline-block';
            children[7].style.display = 'none';
        }
    });
});


function voteUpdateApiCall(data_){
    const csrftoken = getCookie('csrftoken');
    fetch('/update-vote/',{
        method: "POST",
        headers:{
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(data_),
    })
    .then(response => response.json())
    .then(data=>{
        console.log(data);
    })
}

// Ref: https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//Display of Problem-Statements 
document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll(".statement").forEach((button)=>{
        button.onclick = () =>{
            let statementId = button.id;
            let answerId = `a${statementId.slice(1)}`;
            document.querySelector(`#${statementId}`).style.display = 'none';
            document.querySelector(`#${answerId}`).style.display = 'block';
        }
    })

    document.querySelectorAll(".answer").forEach((button)=>{
        button.onclick = () =>{
            let answerId = button.id;
            let statementId = `q${answerId.slice(1)}`;
            document.querySelector(`#${answerId}`).style.display = 'none';
            document.querySelector(`#${statementId}`).style.display = 'block';
        }
    })
})