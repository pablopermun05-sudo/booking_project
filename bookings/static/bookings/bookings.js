const MEDIA_URL = "/media/";
const titleLimit = 50;
const descriptionLimit = 160;
let lastProperty;
let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    let pageNumber = 1;

    // Creating the observers
    let observerInitial = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                pageNumber++;
                loadProperties(true);
            }
        });
    }, {
        rootMargin: '0px 0px 0px 0px',
        threshold: 0.5
    });

    let observerSearched = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                pageNumber++;
                loadProperties(false);
            }
        });
    }, {
        rootMargin: '0px 0px 0px 0px',
        threshold: 0.5
    });

    const propertiesOnScreen = document.querySelectorAll('.initial-property');
    if (propertiesOnScreen.length > 0) {
        lastProperty = propertiesOnScreen[propertiesOnScreen.length - 1];
        observerInitial.observe(lastProperty);
    }

    document.querySelector('#search').onsubmit = (event) => {
        event.preventDefault();
        pageNumber = 1;
        observerInitial.unobserve(lastProperty);
        observerSearched.unobserve(lastProperty);
        loadProperties(false);
    }

    function loadProperties(initial) {
        const initialProperties = document.querySelector('#initial-properties');
        const searchedProperties = document.querySelector('#searched-properties');
        const h2properties = document.querySelector('#h2Index');

        let urlData;

        if(isLoading) {
            return;
        } else {
            isLoading = true;
        }

        if (initial) {
            urlData = `page=${pageNumber}`;
        } else {
            const formData = new FormData(document.querySelector('#search'));
            urlData = new URLSearchParams(formData);
            urlData.append('page', pageNumber);
        }

        const alertDiv = document.querySelector('#alert-form');

        fetch(`/properties/?${urlData}`)
            .then(response => {
                if (!response.ok) {
                    // Extracting JSON error details before throwing to the catch block.
                    return response.json().then(err => { throw err; });
                }
                if (pageNumber == 1) {
                    alertDiv.style.display = 'none';
                }
                return response.json();
            })
            .then(properties => {

                if (pageNumber == 1) {
                    if (initial) {
                        h2properties.textContent = 'Viviendas Disponibles:';
                        searchedProperties.textContent = '';
                        searchedProperties.className = "";
                    } else {
                        h2properties.textContent = 'Viviendas relacionadas con tu búsqueda:';
                        initialProperties.textContent = '';
                    }

                    if (properties.length == 0) {
                        searchedProperties.textContent = 'No se encontraron resultados.';
                        searchedProperties.classList.add("text-center", "mt-5", "fw-semibold", "fs-3", "text-white", "notResultsFound");
                    }
                }

                properties.forEach(property => showProperty(property, initial));

                if (lastProperty && initial) {
                    observerInitial.unobserve(lastProperty);
                } else if (lastProperty) {
                    observerSearched.unobserve(lastProperty);
                }

                // Calling Observer to pay attetion when the las property is on the viewport
                const propertiesOnScreen = document.querySelectorAll('.property');
                lastProperty = propertiesOnScreen[propertiesOnScreen.length - 1];

                if (initial) {
                    observerInitial.observe(lastProperty);
                } else {
                    observerSearched.observe(lastProperty);
                }

            })
            .catch(error => {
                alertDiv.textContent = error.error;
                alertDiv.style.display = 'block';
            })
            .finally(() => {
                isLoading = false;
            })
    }

    // Using textContent instead of innerHTML to prevent XSS attacks.
    function showProperty(property, initial) {
        const divFlex = document.createElement("div");
        divFlex.classList.add("d-flex", "justify-content-center", "mt-5", "property");

        if (initial == true) {
            const initialProperties = document.querySelector('#initial-properties');
            initialProperties.appendChild(divFlex);
        } else {
            const searchedProperties = document.querySelector('#searched-properties');
            searchedProperties.appendChild(divFlex);
        }

        const divCard = document.createElement("div");
        divCard.classList.add("card", "border-light", "mb-3");
        divFlex.appendChild(divCard);

        const divRow = document.createElement("div");
        divRow.classList.add("row", "g-0");
        divCard.appendChild(divRow);

        const divColImg = document.createElement("div");
        divColImg.classList.add("col-md-4");
        divRow.appendChild(divColImg);

        const img = document.createElement("img");
        img.setAttribute('src', MEDIA_URL + property.image);
        img.classList.add("img-fluid", "rounded-start", "h-100", "object-fit-cover");
        divColImg.appendChild(img);

        const divColBody = document.createElement("div");
        divColBody.classList.add("col-md-8");
        divRow.appendChild(divColBody);

        const divCardBody = document.createElement("div");
        divCardBody.classList.add("card-body");
        divColBody.appendChild(divCardBody);

        const h4 = document.createElement("h4");
        if (property.title.length > titleLimit) {
            h4.textContent = property.title.slice(0, titleLimit) + "...";
        } else {
            h4.textContent = property.title;
        }
        h4.classList.add("card-title", "fw-bold");
        divCardBody.appendChild(h4);

        const pLocation = document.createElement("p");
        pLocation.classList.add("card-text");
        const iLocation = document.createElement("i");
        iLocation.classList.add("bi", "bi-geo-alt-fill", "text-danger", "me-1");
        pLocation.appendChild(iLocation);
        const smallLocation = document.createElement("small");
        smallLocation.classList.add("text-body-secondary");
        smallLocation.textContent = property.location;
        pLocation.appendChild(smallLocation);
        divCardBody.appendChild(pLocation);

        const pDescription = document.createElement("p");
        pDescription.classList.add("card-text", "mb-3");
        if (property.description.length > descriptionLimit) {
            pDescription.textContent = property.description.slice(0, descriptionLimit) + "...";
        } else {
            pDescription.textContent = property.description;
        }
        divCardBody.appendChild(pDescription);

        const hr = document.createElement("hr");
        hr.classList.add("mt-1", "mb-1");
        divCardBody.appendChild(hr);

        const divJustifyContentBetween = document.createElement("div");
        divJustifyContentBetween.classList.add("d-flex", "justify-content-between", "align-items-end");

        const divPricePerNight = document.createElement("div");
        const pPriceLabel = document.createElement("p");
        pPriceLabel.classList.add("card-text", "mb-0");
        const smallPriceLabel = document.createElement("small");
        smallPriceLabel.classList.add("text-body-secondary");
        smallPriceLabel.textContent = "Precio por noche";
        pPriceLabel.appendChild(smallPriceLabel);
        const pPriceValue = document.createElement("p");
        pPriceValue.classList.add("card-text", "fs-4", "fw-bold", "text-primary", "mb-0");
        pPriceValue.textContent = property.price_per_night + "€";
        divPricePerNight.appendChild(pPriceLabel);
        divPricePerNight.appendChild(pPriceValue);

        const divButton = document.createElement("div");
        const aLink = document.createElement("a");
        aLink.classList.add("primary-button", "text-nowrap", "d-inline-flex", "justify-content-center", "fw-bold");
        aLink.textContent = "Ver Disponibilidad ";
        const iLink = document.createElement("i");
        iLink.classList.add("bi", "bi-chevron-right", "ms-1");
        aLink.appendChild(iLink);
        divButton.appendChild(aLink);

        divJustifyContentBetween.appendChild(divPricePerNight);
        divJustifyContentBetween.appendChild(divButton);
        divCardBody.appendChild(divJustifyContentBetween);
    }
})