const video = document.getElementById("video");
const statusText = document.getElementById("status");

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream)
  .catch(err => console.error("Camera error:", err));

function startCapture() {
    const name = document.getElementById("studentName").value.trim();
    if (!name) {
        alert("Please enter a name or ID");
        return;
    }

    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    let count = 0;
    const maxImages = 25;

    const interval = setInterval(() => {
        if (count >= maxImages) {
            clearInterval(interval);
            statusText.textContent = "✅ Capture complete!";
            return;
        }

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL("image/jpeg");

        fetch("/upload_face", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, image: imageData, count })
        })
        .then(res => res.json())
        .then(data => console.log(data.message));

        count++;
        statusText.textContent = `Capturing... ${count}/25`;
    }, 300);
}
