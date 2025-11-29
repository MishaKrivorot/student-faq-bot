const API_BASE = "http://localhost:8000/api"; // при деплої змінити на URL бекенду
const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const input = document.getElementById("question");

function addMessage(text, who="bot"){
  const div = document.createElement("div");
  div.className = "msg " + (who==="user" ? "user" : "bot");
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = input.value.trim();
  if(!q) return;
  addMessage(q, "user");
  input.value = "";
  addMessage("...", "bot");
  try {
    const res = await fetch(API_BASE + "/query", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({question: q})
    });
    const data = await res.json();
    // видалимо тимчасове "..."
    chat.querySelectorAll(".msg.bot").forEach(node => {
      if(node.textContent === "...") node.remove();
    });
    addMessage(data.answer || "Відповіді нема", "bot");
  } catch(err){
    chat.querySelectorAll(".msg.bot").forEach(node => {
      if(node.textContent === "...") node.remove();
    });
    addMessage("Помилка з'єднання з сервером", "bot");
  }
});
