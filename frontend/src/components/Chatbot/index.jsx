import { useRef, useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import { REACT_APP_BACKEND_URL } from "../../config";
import { useFetch } from "../../hooks/useFetch";

export default function Chatbot() {
    const [chatmessage, setChatMessage] = useState("");
  
    const {
        // success: postFilesSuccess,
        // loading: postFilesLoading,
        // error: postFilesError,
        renderFetch: getSummary,
        data: summaryData
      } = useFetch(`${REACT_APP_BACKEND_URL}/query`, "GET");

    useEffect(() => {
    if (!summary) {
        getSummary();
    }
    }, [summary]);

    useEffect(() => {
    if (summaryData) {
        setSummary(summaryData);
    }
    }, [summaryData]);

    // TODO: implement spinner when loading (see UploadDialog)

    return (
      <Typography>
        {chatmessage}
      </Typography>
    );
  }
