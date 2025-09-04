const reportButtons = document.querySelectorAll(".report-btn");
const reportModal = document.getElementById("reportModal");
const confirmReportBtn = document.getElementById("confirmReport");
const keepReportBtn = document.getElementById("keepReport");
const reportReasonInput = document.getElementById("reportReason");

let currentType = null;
let currentId = null;
let currentUserId = null;
let currentButton = null; // store which button was clicked

reportButtons.forEach(button => {
    button.addEventListener("click", () => {
        currentType = button.dataset.type;
        currentId = button.dataset.id;
        currentUserId = button.dataset.userId;
        currentButton = button; // keep reference to this button

        reportReasonInput.value = "";
        reportModal.style.display = "flex";
    });
});

keepReportBtn.addEventListener("click", () => {
    reportModal.style.display = "none";
});

confirmReportBtn.addEventListener("click", () => {
    const reason = reportReasonInput.value.trim();
    if (!reason) {
        alert("Please enter a reason before submitting.");
        return;
    }

    const url = `/crowdfunding/report/${currentType}/${currentId}/${currentUserId}/`;

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ reason })
    })
        .then(res => res.json())
        .then(data => {
            reportModal.style.display = "none";
            alert(data.message);
            console.log("Making badge .......... ")
            if (data.success) {
                console.log("inside sucess ....... ")
                if (currentType === "project") {
                    const projectCard = document.querySelector(".project-card");
                    if (projectCard && !projectCard.querySelector(".badge")) {
                        const badge = document.createElement("span");
                        badge.className = "badge bg-danger position-absolute bottom-0 end-0 m-2";
                        badge.textContent = "Reported";
                        projectCard.classList.add("position-relative"); // parent must be relative
                        projectCard.appendChild(badge);
                    }
                }
                if (currentType === "comment") {
                    const commentCard = document.getElementById(`comment-${currentId}`);
                    if (commentCard && !commentCard.querySelector(".badge")) {
                        const badge = document.createElement("span");
                        badge.className = "badge bg-danger position-absolute bottom-0 end-0 m-2";
                        badge.textContent = "Reported";
                        commentCard.classList.add("position-relative"); // parent must be relative
                        commentCard.appendChild(badge);
                    }
                }

                if (currentButton) {
                    currentButton.disabled = true;
                    currentButton.textContent = "Reported";
                }
            }
        })
        .catch(err => console.error("Report error:", err));
});
