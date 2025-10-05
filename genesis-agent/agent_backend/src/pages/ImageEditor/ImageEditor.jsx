
import React, { useState, useRef } from 'react';
import Header from '../../components/Header/Header';
import Tabs from '../../components/Tabs/Tabs';
import EditorControls from '../../components/EditorControls/EditorControls'; // Import the new component
import './ImageEditor.css';

// Component to render content based on the active tab
const TabContent = ({ activeTab, imageInfo }) => {
  switch (activeTab) {
    case 'Editor':
      return (
        <div className="tab-content-wrapper">
          {/* Add the new editor controls here */}
          <EditorControls />
          <div className="info-content">
            <h3>Info</h3>
            {imageInfo ? (
              <ul>
                <li><strong>File Name:</strong> {imageInfo.name}</li>
                <li><strong>Dimensions:</strong> {imageInfo.dimensions}</li>
                <li><strong>Size:</strong> {imageInfo.size}</li>
              </ul>
            ) : (
              <p>Upload an image to see details.</p>
            )}
          </div>
        </div>
      );
    case 'Magic Edit':
      return (
        <div className="info-content">
          <h3>Magic Edit</h3>
          <p>Magic Edit tools will be available here.</p>
        </div>
      );
    case 'Face Swap':
      return (
        <div className="info-content">
          <h3>Face Swap</h3>
          <p>Face Swap feature will be available here.</p>
        </div>
      );
    default:
      return null;
  }
};

const ImageEditor = () => {
  const [image, setImage] = useState(null);
  const [imageInfo, setImageInfo] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [activeTab, setActiveTab] = useState('Editor');
  const fileInputRef = useRef(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        const img = new Image();
        img.onload = () => {
          setImageInfo({
            name: file.name,
            dimensions: `${img.width}x${img.height}`,
            size: `${(file.size / 1024).toFixed(2)} KB`,
          });
        };
        img.src = reader.result;
      };
      reader.readAsDataURL(file);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const handleGenerate = () => {
    console.log('Generate button clicked with prompt:', prompt);
  };

  const editorTabs = ['Editor', 'Magic Edit', 'Face Swap'];

  return (
    <div className="image-editor-page">
      <Header title="Image Editor" />
      <div className="editor-layout">
        <div className="preview-panel">
          {image ? (
            <img src={image} alt="Preview" className="image-preview" />
          ) : (
            <div className="upload-placeholder">
              <button onClick={triggerFileInput} className="upload-btn">
                Upload Image
              </button>
            </div>
          )}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleImageUpload}
            style={{ display: 'none' }}
            accept="image/*"
          />
        </div>
        <div className="info-panel">
          <Tabs tabs={editorTabs} activeTab={activeTab} setActiveTab={setActiveTab} />
          <TabContent activeTab={activeTab} imageInfo={imageInfo} />
        </div>
      </div>
      <div className="prompt-bar">
        <input
          type="text"
          placeholder="Enter your prompt here..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button onClick={handleGenerate}>Generate</button>
      </div>
    </div>
  );
};

export default ImageEditor;
