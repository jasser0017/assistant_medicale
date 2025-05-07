import ChatPanel from "../../components/ChatPanel";
import PatientPanel from "../../components/PatientPanel";
import ChatInput from "../../components/ChatInput";

export default function ChatPage() {
  return (
    <div className="flex h-full gap-6">
      <div className="flex-1 flex flex-col gap-6 overflow-hidden">
        <ChatPanel />
        <ChatInput />
      </div>
      <PatientPanel />
    </div>
  );
}