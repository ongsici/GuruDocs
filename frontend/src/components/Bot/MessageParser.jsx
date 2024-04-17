import React from 'react';

export default function MessageParser({ children, actions, vectorstoreUuidList, setVectorstoreUuidList }) {
    const parse = (message) => {
      if (message.includes('hello')) {
        actions.handleHello();
      } else if (!vectorstoreUuidList || vectorstoreUuidList.length === 0){
        actions.handleNotReady();
      } else {
        actions.sendLLMQuery(message);
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

