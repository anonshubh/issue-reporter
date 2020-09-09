document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll('.upvote').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            // async call - todo
            let children = button.parentNode.childNodes;
            children[1].style.display = 'none';
            children[3].style.display = 'none';
            children[5].style.display = 'inline-block';
        }
    });
    document.querySelectorAll('.downvote').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            // async call - todo
            let children = button.parentNode.childNodes;
            children[1].style.display = 'none';
            children[3].style.display = 'none';
            children[7].style.display = 'inline-block';
        }
    });
    document.querySelectorAll('.upvoted').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            // async call - todo
            let children = button.parentNode.childNodes;
            children[1].style.display = 'inline-block';
            children[3].style.display = 'inline-block';
            children[5].style.display = 'none';
        }
    });
    document.querySelectorAll('.downvoted').forEach((button)=>{
        button.onclick = () => {
            let id_ = button.dataset.id;
            // async call - todo
            let children = button.parentNode.childNodes;
            children[1].style.display = 'inline-block';
            children[3].style.display = 'inline-block';
            children[7].style.display = 'none';
        }
    });
});