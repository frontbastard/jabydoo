document.addEventListener("DOMContentLoaded", function () {
    function openSponsor(encodedUrl) {
        if (!encodedUrl) return;
        let decodedUrl = atob(encodedUrl);
        window.open(decodedUrl, "_blank");
    }

    document.querySelectorAll("[data-sponsor-url]").forEach(button => {
        button.addEventListener("click", function () {
            let encodedUrl = button.getAttribute("data-sponsor-url");
            openSponsor(encodedUrl);
        });
    });
});
