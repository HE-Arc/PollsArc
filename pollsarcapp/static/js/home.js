
let searchPollInput = document.getElementById("search-poll")

if(searchPollInput){
    let proposedPollsInput = document.getElementById("proposed-polls")
    searchPollInput.addEventListener("input", (e) => {
        fetch('search_polls/' + encodeURI(e.data)).then((response) => {
            proposedPollsInput.innerHTML = ""
            response.json().then((data) => {
                data.polls.forEach(element => {
                    console.log(element.id);
                    
                    proposedPollsInput.innerHTML += "<div class='proposed-poll-display'><a href='poll/"+ element.id +"'><strong>Name : "+ element.name +"</strong><br> descrption : "+ element.description +"</a></div>"
              });
            })
        })
    })
}