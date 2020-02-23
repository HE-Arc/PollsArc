
let search_poll_input = document.getElementById("search_poll")

if(search_poll_input){
    let proposed_polls_input = document.getElementById("proposed_polls")
    search_poll_input.addEventListener("input", (e) => {
        fetch('searchPolls/' + encodeURI(e.data)).then((response) => {
            proposed_polls_input.innerHTML = ""
            response.json().then((data) => {
                data.polls.forEach(element => {
                    console.log(element.id);
                    
                    proposed_polls_input.innerHTML += "<div class='proposed_poll_display'><strong>Name : "+ element.name +"</strong><br> descrption : "+ element.description +"</div>"
              });
            })
        })
    })
}