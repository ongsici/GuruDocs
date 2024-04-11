/* eslint-disable react-hooks/exhaustive-deps */
import { useRef, useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { REACT_APP_BACKEND_URL } from "../../config";
import { useFetch } from "../../hooks/useFetch";
import { CircularProgress } from "@mui/material";


export default function Summary({ model, setModel, pagesUuidList, setPagesUuidList }) {
    const [summary, setSummary] = useState("");
  
    const {
        // success: postFilesSuccess,
        loading: postFilesLoading,
        // error: postFilesError,
        renderFetch: getSummary,
        data: postFilesResponse
      } = useFetch(`${REACT_APP_BACKEND_URL}/summary`, "POST");

    useEffect(() => {
      console.log(summary)
      console.log(4, pagesUuidList)
      if (!summary && pagesUuidList?.length > 0) {
        console.log('getsum')
        getSummary({ pages_id: pagesUuidList, model_option: model });
      }
    }, [summary, pagesUuidList, model]);
    
    useEffect(() => {
    if (postFilesResponse) {
        setSummary(postFilesResponse.summary);
    }
    }, [postFilesResponse]);

    // TODO: implement spinner when loading (see UploadDialog)
    if (postFilesLoading) {
        return (
            <Box m={5}>
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
  