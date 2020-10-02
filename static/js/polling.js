var noPoll = 0;
var form = document.querySelector("#poll-form");
document.addEventListener("DOMContentLoaded",()=>{
    var button_position = 5;

    var x = document.createElement("OL");
    x.classList.add("plist");
    form.insertBefore(x,form.childNodes[button_position]);
    button_position++;

    form.insertBefore(add_textbox(),form.childNodes[button_position]);
    button_position++;
    form.insertBefore(add_button(),form.childNodes[button_position]);
    button_position++;
    
    let button = document.querySelector(".tbtn");
    button.onclick = () => {
        let val = document.querySelector(".tbox");
        add_poll(val.value);
        button_position++;
        val.value = '';
        return false;
    }

    document.addEventListener('click',()=>{
        document.querySelectorAll('.rmButton').forEach((rb)=>{
            rb.onclick = () =>{
                let rListId = `${rb.id}p`; 
                let listItem = document.getElementById(rListId);
                listItem.remove();

                let rInputId = `${rb.id}i`; 
                let inputItem = document.getElementById(rInputId);
                inputItem.remove();
                return false;
            }
        })
    })
        
    form.onsubmit = ()=>{
        let statement = document.querySelector("#id_statement").value;
        let data = new Object();
        data.statement = statement;
        data.option =  [];
        while(noPoll){
            let optionId = `${noPoll}i`
            try { 
                let optionVal = document.getElementById(optionId).value;
                data['option'].push(optionVal);
            } catch (error) {
                noPoll--;
                continue;
            }
            noPoll--;
        }
        const csrftoken = getCookie('csrftoken');
        fetch('/polling/new/',{
            method: "POST",
            headers:{
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data=>{
            console.log(data);
            window.location.replace("/polling/");
        })
        return false;
    }
   
});


function add_poll(text){
    let listElement = document.createElement("LI");
    let list = document.querySelector('.plist');
    listElement.innerHTML = text;
    noPoll++;
    listElement.id = `${noPoll}p`;
    listElement.classList.add("mt-2")
    
    let removeButton = document.createElement("button");
    removeButton.innerHTML = 'Remove';
    removeButton.id = noPoll;
    removeButton.classList.add("btn","btn-danger","btn-sm","ml-2","rmButton");

    listElement.appendChild(removeButton);
    list.appendChild(listElement);

    let pollInput = document.createElement("input");
    pollInput.type = 'hidden';
    pollInput.name = noPoll;
    pollInput.value = text;
    pollInput.id = `${noPoll}i`;
    form.appendChild(pollInput);
    return list;
}

function add_textbox(){
    let textbox = document.createElement('input');
    textbox.type = 'text'
    textbox.classList.add("tbox",'mb-2');
    return textbox;
}

function add_button(){
    let button = document.createElement('button');
    button.innerHTML = "Add";
    button.classList.add('btn','btn-success','btn-sm','ml-2','tbtn');
    return button;
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