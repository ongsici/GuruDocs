import React from 'react';

export default function MessageParser({ children, actions }) {
    const parse = (message) => {
      if (message.includes('hello')) {
        actions.handleHello();
      }

    };
  
    return (
      <div>
        {React.Children.map(children, (child) => {
          return React.cloneElement(child, {
            parse: parse,
            actions,
          });
        })}
      </div>
    );
  };

