(function() {
    // 1. Create the UI Elements
    function createSidebar() {
        if (document.getElementById('tubechat-sidebar')) return;

        const sidebar = document.createElement('div');
        sidebar.id = 'tubechat-sidebar';
        sidebar.innerHTML = `
            <div id="tubechat-header">
                <span>TubeChat AI 🤖</span>
                <button id="tubechat-close" style="background:none;border:none;color:white;cursor:pointer;">✖</button>
            </div>
            <div id="tubechat-messages">
                <div class="message bot-msg">Hello! I'm analyzing this video...</div>
            </div>
            <div id="tubechat-input-area">
                <input type="text" id="tubechat-input" placeholder="Ask about the video...">
                <button id="tubechat-send">Send</button>
            </div>
        `;
        document.body.appendChild(sidebar);

        // Event Listeners
        document.getElementById('tubechat-close').onclick = () => sidebar.remove();
        document.getElementById('tubechat-send').onclick = sendMessage;
        document.getElementById('tubechat-input').onkeypress = (e) => {
            if (e.key === 'Enter') sendMessage();
        };

        // Trigger backend processing
        const videoId = new URLSearchParams(window.location.search).get('v');
        if (videoId) {
            processVideo(videoId);
        }
    }

    // 2. Call Backend to Process Video
    async function processVideo(videoId) {
        addMessage("Processing transcript...", "bot-msg");
        try {
            const response = await fetch('http://localhost:8000/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_id: videoId })
            });
            const data = await response.json();
            if (data.status === 'success') {
                addMessage("Ready! Ask me anything.", "bot-msg");
            } else {
                addMessage("Error processing video.", "bot-msg");
            }
        } catch (error) {
            addMessage("Backend not connected. Is the Python server running?", "bot-msg");
        }
    }

    // 3. Handle Chat
    async function sendMessage() {
        const input = document.getElementById('tubechat-input');
        const question = input.value.trim();
        if (!question) return;

        addMessage(question, "user-msg");
        input.value = '';
        addMessage("Thinking...", "bot-msg");

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });
            const data = await response.json();
            
            // Remove "Thinking..." (simple way: remove last child)
            const messagesDiv = document.getElementById('tubechat-messages');
            messagesDiv.removeChild(messagesDiv.lastChild);
            
            addMessage(data.answer, "bot-msg");
        } catch (error) {
            addMessage("Error getting answer.", "bot-msg");
        }
    }

    // Helper to add messages to UI
    function addMessage(text, className) {
        const div = document.createElement('div');
        div.className = `message ${className}`;
        div.innerText = text;
        const container = document.getElementById('tubechat-messages');
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    }

    // Initialize logic
    // We wait a second to ensure the page loads, or listen for URL changes (SPA navigation)
    let currentUrl = location.href;
    setInterval(() => {
        if (location.href !== currentUrl) {
            currentUrl = location.href;
            if (currentUrl.includes("watch?v=")) {
                const existingSidebar = document.getElementById('tubechat-sidebar');
                if (existingSidebar) existingSidebar.remove();
                createSidebar();
            }
        }
    }, 1000);

    if (location.href.includes("watch?v=")) {
        createSidebar();
    }

})();