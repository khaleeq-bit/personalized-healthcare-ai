async function analyzeSymptoms() {

    const age = document.getElementById("age").value;

    const checkboxes = document.querySelectorAll(
        '.symptom input[type="checkbox"]:checked'
    );

    const symptoms = [];

    checkboxes.forEach(function (checkbox) {
        symptoms.push(checkbox.value);
    });

    if (!age) {
        alert("Please enter your age.");
        return;
    }

    if (symptoms.length === 0) {
        alert("Please select at least one symptom.");
        return;
    }

    // Show result section immediately
    const result = document.getElementById("result");
    const prediction = document.getElementById("prediction");

    result.classList.remove("hidden");
    prediction.textContent = "Analyzing...";

    try {

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                age: age,
                symptoms: symptoms
            })
        });

        const data = await response.json();

        console.log(data);

        if (response.ok) {

            prediction.textContent = data.prediction;

        } else {

            prediction.textContent = "Prediction error";

        }

    } catch (error) {

        console.error(error);

        prediction.textContent =
            "Unable to connect to prediction system.";

    }

    result.scrollIntoView({
        behavior: "smooth"
    });
}