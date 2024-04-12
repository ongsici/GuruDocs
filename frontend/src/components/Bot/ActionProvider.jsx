import React from 'react';


export default function ActionProvider({ createChatBotMessage, setState, children }) {
  const handleHello = () => {
    const botMessage = createChatBotMessage('Hello. Nice to meet you.');

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };
 
  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleHello,
          },
        });
      })}
    </div>
  );
};
