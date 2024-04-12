import { useRef, useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import { REACT_APP_BACKEND_URL } from "../../config.js";
import { useFetch } from "../../hooks/useFetch.js";
import Chatbot from 'react-chatbot-kit'
// import 'react-chatbot-kit/build/main.css'
import '../Bot/App.css'
import config from '../Bot/config.js';
import MessageParser from '../Bot/MessageParser.jsx';
import ActionProvider from '../Bot/ActionProvider.jsx';

export default function ChatBot() {

  return (
    <div>
      <Chatbot
        config={config}
        messageParser={MessageParser}
        actionProvider={ActionProvider}
      />
    </div>
);
  }