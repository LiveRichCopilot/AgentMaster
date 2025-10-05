import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  IoHomeOutline,
  IoImageOutline,
  IoColorWandOutline,
  IoKeyOutline,
  IoDocumentTextOutline,
  IoPersonCircleOutline,
  IoLogOutOutline
} from 'react-icons/io5';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">SWITCH</div>
      <nav className="sidebar-menu">
        <NavLink to="/dashboard">
          <IoHomeOutline />
          <span>Dashboard</span>
        </NavLink>
        <NavLink to="/image-editor">
          <IoImageOutline />
          <span>Image Editor</span>
        </NavLink>
        <NavLink to="/prompt-studio">
          <IoColorWandOutline />
          <span>Prompt Studio</span>
        </NavLink>
        <NavLink to="/api-keys">
          <IoKeyOutline />
          <span>API Keys</span>
        </NavLink>
        <NavLink to="/documentation">
          <IoDocumentTextOutline />
          <span>Documentation</span>
        </NavLink>
      </nav>
      <div className="sidebar-footer">
        <div className="user-profile">
          <IoPersonCircleOutline size={40} className="user-avatar-icon" />
          <span>Rich</span>
        </div>
        <a href="/logout" className="sign-out-link">
          <IoLogOutOutline />
          <span>Sign Out</span>
        </a>
      </div>
    </div>
  );
};

export default Sidebar;
