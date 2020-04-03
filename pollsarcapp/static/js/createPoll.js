let addedUsers = []; //contains the invited user

let searchUserInput = document.getElementById("search-user");

if (searchUserInput) {
    // Makes a GET query to get users from the user search
    searchUserInput.addEventListener("input", (e) => {
        fetch('search_users/' + encodeURI(e.data)).then((response) => {
            response.json().then((data) => {

                // This array contains users from the GET research
                userToDisplay = [];
                for (let i = 0; i < data.users.length; i++) {
                    userToDisplay.push(data.users[i].pseudo);
                }

                $("#search-user").autocomplete({
                    source: data.users,
                    select: function (e, ui) {

                        let addedUser = ui.item.label;

                        // if the user isn't already in the invited list, add the user to the invited user array and display on the page
                        if (!userAlreadySelected(addedUsers, addedUser)) {
                            addedUsers.push([ui.item.id, addedUser]);
                            document.getElementById("selected-user-display").innerHTML += "<div class='user' id=user-" + ui.item.id + ">" + addedUser + '<button type="button" class="close" onclick="removeUser(this)" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';
                            document.getElementById("selected-user").value = JSON.stringify(addedUsers.map((v, i) => { return v[0]; }));
                        }
                    }
                });
            });
        });
    });
}

let isPrivateCheckbox = document.getElementById('is-private');

// Allow to remove the user search field if the private checkbox isn't checked, othwersiw display the search field
if (isPrivateCheckbox) {
    isPrivateCheckbox.addEventListener('change', function (e) {
        let searchGroup = document.getElementById('search-user-group');

        if (isPrivateCheckbox.checked) {
            searchGroup.style.display = 'block';
        } else {
            addedUsers = [];
            searchGroup.style.display = 'none';
        }
    });
}

//Return a boolean tha indicated if the user is already present in the invited user list
function userAlreadySelected(usersArray, user) {
    return usersArray.map((v, i) => { return v[1]; }).includes(user);
}

// remove a user from the page and the array
function removeUser(element) {
    let parent = element.parentNode;

    let indexToRemove = 0;
    addedUsers.forEach((elem, index) => {
        if ("user-" + elem === parent.id) {
            indexToRemove = index;
        }
    });
    addedUsers.splice(indexToRemove, 1);
    parent.remove();
}

let nbProp = 0; // index of the current proposition
let proposedProps = []; // array that contain the proposition

let propButton = document.getElementById("add-proposition-button"); // proposition button

// if the proposition exist, add a proposition
if (propButton) {
    propButton.addEventListener("click", (e) => {
        addProposition();
    });
}

// Add a proposition on the page and on the propositon array
function addProposition() {
    let propInput = document.getElementById("add-proposition");
    let prop = propInput.value;

    //if the proposition begin by a number, interupt the function
    if (prop == "" || prop.match(/^\d/))
        return;

    propInput.value = "";
    propInput.focus();

    nbProp++;
    proposedProps.push(prop);

    document.getElementById("proposed-prop-display").innerHTML += "<div id='" + prop + "'><strong>" + nbProp + ")</strong> " + prop + '<button type="button" class="close" onclick="removeProp(this)" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';
    document.getElementById("proposed-prop").value = JSON.stringify(proposedProps);
}

// Remove a added propositon on the page and from the array
function removeProp(element) {
    let parent = element.parentNode;

    var index = proposedProps.indexOf(parent.id);
    if (index !== -1) proposedProps.splice(index, 1);

    parent.remove();
}

//Check if minimum a proposition is filled
$("#poll-form").submit(() => {
    if (proposed_props.length == 0) {
        alert("You must enter propositions ! ");
        return false;
    } else {
        // Allow to don't send the search field on the server
        $("#search-user").prop('disabled', true);
        return true;
    }
    return true;
});

// Prevent from sending the form from the addProposition field
$("#add-proposition").keypress(function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        addProposition();
    }
});