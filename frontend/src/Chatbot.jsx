import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Chatbot() {
  const [messages, setMessages] = useState([
    {
      text: "Hi I am telecom corp agent.  How can I help you with queries related to telecom marketing and error code lookups ?",
      sender: "bot",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });

      const data = await response.json();
      setMessages([...newMessages, { text: data.response, sender: "bot" }]);
    } catch (error) {
      console.error("Error:", error);
      setMessages([
        ...newMessages,
        { text: "Error getting response", sender: "bot" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col w-full max-w-lg mx-auto bg-gray-100 rounded-lg shadow-lg p-4">
      {/* Messages */}
      <div className="h-96 overflow-y-auto p-2 space-y-3">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg max-w-xs ${
              msg.sender === "user"
                ? "bg-blue-500 text-white self-end ml-auto"
                : "bg-gray-300 text-black self-start"
            }`}
          >
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {msg.text}
            </ReactMarkdown>
          </div>
        ))}

        {/* Loader */}
        {loading && (
          <div className="text-gray-500 italic">Bot is typing...</div>
        )}
      </div>

      {/* Input Box */}
      <div className="flex items-center border-t border-gray-300 mt-2 pt-2">
        <input
          type="text"
          className="flex-1 p-2 border rounded-lg outline-none"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          className="bg-blue-500 text-white p-2 ml-2 rounded-lg"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
