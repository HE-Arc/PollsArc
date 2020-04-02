
let searchPollInput = document.getElementById("search-poll")

if(searchPollInput){
    let proposedPollsInput = document.getElementById("proposed-polls")
    // Makes a GET query to get polls from the user research
    searchPollInput.addEventListener("input", (e) => {
        fetch('search_polls/' + encodeURI(e.data)).then((response) => {
            proposedPollsInput.innerHTML = ""
            response.json().then((data) => {
                data.polls.forEach(element => {
                    console.log(element.id);
                    
                    //display the poll on the page
                    proposedPollsInput.innerHTML += "<div class='proposed-poll-display'><a href='poll/"+ element.id +"'><strong>Name : "+ element.name +"</strong><br> descrption : "+ element.description +"</a></div>"
              });
            })
        })
    })
}