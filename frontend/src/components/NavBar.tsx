import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function App() {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col p-6 gap-6">
        <Topbar />
        <div className="flex-1 overflow-hidden">
          <Outlet />
        </div>
      </div>
      
      {/* Message Windows */}
      <div className="fixed bottom-2 right-2 text-xs text-gray-400/50">
        Active Windows • Accident aux paramètres pour activer Windows.
      </div>
    </div>
  );
}