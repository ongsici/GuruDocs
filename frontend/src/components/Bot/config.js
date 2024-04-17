import { createChatBotMessage } from 'react-chatbot-kit';


const botName = 'GuruDocsBot';

const config = {
  initialMessages: [createChatBotMessage(`Hello! What questions do you have about your document?`)],
  botName: botName,
  // customStyles: {
  //   botMessageBox: {
  //     backgroundColor: '#5BBCFF',
  //   },
  //   chatButton: {
  //     backgroundColor: '#5ccc9d',
  //   },
  // },
};

export default config;