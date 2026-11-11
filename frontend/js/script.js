// Backend API URL

const API_URL = "https://ai-cv-analyzer-1-4cp0.onrender.com";


// Registration Form

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const fullName = document.getElementById("full_name").value.trim();

        const email = document.getElementById("email").value.trim();

        const password = document.getElementById("password").value;

        const confirmPassword = document.getElementById("confirm_password").value;

        const messageBox = document.getElementById("registerMessage");

        const submitButton = registerForm.querySelector("button[type='submit']");


        // Check password confirmation

        if (password !== confirmPassword) {

            messageBox.textContent = "Passwords do not match.";

            messageBox.className = "form-message error";

            return;
        }


        // Show loading

        submitButton.disabled = true;

        submitButton.textContent = "Creating Account...";

        messageBox.className = "form-message";

        messageBox.textContent = "";


        try {

            // Send registration request

            const response = await fetch(`${API_URL}/auth/register`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    full_name: fullName,

                    email: email,

                    password: password

                })

            });


            const data = await response.json();


            // Handle API errors

            if (!response.ok) {

                throw new Error(
                    data.detail || "Registration failed."
                );

            }


            // Success message

            messageBox.textContent = data.message;

            messageBox.className = "form-message success";


            // Reset form

            registerForm.reset();


            // Redirect to login page after 2 seconds

            setTimeout(() => {

                window.location.href = "login.html";

            }, 2000);


        }

        catch (error) {

            messageBox.textContent = error.message;

            messageBox.className = "form-message error";

        }

        finally {

            submitButton.disabled = false;

            submitButton.textContent = "Create Account →";

        }

    });

}

// ===============================
// LOGIN FORM
// ===============================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const email = document.getElementById("email").value.trim();

        const password = document.getElementById("password").value;

        const messageBox = document.getElementById("loginMessage");

        const submitButton = loginForm.querySelector(
            "button[type='submit']"
        );


        // Loading message

        submitButton.disabled = true;

        submitButton.textContent = "Logging in...";

        messageBox.className = "form-message";

        messageBox.textContent = "";


        try {

            // Send Login Request

            const response = await fetch(`${API_URL}/auth/login`, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    email: email,

                    password: password

                })

            });


            const data = await response.json();


            // Check API Response

            if (!response.ok) {

                throw new Error(
                    data.detail || "Login failed."
                );

            }


            // Save basic user information temporarily

            sessionStorage.setItem(
                "currentUser",
                JSON.stringify(data.user)
            );


            // Show success message

            messageBox.textContent = data.message;

            messageBox.className = "form-message success";


            // Redirect to dashboard

            setTimeout(() => {

                window.location.href = "dashboard.html";

            }, 1500);


        }

        catch (error) {

            messageBox.textContent = error.message;

            messageBox.className = "form-message error";

        }

        finally {

            submitButton.disabled = false;

            submitButton.textContent = "Login →";

        }

    });

}

// ===============================
// DASHBOARD USER INFORMATION
// ===============================

const currentUser = sessionStorage.getItem("currentUser");

const dashboardPage = document.querySelector(".dashboard-page");

if (dashboardPage) {

    // Check login information

    if (!currentUser) {

        window.location.href = "login.html";

    } else {

        const user = JSON.parse(currentUser);

        // Display user name

        document.getElementById("userName").textContent =
            user.full_name;

        document.getElementById("userEmail").textContent =
            user.email;

        document.getElementById("welcomeName").textContent =
            user.full_name.split(" ")[0];

        // Display avatar initial

        document.getElementById("userAvatar").textContent =
            user.full_name.charAt(0).toUpperCase();

    }

}


// ===============================
// LOGOUT FUNCTION
// ===============================

const logoutBtn = document.getElementById("logoutBtn");

if (logoutBtn) {

    logoutBtn.addEventListener("click", function () {

        sessionStorage.removeItem("currentUser");

        window.location.href = "login.html";

    });

}

// =====================================
// CV PDF UPLOAD AND ANALYSIS
// =====================================

