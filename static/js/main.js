document.addEventListener("DOMContentLoaded", function () {
    function openSponsor(encodedUrl) {
        if (!encodedUrl) return;
        let decodedUrl = atob(encodedUrl);
        window.open(decodedUrl, "_blank", "noopener,noreferrer");
    }

    document.querySelectorAll("[data-sponsor-url]").forEach(button => {
        button.addEventListener("click", function () {
            let encodedUrl = button.getAttribute("data-sponsor-url");
            openSponsor(encodedUrl);
        });
    });

    document.querySelectorAll(".content table").forEach(function (table) {
        if (!table.parentElement.classList.contains("table-wrapper")) {
            let wrapper = document.createElement("div");
            wrapper.classList.add("table-wrapper");
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
});
