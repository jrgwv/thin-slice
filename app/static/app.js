const notesEl = document.getElementById("notes");
const buttonEl = document.getElementById("analyzeButton");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const summaryEl = document.getElementById("summary");
const actionItemsEl = document.getElementById("actionItems");
const nextStepEl = document.getElementById("nextStep");

function setLoading(isLoading) {
  buttonEl.disabled = isLoading;
  buttonEl.textContent = isLoading ? "Analyzing..." : "Analyze";
  statusEl.textContent = isLoading ? "Running prototype..." : "";
}

function renderResults(data) {
  summaryEl.textContent = data.summary || "";
  nextStepEl.textContent = data.next_step || "";

  actionItemsEl.innerHTML = "";
  (data.action_items || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    actionItemsEl.appendChild(li);
  });

  resultsEl.classList.remove("hidden");
}

buttonEl.addEventListener("click", async () => {
  const text = notesEl.value.trim();

  if (!text) {
    statusEl.textContent = "Please enter some notes first.";
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }

    renderResults(data);
    statusEl.textContent = "Done.";
  } catch (error) {
    statusEl.textContent = `Error: ${error.message}`;
  } finally {
    setLoading(false);
  }
});
