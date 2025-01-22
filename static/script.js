document.getElementById("fileInput").addEventListener("change", (event) => {
  const fileInput = event.target;
  const preview = document.getElementById("preview");
  if (!fileInput.files[0]) {
    preview.src = null;
    return;
  }
  preview.src = URL.createObjectURL(fileInput.files[0]);
  preview.onload = () => {
    URL.revokeObjectURL(preview.src);
  };
});

document
  .getElementById("uploadForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files[0]) {
      alert("Please upload an image.");
      return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const resultDiv = document.getElementById("result");
    resultDiv.textContent = "Predicting...";

    try {
      const response = await fetch("/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (data.error) {
        resultDiv.textContent = `Error: ${data.error}`;
      } else {
        resultDiv.innerHTML = `<strong>Prediction:</strong> ${data.class}<br><strong>Accuracy:</strong> ${data.accuracy}`;
      }
    } catch (error) {
      console.error("Error:", error);
      resultDiv.innerHTML = `<p>An error occurred while predicting.</p>
      <br/> <pre>${error}</pre>
      `;
    }
  });

document.getElementById("reportButton").addEventListener("click", async () => {
  const reportDiv = document.getElementById("report");
  reportDiv.textContent = "Evaluating Model...";

  try {
    const response = await fetch("/evaluate-model", { method: "GET" });
    const data = await response.json();

    if (data.report) {
      reportDiv.innerHTML = `<pre>${data.report}</pre>`;
    } else {
      reportDiv.textContent = "Unable to fetch the report.";
    }
  } catch (error) {
    console.error("Error:", error);
    reportDiv.innerHTML = `<p>An error occurred while fetching the report.</p>
      <br/> <pre>${error}</pre>
      `;
  }
});
