let added_users = []

let search_user_input = document.getElementById("search_user")

if(search_user_input){
    search_user_input.addEventListener("input", (e) => {
        fetch('searchUsers/' + encodeURI(e.data)).then((response) => {
            response.json().then((data) => {
                user_to_display = [];
                for(let i = 0; i < data.users.length; i++){
                    user_to_display.push(data.users[i].pseudo)
                }
    
                $("#search_user").autocomplete({
                    source: data.users,
                    select: function(e, ui){
    
                        let added_user = ui.item.label
                            if(!user_already_selected(added_users, added_user)){
                                added_users.push([ui.item.id, added_user])
                                
                                document.getElementById("selected_user_display").innerHTML += "<div class='user' id=user_"+ ui.item.id +">"+ added_user +'<button type="button" class="close" onclick="removeUser(this)" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
        
                                document.getElementById("selected_user").value = JSON.stringify(added_users.map((v,i) => {return v[0]}))
                            }                    
                        }
                    })
                })
            })
    })
}

function user_already_selected(users_array, user){
    return users_array.map((v,i) => {return v[1]}).includes(user)
}

function removeUser(element){
    let parent = element.parentNode

    let index_to_remove = 0;
    added_users.forEach( (elem, index) =>{
        if("user_" + elem === parent.id){
            index_to_remove = index
        }
    })
    added_users.splice(index_to_remove,1)
    parent.remove()
}

let nb_prop = 0
let proposed_props = []

let prop_button = document.getElementById("add_proposition_button")

if(prop_button){
    prop_button.addEventListener("click", (e) => {
        addProposition();
    })
}

function addProposition(){
    let prop_input = document.getElementById("add_proposition")
    let prop = prop_input.value

    if (prop == "")
        return;

    prop_input.value = ""
    prop_input.focus()

    nb_prop++
    proposed_props.push(prop)

    //document.getElementById("proposed_prop_display").innerHTML += "<span><strong>"+ nb_prop + ")</strong> "+ prop +"</span>"
    document.getElementById("proposed_prop_display").innerHTML += "<div id='prop_'" + nb_prop + "><strong>"+ nb_prop + ")</strong> "+ prop +'<button type="button" class="close" onclick="removeProp(this)" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    document.getElementById("proposed_prop").value = JSON.stringify(proposed_props)
}

function removeProp(element){
    let parent = element.parentNode

    let index_to_remove = 0;
    proposed_props.forEach( (elem, index) =>{
        if("prop_" + elem === parent.id){
            index_to_remove = index
        }
    })
    proposed_props.splice(index_to_remove,1)
    parent.remove()
}


// Allow to don't send the search field on the server
$("#poll_form").submit(() => {
    $("#search_user").prop('disabled', true)
    return true
})

// Prevent from sending the form from the addProposition field
$("#add_proposition").keypress(function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        addProposition();
    }
});