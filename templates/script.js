document.addEventListener("DOMContentLoaded", function () {
    var showModal = "{{ show_modal|default(False)|lower }}"; 
    var modalMessage = "{{ modal_message|default('') }}"; 
    
    if (showModal === "true") {
        var modal = document.getElementById("myModal");
        var modalText = document.getElementById("modalText");
        modalText.innerText = modalMessage;  // Set modal message
        modal.style.display = "block";  // Show modal
    }

    // Close modal when clicking on the close button
    document.querySelector(".close").addEventListener("click", function () {
        document.getElementById("myModal").style.display = "none";
    });

    // Close modal when clicking outside of it
    window.onclick = function (event) {
        var modal = document.getElementById("myModal");
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    // Loader functionality on search button click
    document.querySelector(".search-button").addEventListener("click", function (event) {
        event.preventDefault(); // Prevents form submission until loader is shown
        document.querySelector(".loader").style.display = "flex"; // Show loader
        
        // Submit the form after a short delay (e.g., 500ms)
        setTimeout(function () {
            document.getElementById("newsForm").submit();
        }, 500);
    });

    window.addEventListener("load", () => {
        const loader = document.querySelector(".loader");
        loader.classList.add("loader-hidden");
        loader.addEventListener("transitioned", () => {
            document.body.removeChild
        })
    })
});