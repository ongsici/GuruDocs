import Chatbot from 'react-chatbot-kit'
import '../Bot/App.css'
import config from '../Bot/config.js';
import MessageParser from '../Bot/MessageParser.jsx';
import ActionProvider from '../Bot/ActionProvider.jsx';

export default function ChatBot({ model, setModel, vectorstoreUuidList, setVectorstoreUuidList }) {

  return (
    <div>
      <Chatbot
        config={config}
        messageParser={(props) => <MessageParser {...props} 
                                    vectorstoreUuidList={vectorstoreUuidList}
                                    setVectorstoreUuidList={setVectorstoreUuidList}/>}
        actionProvider={(props) => <ActionProvider {...props} 
                                    model={model} 
                                    setModel={setModel}
                                    vectorstoreUuidList={vectorstoreUuidList}
                                    setVectorstoreUuidList={setVectorstoreUuidList}/>}
      />
    </div>
);
  }