import { FiSend } from "react-icons/fi";

export default function ChatInput() {
  return (
    <form
      onSubmit={(e) => e.preventDefault()}
      className="sticky bottom-0 left-0 right-0 rounded-4xl bg-white/10
                 backdrop-blur-md border border-white/20 mx-8 mb-6 flex items-center
                 px-4 py-3 shadow-[0_4px_20px_rgba(0,0,0,0.1)]"
    >
      <input
        type="text"
        placeholder="Enter a prompt"
        className="flex-1 bg-transparent text-sm text-white placeholder:text-white/60
                   focus:outline-none"
      />
      <button
        type="submit"
        className="ml-4 inline-flex items-center gap-1 rounded-full bg-primary/90
                   px-6 py-2 text-sm font-medium text-white hover:bg-primary"
      >
        Generate <FiSend />
      </button>
    </form>
  );
}
