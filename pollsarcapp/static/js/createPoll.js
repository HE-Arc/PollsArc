let addedUsers = []

let searchUserInput = document.getElementById("search-user")

if(searchUserInput){
    searchUserInput.addEventListener("input", (e) => {
        fetch('search_users/' + encodeURI(e.data)).then((response) => {
            response.json().then((data) => {
                userToDisplay = [];
                for(let i = 0; i < data.users.length; i++){
                    userToDisplay.push(data.users[i].pseudo)
                }
    
                $("#search-user").autocomplete({
                    source: data.users,
                    select: function(e, ui){
    
                        let addedUser = ui.item.label
                            if(!userAlreadySelected(addedUsers, addedUser)){
                                addedUsers.push([ui.item.id, addedUser])
                                
                                document.getElementById("selected-user-display").innerHTML += "<div class='user' id=user-"+ ui.item.id +">"+ addedUser +'<button type="button" class="close" onclick="removeUser(this)" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
                                document.getElementById("selected-user").value = JSON.stringify(addedUsers.map((v,i) => {return v[0]}))
                            }                    
                        }
                    })
                })
            })
    })
}

let isPrivateCheckbox = document.getElementById('is-private')

if(isPrivateCheckbox)
{
    isPrivateCheckbox.addEventListener('change', function(e) {
        let searchGroup = document.getElementById('search-user-group')
        
        if(isPrivateCheckbox.checked){
            searchGroup.style.display = 'block'
        }else {
            addedUsers = []
            searchGroup.style.display = 'none'
        }
    })
}

function userAlreadySelected(usersArray, user){
    return usersArray.map((v,i) => {return v[1]}).includes(user)
}

function removeUser(element){
    let parent = element.parentNode

    let indexToRemove = 0;
    addedUsers.forEach( (elem, index) =>{
        if("user-" + elem === parent.id){
            indexToRemove = index
        }
    })
    addedUsers.splice(indexToRemove,1)
    parent.remove()
}

let nbProp = 0
let proposedProps = []

let propButton = document.getElementById("add-proposition-button")

if(propButton){
    propButton.addEventListener("click", (e) => {
        addProposition();
    })
}

function addProposition(){
    let propInput = document.getElementById("add-proposition")
    let prop = propInput.value

    if (prop == "" || prop.match(/^\d/))
        return;

    propInput.value = ""
    propInput.focus()

    nbProp++
    proposedProps.push(prop)

    document.getElementById("proposed-prop-display").innerHTML += "<div id='"+ prop +"'><strong>"+ nbProp + ")</strong> "+ prop +'<button type="button" class="close" onclick="removeProp(this)" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
    document.getElementById("proposed-prop").value = JSON.stringify(proposedProps)
}

function removeProp(element){
    let parent = element.parentNode

    var index = proposedProps.indexOf(parent.id);
    if (index !== -1) proposedProps.splice(index, 1);

    parent.remove()
}


// Allow to don't send the search field on the server
$("#poll-form").submit(() => {
    $("#search-user").prop('disabled', true)
    return true
})

// Prevent from sending the form from the addProposition field
$("#add-proposition").keypress(function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        addProposition();
    }
});