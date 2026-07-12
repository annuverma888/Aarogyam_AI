// ================================
// Disease Recommendation System
// script.js
// ================================

document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Initialize Select2
    // ==========================

    if ($(".symptom-select").length) {

        $(".symptom-select").select2({

            placeholder: "🔍 Search Symptoms",

            allowClear: true,

            width: "100%"

        });

    }

    // ==========================
    // Loading Spinner
    // ==========================

    const form = document.querySelector("form");

    if (form) {

        form.addEventListener("submit", function () {

            const loading = document.getElementById("loading");

            if (loading) {

                loading.style.display = "flex";

            }

        });

    }

    // ==========================
    // Hide Loading
    // ==========================

    window.onload = function () {

        const loading = document.getElementById("loading");

        if (loading) {

            loading.style.display = "none";

        }

    }

    // ==========================
    // Dark Mode
    // ==========================

    const themeBtn = document.getElementById("theme-btn");

    if (themeBtn) {

        let theme = localStorage.getItem("theme");

        if (theme === "dark") {

            document.body.classList.add("dark-mode");

            themeBtn.innerHTML =
                '<i class="bi bi-sun-fill"></i>';

        }

        themeBtn.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

            if (document.body.classList.contains("dark-mode")) {

                localStorage.setItem("theme", "dark");

                themeBtn.innerHTML =
                    '<i class="bi bi-sun-fill"></i>';

            }

            else {

                localStorage.setItem("theme", "light");

                themeBtn.innerHTML =
                    '<i class="bi bi-moon-stars-fill"></i>';

            }

        });

    }

    // ==========================
    // Card Animation
    // ==========================

    const cards = document.querySelectorAll(".result-card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-10px)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0px)";

        });

    });

    // ==========================
    // Copy Disease Name
    // ==========================

    const disease = document.querySelector(".disease-name");

    if (disease) {

        disease.style.cursor = "pointer";

        disease.title = "Click to Copy";

        disease.addEventListener("click", function () {

            navigator.clipboard.writeText(disease.innerText);

            showToast("Disease name copied!");

        });

    }

    // ==========================
    // Smooth Scroll
    // ==========================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            e.preventDefault();

            document.querySelector(this.getAttribute("href"))
                ?.scrollIntoView({

                    behavior: "smooth"

                });

        });

    });

});

// =====================================
// Scroll to Top Button
// =====================================

const scrollBtn = document.createElement("button");

scrollBtn.innerHTML = "⬆";

scrollBtn.id = "scrollTop";

document.body.appendChild(scrollBtn);

scrollBtn.onclick = function () {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

};

window.addEventListener("scroll", function () {

    if (window.scrollY > 300) {

        scrollBtn.style.display = "block";

    }

    else {

        scrollBtn.style.display = "none";

    }

});

// =====================================
// Toast Notification
// =====================================

function showToast(message) {

    const toast = document.createElement("div");

    toast.className = "custom-toast";

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 2500);

}

// =====================================
// Print Report
// =====================================

function printReport() {

    window.print();

}

// =====================================
// Download PDF Placeholder
// =====================================

function downloadPDF() {

    showToast("PDF feature will be added in next step.");

}

