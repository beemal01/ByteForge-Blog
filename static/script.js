function showMessage(text, isSuccess = false){
    const divMessage = document.getElementById('message')
    if(divMessage){
        divMessage.textContent = text;
        divMessage.className = 'alert mb-3 ' + (isSuccess ? 'alert-success' : 'alert-danger');
        divMessage.classList.remove('d-none');
    }
}

async function signupFunc(){
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;

    const payload = {
        name:name,
        email:email,
        password:password,
    }
    const button = document.getElementById('btn');
    button.disabled = true;
    button.textContent = "Registering....";
    try{
        const response = await fetch('/api/signupview/', {
            method : "POST",
            headers : {
                "Content-Type": "application/json"
            },
            body : JSON.stringify(payload),
        });
        if (response.ok){
            const data = await response.json();
            showMessage("Register Successfull, Please check your mail.", true);
            localStorage.setItem('email', email);

            setTimeout(() => {
                window.location.href = '/otp/';
            }, 1000);
        }
        else{
            const errorData = await response.json();
            showMessage(errorData.message ||  "Registration failed. Please check your details.");
        }
        
    }
    catch (error) {
        showMessage("Network error. Please try again.");
    }
    finally{
        button.disabled = false;
        button.textContent = "Register";
    }
};


async function optUser() {
    const otp = document.getElementById('otp').value;
    const email = localStorage.getItem('email');

    const payload = {
        email:email,
        otp:otp,
    }

    const button = document.getElementById('btn');
    button.disabled = true;
    button.textContent = "Verifying...";

    try{
        const response = await fetch('/api/otpview/', {
            method : "POST",
            headers : {
                "Content-Type": "application/json"
            },
            body : JSON.stringify(payload),
        });
        
        if (response.ok){
            showMessage("OTP Successfully Verified...", true);
            setTimeout(() =>{
                window.location.href = "/signin/";
            }, 1000);
        }
        else{
            const msg = await response.json();
            showMessage(msg.message || "Please enter valid OTP!!!");
        };
    }
    catch (error) {
        showMessage("Network error. Please try again.");
    }
    finally{
        button.disabled = false;
        button.textContent = "Submit";
    }
};

async function logUser() {
    const email = document.getElementById('logEmail').value;
    const password = document.getElementById('logPassword').value;

    const payload = {
        email:email,
        password:password,
    }
    const button = document.getElementById('btn');
    button.disabled = true;
    button.textContent = "Signing In...";

    try{
        const response = await fetch('/api/loginview/', {
            method : "POST",
            headers : {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify(payload),
        });

        if (response.ok){
            const data = await response.json();
            localStorage.setItem('refresh', data.refresh);
            localStorage.setItem('access', data.access);
            if (data.User && data.User.name) {
                localStorage.setItem('name', data.User.name);
            }
            
            showMessage("Sign In Successfull", true);

            setTimeout(()=>{
                window.location.href = '/';
            }, 1000);
        }
        else{
            const msg = await response.json();
            showMessage(msg.message || "Invalid Credientials! Please, Try-again...");
        };
        
    }
    catch (error) {
        showMessage("Network error. Please try again.");
    }
    finally{
        button.disabled = false;
        button.textContent = "Sign In";
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const access = localStorage.getItem('access');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const logoutBtn = document.getElementById('logout');
    const createBtn = document.getElementById('create-btn');
    const displayBtn = document.getElementById('display-name');

    if (access && loginBtn && registerBtn && logoutBtn && createBtn && displayBtn) {
        loginBtn.style.display = 'none';
        registerBtn.style.display = 'none';
        createBtn.style.display = 'block';
        logoutBtn.style.display = 'block';
        const storedName = localStorage.getItem('name');
        if (storedName) {
            displayBtn.style.display = 'block';
            displayBtn.textContent = "Hey, " + storedName;
        }
    } else if (loginBtn) {
        loginBtn.style.display = 'block';
        registerBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (createBtn) createBtn.style.display = 'none';
        if (displayBtn) displayBtn.style.display = 'none';
    }
});

function logoutUser() {
    const refresh = localStorage.getItem('refresh');

    fetch('/api/logoutview/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({refresh}),
    }).finally(() => {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        localStorage.removeItem('name');
        window.location.href = '/';
    })
}

async function refreshAccessToken(){
    const refresh = localStorage.getItem('refresh');
    if(!refresh) return null;
    const response = await fetch('/api/token/refresh/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({refresh}),
    });
    if(response.ok){
        const data = await response.json();
        localStorage.setItem('access', data.access);
        return data.access;
    }
    return null;
}

async function submitPost() {
    const title = document.getElementById('title').value;
    const featured_image = document.getElementById('featured_image').files[0];
    const blog_post = quill.root.innerHTML;  

    if (!featured_image) {
        showMessage("Please select a featured image.");
        return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('featured_image', featured_image);
    formData.append('blog_body', blog_post); 

    const button = document.getElementById('btn');
    button.disabled = true;
    button.textContent = "Submitting...";

    let access = localStorage.getItem("access");
    let response = await fetch('/api/blogview/', {
        method : "POST",
        headers : {
            "Authorization": "Bearer " + access
        },
        body : formData,
    });

    if(response.status === 401){
        access = await refreshAccessToken();
        if(access){
            response = await fetch('/api/blogview/', {
                method : "POST",
                headers : {
                    "Authorization": "Bearer " + access
                },
                body : formData,
            });
        }
    }

    try{
        if (response.ok){
            showMessage("Successfully created post.", true);
            setTimeout(()=>{
                window.location.href = '/';
            }, 1000);
         }
         else{
            const msg = await response.json();
            showMessage(msg.message || "Failed to create post.");
         }
    }
    catch (error) {
        showMessage("Network error. Please try again.");
    }
    finally{
        button.disabled = false;
        button.textContent = "Submit";
    }
};



async function updatePost(slug) {
    const title = document.getElementById('title').value;
    const featured_image = document.getElementById('featured_image').files[0];
    const blog_body = quill.root.innerHTML;

    const formData = new FormData();
    formData.append('title', title);
    formData.append('blog_body', blog_body);
    if (featured_image) {
        formData.append('featured_image', featured_image);
    }

    const button = document.getElementById('btn');
    button.disabled = true;
    button.textContent = 'Updating...';

    let access = localStorage.getItem('access');
    let response = await fetch(`/api/blogdetails/${slug}/`, {
        method: 'PUT',
        headers: { 'Authorization': 'Bearer ' + access },
        body: formData,
    });

    if (response.ok) {
        showMessage('Successfully Updated Post.', true);
        window.location.href = `/${slug}/`;
    } else {
        const text = await response.text();
        showMessage('Error (' + response.status + '): ' + text);
        button.disabled = false;
        button.textContent = 'Update';
    }
}


async function deletePost(slug) {
    window._deleteSlug = slug;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

document.addEventListener('DOMContentLoaded', () => {
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', async () => {
            const slug = window._deleteSlug;
            if (!slug) return;

            const access = localStorage.getItem('access');
            const response = await fetch(`/api/blogdetails/${slug}/`, {
                method: 'DELETE',
                headers: { 'Authorization': 'Bearer ' + access }
            });

            const deleteModal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
            deleteModal.hide();

            if (response.ok) {
                showMessage('Post deleted successfully.', true);
                window.location.href = '/';
            } else {
                showMessage('Failed to delete post.', false);
            }
        });
    }
});
