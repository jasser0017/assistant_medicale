import clsx from "clsx";

const messages = [
  { id: 1, from: "bot", text: "Hello, how can I assist you today?" },
  { id: 2, from: "user", text: "Can you create an image of a heart?" },
];

export default function ChatPanel() {
  return (
    <div className="flex-1 rounded-4xl bg-white/10 p-6 backdrop-blur-xl border border-white/20 shadow-[0_4px_30px_rgba(0,0,0,0.1)] overflow-y-auto">
      {messages.map((m) => (
        <div
          key={m.id}
          className={clsx(
            "mb-4 max-w-md rounded-3xl px-4 py-2 text-sm transition-all",
            m.from === "bot"
              ? "bg-primary/90 ml-auto text-white shadow-md"
              : "bg-gray-800 mr-auto text-gray-100 border border-gray-700"
          )}
        >
          {m.text}
        </div>
      ))}
    </div>
  );
}