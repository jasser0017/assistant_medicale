import { createBrowserRouter } from "react-router-dom";
import App from "../App";
//import Dashboard from "src/pages/Dashboard";
import ChatPage from "src/pages/Chat";

// pour l’instant Home = Dashboard provisoire

export const router = createBrowserRouter([
  {
    element: <App />,
    children: [
      { path: "chat", element: <ChatPage /> },
{ index: true, element: <ChatPage /> },
      // les autres routes seront ajoutées plus tard
    ],
  },
]);
