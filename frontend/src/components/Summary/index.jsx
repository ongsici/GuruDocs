/* eslint-disable react-hooks/exhaustive-deps */
import React,{ useRef, useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { REACT_APP_BACKEND_URL } from "../../config";
import { useFetch } from "../../hooks/useFetch";
import { CircularProgress, Card, CardContent } from "@mui/material";


export default function Summary({ model, setModel, pagesUuidList, setPagesUuidList, fileName, setFileName }) {
    const [summaries, setSummaries] = useState([]);
  
    const {
        loading: postFilesLoading,
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
      const sumDescription = "Generating document summary..."
        return (
            <Box m={10} textAlign="center">
              <CircularProgress />
              <Typography variant="body1" mt={2}>{sumDescription}</Typography>
            </Box>
        );
      }

    const formatSummary = (summary) => {
      return summary.split('\n').map((line, index) => <React.Fragment key={index}>{line}<br /></React.Fragment>);
    };
    
    return (
      <div>
          {summaries.map((summary, index) => (
              <Card key={index} style={{ marginBottom: '10px' }}>
                  <CardContent>
                      <Typography variant="h6" gutterBottom>
                          {fileName}
                      </Typography>
                      <Typography variant="body1">
                          {formatSummary(summary)}
                      </Typography>
                  </CardContent>
              </Card>
          ))}
      </div>
    );
  }
  