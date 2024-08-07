import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";

var routes = [
  {
    key: 0,
    path: "/",
    name: "Chat",
    icon: "fa-solid fa-pen-to-square text-primary",
    component: <Chat />,
    layout: "/auth",
  },
  // {
  //   key: 1,
  //   path: "/c/:id",
  //   name: "Chat",
  //   icon: "fa-solid fa-pen-to-square text-primary",
  //   component: <Chat />,
  //   layout: "/chat",
  // },
  {
    key: 2,
    path: "/login",
    name: "Login",
    icon: "ni ni-key-25 text-info",
    component: <Login />,
    layout: "/auth",
  },
  {
    key: 3,
    path: "/register",
    name: "Register",
    icon: "ni ni-circle-08 text-pink",
    component: <Register />,
    layout: "/auth",
  },
];
export default routes;
