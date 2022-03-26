
const form = document.getElementById("loginForm");
const error= document.getElementById("messageError");

form.addEventListener('submit', async (e)=> {
    e.preventDefault();
    console.log(e.target);
    const username = e.target[0].value;
    const password = e.target[1].value;
    const confirm = e.target[2]?.value === "Login" ? null : e.target[2].value
    console.log(e.target[3]?.value ? "Signup submit": "Login submit");

    if (confirm) {
        const data = {username: username, password: password, confirm: confirm};
        const response = await fetch('/register/', {
            method: 'POST',
            body: JSON.stringify(data),
        })
        const respuesta = await response.json();
        console.log(respuesta);
        if (respuesta?.error){
            error.innerHTML = `An error ocurred: ${respuesta.error}`;
            error.style.display = 'block';
        } else {
            error.style.display = 'block';
            error.style.color = 'green'
            error.innerHTML = `User saved successfully. You can now login.`
        }
    }

    else {
        const data = {username: username, password: password};
        console.log(data);
        const response = await fetch('/login/', {
            method: 'POST',
            body: JSON.stringify(data),
        })
        console.log(response);
        
        if (response?.redirected){
            error.style.display = 'none';
            setTimeout(()=> {
                window.location.href = response.url
            }, 2000)
        } else {
            const respuesta = await response.json()
            error.innerHTML = `An error ocurred: ${respuesta.error}`;
            error.style.display = 'block';
        }
    }
})