const uploadBtn = document.getElementById("uploadBtn");
const cvFile = document.getElementById("cvFile");

const selectedFile = document.getElementById("selectedFile");
const uploadMessage = document.getElementById("uploadMessage");

const uploadProgress = document.getElementById("uploadProgress");
const progressBar = document.getElementById("progressBar");

if (uploadBtn && cvFile) {

    uploadBtn.addEventListener("click", function () {
        cvFile.click();
    });

    cvFile.addEventListener("change", async function () {

        const file = cvFile.files[0];

        if (!file) return;

        console.log("Selected file:", file.name);

        selectedFile.textContent = "Selected: " + file.name;

        // Validate PDF
        if (!file.name.toLowerCase().endsWith(".pdf")) {
            uploadMessage.textContent = "Please select a PDF file.";
            uploadMessage.className = "form-message error";
            return;
        }

        // Validate size
        if (file.size > 5 * 1024 * 1024) {
            uploadMessage.textContent = "File must be less than 5MB.";
            uploadMessage.className = "form-message error";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        uploadBtn.disabled = true;
        uploadBtn.textContent = "Analyzing...";

        uploadMessage.textContent = "Analyzing your CV. Please wait...";
        uploadMessage.className = "form-message";

        uploadProgress.classList.add("active");
        progressBar.style.width = "30%";

        try {

            console.log("Sending request to backend...");

            const response = await fetch(
                `${API_URL}/cv/analyze-complete`,
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            console.log("Backend response:", data);

            if (!response.ok) {
                throw new Error(data.detail || "Analysis failed.");
            }

            sessionStorage.setItem(
                "cvAnalysisResult",
                JSON.stringify(data)
            );

            progressBar.style.width = "100%";

            uploadMessage.textContent =
                "Analysis completed! Redirecting...";

            uploadMessage.className = "form-message success";

            window.location.href = "result.html";

        }

        catch (error) {

            console.error("CV Analysis Error:", error);

            uploadMessage.textContent = error.message;

            uploadMessage.className = "form-message error";

        }

        finally {

            uploadBtn.disabled = false;
            uploadBtn.textContent = "Choose PDF File";

        }

    });

}

// =====================================
// DISPLAY CV ANALYSIS RESULT
// =====================================

const resultPage = document.querySelector(".result-container");

if (resultPage) {

    const savedResult = sessionStorage.getItem("cvAnalysisResult");

    if (!savedResult) {

        window.location.href = "dashboard.html";

    } else {

        try {

            const result = JSON.parse(savedResult);

            console.log("Complete CV Result:", result);

            // Score
            document.getElementById("cvScore").textContent =
                result.score_analysis?.predicted_score ?? "N/A";


            // File Information
            document.getElementById("fileName").textContent =
                result.filename ?? "N/A";

            document.getElementById("pageCount").textContent =
                result.file_information?.page_count ?? "N/A";

            document.getElementById("wordCount").textContent =
                result.file_information?.word_count ?? "N/A";


            // Skills
            document.getElementById("skillsCount").textContent =
                result.skills_analysis?.total_skills ?? 0;


            // Education
            document.getElementById("educationCount").textContent =
                result.education_analysis?.degrees?.length ?? 0;


            // Projects
            document.getElementById("projectsCount").textContent =
                result.projects_analysis?.total_projects ?? 0;


            // Suggestions
            const suggestionList =
                document.getElementById("suggestionList");

            suggestionList.innerHTML = "";

            const suggestions =
                result.improvement_analysis?.suggestions ?? [];

            if (suggestions.length === 0) {

                suggestionList.textContent =
                    "No suggestions available.";

            } else {

                suggestions.forEach(function (suggestion) {

                    const item = document.createElement("div");

                    item.className = "suggestion-item";

                    item.textContent =
                        typeof suggestion === "string"
                            ? suggestion
                            : JSON.stringify(suggestion);

                    suggestionList.appendChild(item);

                });

            }

        } catch (error) {

            console.error("Result Display Error:", error);

            alert("Unable to display CV analysis results.");

        }

    }

}