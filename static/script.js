
const checkButton = document.getElementById("check-btn");
const sentenceInput = document.getElementById("sentence");
const resultsSection = document.getElementById("results");
const characterCount = document.getElementById("character-count");
const errorMessage = document.getElementById("error-message");

sentenceInput.addEventListener("input", () => {
    characterCount.textContent =
        `${sentenceInput.value.length} characters`;
});
checkButton.addEventListener("click", async () => {
    const sentence = sentenceInput.value.trim();

    if (!sentence) {
    errorMessage.textContent = "Please enter an English sentence.";
    errorMessage.hidden = false;
    return;
}

    checkButton.disabled = true;
    checkButton.textContent = "Checking...";
    resultsSection.hidden = true;
errorMessage.hidden = true;
    try {
        const response = await fetch("/grammar/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: sentence
            })
        });

        if (!response.ok) {
            throw new Error("Unable to check grammar. Please try again.");
        }

        const data = await response.json();

        document.getElementById("corrected").textContent =
            data.corrected;

        document.getElementById("explanation").textContent =
            data.explanation;

        document.getElementById("natural").textContent =
            data.natural;

        resultsSection.hidden = false;

    } catch (error) {
errorMessage.textContent = error.message;
errorMessage.hidden = false;
} finally {
        checkButton.disabled = false;
        checkButton.textContent = "Check Grammar";
    }
});
const speakButton = document.getElementById("start-speaking");
const speechStatus = document.getElementById("speech-status");

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    speakButton.addEventListener("click", () => {
        speechStatus.textContent = "Listening...";
        recognition.start();
    });

    recognition.onresult = (event) => {
        const spokenText = event.results[0][0].transcript;
        sentenceInput.value = spokenText;
        characterCount.textContent = `${spokenText.length} characters`;
        speechStatus.textContent = "Speech recognized!";
    };

    recognition.onerror = (event) => {
        speechStatus.textContent = "Microphone error: " + event.error;
    };

    recognition.onend = () => {
        if (speechStatus.textContent === "Listening...") {
            speechStatus.textContent = "Listening stopped.";
        }
    };
} else {
    speakButton.disabled = true;
    speechStatus.textContent = "Speech recognition is not supported.";
}
const listenButton = document.getElementById("listen-btn");

listenButton.addEventListener("click", () => {
    const text = sentenceInput.value.trim();

    if (!text) {
        speechStatus.textContent = "Please enter a sentence first.";
        return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 0.9;

    window.speechSynthesis.speak(speech);
});
const conversationHistory = [];
const chatInput = document.getElementById("chat-input");
const sendChatButton = document.getElementById("send-chat");
const chatMessages = document.getElementById("chat-messages");

sendChatButton.addEventListener("click", async () => {
    const message = chatInput.value.trim();

    if (!message) return;

    const userMessage = document.createElement("p");
    userMessage.textContent = "You: " + message;
    userMessage.classList.add("user-message");
    chatMessages.appendChild(userMessage);
chatMessages.scrollTop = chatMessages.scrollHeight;
    chatInput.value = "";
    sendChatButton.disabled = true;
    sendChatButton.textContent = "Thinking...";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
           body: JSON.stringify({
    message,
        history: conversationHistory,
    level: document.getElementById("english-level").value
})
});
        if (!response.ok) {
            throw new Error("Unable to get AI response.");
        }

        const data = await response.json();
conversationHistory.push({
    role: "user",
    content: message
});

conversationHistory.push({
    role: "assistant",
    content: data.reply
});
        const aiMessage = document.createElement("p");
        aiMessage.textContent = "AI Coach: " + data.reply;
        aiMessage.classList.add("ai-message");
        chatMessages.appendChild(aiMessage);
        const replayButton = document.createElement("button");

replayButton.textContent = "🔊 Listen Again";
replayButton.type = "button";
replayButton.classList.add("replay-button");

replayButton.addEventListener("click", () => {
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(data.reply);
    speech.lang = "en-US";
    speech.rate = 0.9;

    window.speechSynthesis.speak(speech);
});

aiMessage.appendChild(replayButton);
        chatMessages.scrollTop = chatMessages.scrollHeight;
window.speechSynthesis.cancel();

const aiSpeech = new SpeechSynthesisUtterance(data.reply);

aiSpeech.lang = "en-US";
aiSpeech.rate = 0.9;
aiSpeech.pitch = 1;

window.speechSynthesis.speak(aiSpeech);
    } catch (error) {
        const errorText = document.createElement("p");
        errorText.textContent = error.message;
        chatMessages.appendChild(errorText);

    } finally {
        sendChatButton.disabled = false;
        sendChatButton.textContent = "Send Message";
    }
});
const voiceChatButton = document.getElementById("start-voice-chat");
const voiceChatStatus = document.getElementById("voice-chat-status");

if (SpeechRecognition) {
    const voiceRecognition = new SpeechRecognition();
    voiceRecognition.lang = "en-US";
    voiceRecognition.continuous = false;
    voiceRecognition.interimResults = false;

voiceChatButton.addEventListener("click", () => {        window.speechSynthesis.cancel();
        voiceChatStatus.textContent = "Listening...";
        voiceRecognition.start();
    });

    voiceRecognition.onresult = (event) => {
        const spokenMessage = event.results[0][0].transcript;

        chatInput.value = spokenMessage;
        voiceChatStatus.textContent = "Sending your message...";

        sendChatButton.click();
    };

    voiceRecognition.onerror = (event) => {
        voiceChatStatus.textContent =
            "Microphone error: " + event.error;
    };

    voiceRecognition.onend = () => {
        if (voiceChatStatus.textContent === "Listening...") {
            voiceChatStatus.textContent = "Listening stopped.";
        }
    };
} else {
    voiceChatButton.disabled = true;
    voiceChatStatus.textContent =
        "Voice recognition is not supported in this browser.";
}


newChatButton.addEventListener("click", () => {
    conversationHistory.length = 0;

    chatMessages.innerHTML = "";
    chatInput.value = "";

    window.speechSynthesis.cancel();

    voiceChatStatus.textContent = "New conversation started!";
});