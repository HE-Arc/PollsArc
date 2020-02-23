let added_users = []

document.getElementById("search_user").addEventListener("input", (e) => {
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
                            
                            document.getElementById("selected_user_display").innerHTML += "<div class='user' id="+ ui.item.id +">"+ added_user +'<button type="button" class="close" onclick="removeUser(this)" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    
                            document.getElementById("selected_user").value = JSON.stringify(added_users.map((v,i) => {return v[0]}))
                        }                    
                    }
                })
            })
        })
})

function user_already_selected(users_array, user){
    return users_array.map((v,i) => {return v[1]}).includes(user)
}

let nb_prop = 0
let proposed_props = []

document.getElementById("add_proposition_button").addEventListener("click", (e) => {
    var prop = document.getElementById("add_proposition").value
    nb_prop++
    proposed_props.push(prop)

    document.getElementById("proposed_prop_display").innerHTML += "<p><strong>"+ nb_prop + ")</strong> "+ prop +"</p>"

    document.getElementById("proposed_prop").value = JSON.stringify(proposed_props)
})

function removeUser(element){
    let parent = element.parentNode

    let index_to_remove = 0;
    added_users.forEach( (elem, index) =>{
        if(elem == parent.id){
            index_to_remove = index
        }
    })
    added_users.splice(index_to_remove,1)
    parent.remove()
}

// Allow to don't send the search field on the server
$("#poll_form").submit(() => {
    $("#search_user").prop('disabled', true)
    return true
})