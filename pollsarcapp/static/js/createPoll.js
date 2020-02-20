let added_users = []

document.getElementById("search_user").addEventListener("input", (e) => {
    fetch('http://127.0.0.1:8000/searchUsers/' + e.data)
        .then((response) => {
            response.json().then((data) => {
                /*user_to_display = [];
                for(let i = 0; i < data.users.length; i++){
                    user_to_display.push(data.users[i].pseudo)
                }
                $("#search_user").autocomplete({
                    source: user_to_display
                })
                let user_to_add = document.getElementById("search_user").value
                if(user_to_display.includes(user_to_add) && !added_users.includes(user_to_add)){
                    document.getElementById("add_user").disabled = false;
                }*/
                
            })
        })
})

$(document).ready(function() { 

    var sampleArray = [{id:0,text:'enhancement'}, {id:1,text:'bug'}
                       ,{id:2,text:'duplicate'},{id:3,text:'invalid'}
                       ,{id:4,text:'wontfix'}];

    $("#search_user").select2({ data: sampleArray });

});

/*document.getElementById("add_user").addEventListener("click", (e) =>{

    let added_user = document.getElementById("search_user").value
    added_users.push(added_user)
    selected_user.innerHTML += "<p>"+ added_user +"</p>"
})

document.getElementById("add_proposition_button").addEventListener("click", (e) =>{

})*/