document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#search').onsubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const urlData = new URLSearchParams(formData);
        fetch(`/properties/?${urlData}`)
        .then(response => response.json())
        .then(data => {

        })
    }
})