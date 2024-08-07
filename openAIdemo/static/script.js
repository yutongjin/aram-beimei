// static/script.js
function moveCard(card) {
    const targetContainer = document.getElementById('movedContainer');

    if (targetContainer) {
        targetContainer.appendChild(card); // Move the card to the new container
    } else {
        console.error('Target container not found');
    }
    console.log(card.textContent)
    fetch('add_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Django CSRF token for security
        },
        body: JSON.stringify({ item_text: card.textContent })
    })
    .then(response =>  console.log("123"))
    .catch(error => console.error(error));
}

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}