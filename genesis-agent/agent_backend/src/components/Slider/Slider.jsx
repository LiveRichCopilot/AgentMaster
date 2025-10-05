import React from 'react';
import './Slider.css';

const Slider = ({ label, value, onChange, min, max, step }) => {
  return (
    <div className="slider-container">
      <label>{label}</label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={onChange}
        className="slider"
      />
      <span>{value}</span>
    </div>
  );
};

export default Slider;
