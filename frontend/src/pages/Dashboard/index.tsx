// src/pages/Dashboard/index.tsx
import Card from "../../components/Card";
import {
  AiOutlineRobot,
  AiOutlinePicture,
  AiOutlineVideoCamera,
  AiOutlineAudio,
  AiOutlineBulb,
  AiOutlineBarChart,
} from "react-icons/ai";

export default function Dashboard() {
  return (
    <div className="flex-1 overflow-y-auto bg-bgLight">
      {/* Max-width + spacing */}
      <div className="mx-auto max-w-6xl space-y-6 p-8">
        <div className="grid gap-6 lg:grid-cols-2">
          <Card title="Chatbot" icon={<AiOutlineRobot />} />
          <Card title="Image Generation" icon={<AiOutlinePicture />} />
          <Card title="Educational Videos" icon={<AiOutlineVideoCamera />} />
          <Card title="Voice Integration" icon={<AiOutlineAudio />} />
          <Card title="Quizzes" icon={<AiOutlineBulb />} />
          <Card title="Weekly Reports" icon={<AiOutlineBarChart />} />
        </div>
      </div>
    </div>
  );
}
