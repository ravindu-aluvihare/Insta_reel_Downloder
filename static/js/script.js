document.getElementById("reelForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const url = document.getElementById("url").value;
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    loading.style.display = "block";
    result.innerHTML = "";

    const formData = new FormData();
    formData.append("url", url);

    try {
        const response = await fetch("/download", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        loading.style.display = "none";

        if (data.success) {
            result.innerHTML = `<a href="${data.url}" class="download-link">📥 Download Reel Video</a>`;
        } else {
            result.innerHTML = `<p style="color:red;">❌ Error: ${data.message}</p>`;
        }
    } catch (error) {
        loading.style.display = "none";
        result.innerHTML = `<p style="color:red;">❌ Request failed.</p>`;
    }
});
