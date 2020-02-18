document.getElementById("search_user").addEventListener("input", (e) => {
    fetch('http://127.0.0.1:8000/searchUsers/' + e.data)
        .then((response) => {
            response.json().then((data) => {
                document.gete
                
            })
        })
})