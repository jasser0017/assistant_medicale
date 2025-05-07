import React from 'react';
import { Outlet } from 'react-router-dom';
import NavBar from './NavBar';

export default function Layout() {
  return (
    <div className="app-container">
      <NavBar />
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
