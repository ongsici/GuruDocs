import React from 'react';
import { useState, useEffect } from "react";
import { useFetch } from "../../hooks/useFetch";
import { REACT_APP_BACKEND_URL } from "../../config";
import { CircularProgress } from "@mui/material";
import Box from "@mui/material/Box";

export default function ActionProvider({ createChatBotMessage, setState, children, model, setModel, vectorstoreUuidList, setVectorstoreUuidList }) {
  const {
    loading: getResponseLoading,
    error: getResponseError,
    data: postFilesResponse,
    renderFetch: sendQuery,
  } = useFetch(`${REACT_APP_BACKEND_URL}/query`, "POST");
  
  const handleHello = () => {
    const botMessage = createChatBotMessage('Hello. Nice to meet you.');

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  const handleNotReady = () => {
    const botMessage = createChatBotMessage('Please upload a document or wait for the document processing to be completed.');

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };
  
  const sendLLMQuery = (message) => {
    if (message && vectorstoreUuidList && vectorstoreUuidList.length > 0) {
      console.log("sending API", message, vectorstoreUuidList)
      sendQuery({ model_option: model,
                  vectorstore_id: vectorstoreUuidList[0],
                  user_query: message });
    }
    const botMessage = createChatBotMessage("Sending query, please wait...");
        setState((prev) => ({
          ...prev,
          messages: [...prev.messages, botMessage],
    }));      
  };

  useEffect(() => {
    if (postFilesResponse) {
      const botMessage = createChatBotMessage(postFilesResponse.response);
        setState((prev) => ({
          ...prev,
          messages: [...prev.messages, botMessage],
    }));    
    } else if (getResponseError) {
      const botMessage = createChatBotMessage("Sorry there was an error in getting a response. Please try again.");
        setState((prev) => ({
          ...prev,
          messages: [...prev.messages, botMessage],
    }));  
    }
  }, [postFilesResponse, getResponseError]);

  // if (getResponseLoading) {
  //   return (
  //     <Box m={5}>
  //       <CircularProgress />
  //     </Box>
  // );
  // }
 
  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleHello,
            handleNotReady,
            sendLLMQuery
          },
        });
      })}
    </div>
  );
};
