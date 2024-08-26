// import React from 'react';

function Modal({ data }) {
  const errors = data;

  return (
    <>
      {Object.keys(errors).length > 0 && (
        <div className="error-messages">
          {Object.values(errors)
            .filter((error) => error)
            .map((error, index) => (
              <div key={index}>{error}</div>
            ))}
        </div>
      )}
    </>
  );
}

export default Modal;
