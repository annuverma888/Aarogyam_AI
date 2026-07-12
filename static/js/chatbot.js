const button = document.getElementById("chatButton");

const windowBox = document.getElementById("chatWindow");

const closeBtn = document.getElementById("closeChat");

const sendBtn = document.getElementById("sendBtn");

const chatBody = document.getElementById("chatBody");

button.onclick = () => {

    windowBox.style.display = "flex";

}

closeBtn.onclick = () => {

    windowBox.style.display = "none";

}

sendBtn.onclick = sendMessage;

document.getElementById("chatInput").addEventListener("keypress", function(e){

    if(e.key=="Enter"){

        sendMessage();

    }

});

function sendMessage(){

    let input=document.getElementById("chatInput");

    let message=input.value.trim();

    if(message=="") return;

    chatBody.innerHTML+=`

    <div class="user-message">

    ${message}

    </div>

    `;

    fetch("/chat",{

        method:"POST",

        headers:{

            "Content-Type":"application/x-www-form-urlencoded"

        },

        body:"message="+encodeURIComponent(message)

    })

    .then(res=>res.json())

    .then(data=>{

        chatBody.innerHTML+=`

        <div class="bot-message">

        ${data.reply}

        </div>

        `;

        chatBody.scrollTop=chatBody.scrollHeight;

    });

    input.value="";

}