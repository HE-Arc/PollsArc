let added_users = []

document.getElementById("search_user").addEventListener("input", (e) => {
    fetch('http://127.0.0.1:8000/searchUsers/' + encodeURI(e.data))
        .then((response) => {
            response.json().then((data) => {
                //document.getElementById("add_user").disabled= true
                user_to_display = [];
                for(let i = 0; i < data.users.length; i++){
                    user_to_display.push(data.users[i].pseudo)
                }
                $("#search_user").autocomplete({
                    source: data.users,
                    select: function(e, ui){

                        let added_user = ui.item.label
                        if(!added_users.includes(added_user)){
                            added_users.push(added_user)
                            document.getElementById("selected_user_display").innerHTML += "<p>"+ added_user +"</p>"
    
                            /*var input = document.createElement("input");
                            input.setAttribute("type", "hidden");
                            input.setAttribute("name", "users[]");
                            input.setAttribute("value", ui.item.id);
    
                            document.getElementById("poll_form").append(input)*/
                            document.getElementById("selected_user").value = JSON.stringify(added_users)
                        }                    
                    }
                })
                /*let user_to_add = document.getElementById("search_user").value
                if(user_to_display.includes(user_to_add) && !added_users.includes(user_to_add)){
                    document.getElementById("add_user").disabled = false
                }*/
            })
        })
})

/*document.getElementById("add_user").addEventListener("click", (e) =>{

    let added_user = document.getElementById("search_user").value
    added_users.push(added_user)
    selected_user.innerHTML += "<p>"+ added_user +"</p>"

    var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "users[]");
    input.setAttribute("value", added_user);

    document.getElementById("poll_form").append(input)
    document.getElementById("add_user").disabled = true
})*/

let nb_prop = 0
let proposed_props = []

document.getElementById("add_proposition_button").addEventListener("click", (e) => {
    var prop = document.getElementById("add_proposition").value
    nb_prop++
    proposed_props.push(prop)

    document.getElementById("proposed_prop_display").innerHTML += "<p><strong>"+ nb_prop + ")</strong> "+ prop +"</p>"

    document.getElementById("proposed_prop").value = JSON.stringify(proposed_props)
})