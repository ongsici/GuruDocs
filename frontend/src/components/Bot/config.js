import { createChatBotMessage } from 'react-chatbot-kit';


const botName = 'GuruDocsBot';

const config = {
  initialMessages: [createChatBotMessage(`Hello! What questions do you have about your document?`)],
  botName: botName,
  customComponents: {
    botChatMessage: ({ message, loader }) => (
      <div className="react-chatbot-kit-chat-bot-message">
        {message.split("\n").map((msg) => (
          <p style={{ marginBlock: "0px" }}>{msg}</p>
        ))}
        <div className="react-chatbot-kit-chat-bot-message-arrow"></div>
      </div>
    ),
  },

};

export default config;