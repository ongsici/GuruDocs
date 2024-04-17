import React, { useState } from 'react';
import './Toast.css';

export default function Toast({ message, onClose }) {
  const [visible, setVisible] = useState(true);

  const handleClose = () => {
    setVisible(false);
    onClose();
  };

  return (
    <div className={`toast ${visible ? 'show' : 'hide'}`}>
      <div className="toast-content">{message}</div>
      <button className="close-button" onClick={handleClose}>
        &times;
      </button>
    </div>
  );
}

