/* eslint-disable react-hooks/exhaustive-deps */
import { useRef, useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
// import { Card, CardContent, CircularProgress, Typography, Box } from '@material-ui/core';
import { REACT_APP_BACKEND_URL } from "../../config";
import { useFetch } from "../../hooks/useFetch";
import { CircularProgress, Card, CardContent } from "@mui/material";


export default function Summary({ model, setModel, pagesUuidList, setPagesUuidList, fileName, setFileName }) {
    const [summaries, setSummaries] = useState([]);
  
    const {
        // success: postFilesSuccess,
        loading: postFilesLoading,
        // error: postFilesError,
        renderFetch: getSummary,
        data: postFilesResponse
      } = useFetch(`${REACT_APP_BACKEND_URL}/summary`, "POST");

    useEffect(() => {
      if (pagesUuidList?.length > 0 && summaries.length === 0) {
        getSummary({ pages_id: pagesUuidList, model_option: model });
      }
    }, [summaries, pagesUuidList, model]);
    
    useEffect(() => {
    if (postFilesResponse) {
        setSummaries(postFilesResponse.summary);
    }
    }, [postFilesResponse]);

    if (postFilesLoading) {
        return (
            <Box m={5}>
              <CircularProgress />
            </Box>
        );
      }
    
    return (
      <div>
          {summaries.map((summary, index) => (
              <Card key={index} style={{ marginBottom: '10px' }}>
                  <CardContent>
                      <Typography variant="h6" gutterBottom>
                          {fileName}
                      </Typography>
                      <Typography variant="body1">
                          {summary}
                      </Typography>
                  </CardContent>
              </Card>
          ))}
      </div>
    );
  }
  