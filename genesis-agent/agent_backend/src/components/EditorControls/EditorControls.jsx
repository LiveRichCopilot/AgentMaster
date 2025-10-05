
import React from 'react';
import './EditorControls.css';

const EditorControls = () => {
  return (
    <div className="editor-controls">
      <div className="slider-group">
        <label>Clarity</label>
        <input type="range" min="0" max="100" defaultValue="50" />
      </div>
      <div className="slider-group">
        <label>Sharpen</label>
        <input type="range" min="0" max="100" defaultValue="50" />
      </div>
      <div className="slider-group">
        <label>Denoise</label>
        <input type="range" min="0" max="100" defaultValue="50" />
      </div>
      <div className="slider-group">
        <label>Deblur</label>
        <input type="range" min="0" max="100" defaultValue="50" />
      </div>
    </div>
  );
};

export default EditorControls;
