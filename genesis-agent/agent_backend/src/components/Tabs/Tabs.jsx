import React from 'react';
import './Tabs.css';

const Tabs = ({ items, activeTab, setActiveTab }) => {
  return (
    <div className="tabs-container">
      {items.map((item) => (
        <button
          key={item.id}
          className={`tab-item ${activeTab === item.id ? 'active' : ''}`}
          onClick={() => setActiveTab(item.id)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
};

export default Tabs;
