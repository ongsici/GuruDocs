/* eslint-disable react-hooks/exhaustive-deps */
import { useRef, useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { REACT_APP_BACKEND_URL } from "../../config";
import { useFetch } from "../../hooks/useFetch";
import { CircularProgress } from "@mui/material";


export default function Summary() {
    const [summary, setSummary] = useState("");
  
    const {
        // success: postFilesSuccess,
        loading: postFilesLoading,
        // error: postFilesError,
        renderFetch: getSummary,
        data: summaryData
      } = useFetch(`${REACT_APP_BACKEND_URL}/summary`, "GET");

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
    if (postFilesLoading) {
        return (
            <Box m={20}>
              <CircularProgress />
            </Box>
        );
      }

    return (
      <Typography>
        {summary}
      </Typography>
    );
  }
  