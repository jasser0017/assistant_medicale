import { NavLink } from "react-router-dom";
import {
  AiOutlineRobot,
  AiOutlinePicture,
  AiOutlineVideoCamera,
  AiOutlineAudio,
  AiOutlineBulb,
  AiOutlineBarChart,
} from "react-icons/ai";

const links = [
  { to: "/", icon: AiOutlineRobot, label: "Chat" },
  { to: "/image", icon: AiOutlinePicture, label: "Images" },
  { to: "/videos", icon: AiOutlineVideoCamera, label: "Vidéos" },
  { to: "/voice", icon: AiOutlineAudio, label: "Voix" },
  { to: "/quiz", icon: AiOutlineBulb, label: "Quiz" },
  { to: "/reports", icon: AiOutlineBarChart, label: "Rapports" },
];

export default function Sidebar() {
  return (
    <aside className="flex w-20 flex-col items-center gap-6 bg-primary/90 py-6 text-white">
      {links.map(({ to, icon: Icon, label }) => (
        <NavLink
          key={to}
          to={to}
          title={label}
          className={({ isActive }) =>
            `flex h-11 w-11 items-center justify-center rounded-xl transition
             ${isActive ? "bg-white/20" : "hover:bg-white/10"}`
          }
        >
          <Icon size={22} />
        </NavLink>
      ))}
    </aside>
  );
}
