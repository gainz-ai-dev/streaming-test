import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

import AuthLayout from "./layouts/Auth";
import ChatLayout from "./layouts/Chat";
import './App.css';

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/auth/*" element={<AuthLayout />} />
      <Route path="/*" element={<ChatLayout />} />
    </Routes>
  </BrowserRouter>
);
