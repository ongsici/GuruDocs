/* eslint-disable react-hooks/exhaustive-deps */
import { useRef, useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import Typography from "@mui/material/Typography";

import { REACT_APP_BACKEND_URL } from "../../config";
import { useFetch } from "../../hooks/useFetch";
import { CircularProgress } from "@mui/material";

const DEFAULT_MODEL_VALUE = "llama2";

export default function UploadDialog({ open, handleClose, model, setModel, pagesUuidList, setPagesUuidList, vectorstoreUuidList, setVectorstoreUuidList, fileName, setFileName }) {
  const fileRef = useRef(null);
  const [files, setFiles] = useState(null);
  const handleFileChange = (event) => {
    setFiles(event.target.files);
  };
  const handleUpload = () => {
    fileRef.current.click();
  };

  const handleModelChange = (event) => {
    setModel(event.target.value);
  };


  const {
    success: postFilesSuccess,
    loading: postFilesLoading,
    error: postFilesError,
    data: postFilesResponse,
    renderFetch: postFiles,
  } = useFetch(`${REACT_APP_BACKEND_URL}/embed`, "POST");

  const handleSubmit = (event) => {
    event.preventDefault();

    const fileBase64StringArr = [];

    if (files?.length > 0) {
      [...files].forEach((file) => {
        const reader = new FileReader();
        const filename = file.name;
        setFileName(filename)

        reader.onload = function (e) {
          const base64String = btoa(e.target.result);
          fileBase64StringArr.push(base64String);

          if (fileBase64StringArr.length === files.length) {
            postFiles({ model, files: fileBase64StringArr });
          }

        };

        reader.readAsBinaryString(file);
      });
    }
  };

  useEffect(() => {
    if (postFilesSuccess && postFilesResponse) {
      setPagesUuidList(postFilesResponse.pages_uuid_list); 
      setVectorstoreUuidList(postFilesResponse.vectorstore_uuid_list);
      handleClose();
    }
  }, [postFilesSuccess,postFilesResponse]);

  if (postFilesLoading) {
    const embedDescription = "Embedding your documents..."
    return (
      <Dialog
        open={open}
        onClose={handleClose}
        PaperProps={{
          component: "form",
          onSubmit: handleSubmit,
        }}
      >
        <Box m={20} textAlign="center">
          <CircularProgress />
          <Typography variant="body1" mt={2}>{embedDescription}</Typography>
        </Box>
      </Dialog>
    );
  }

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      PaperProps={{
        component: "form",
        onSubmit: handleSubmit,
      }}
    >
      <DialogTitle>Upload your documents</DialogTitle>

      <DialogContent>
        {postFilesError ? (
          <DialogContentText color="error">An error occurred</DialogContentText>
        ) : null}

        <Box my={2}>
          <DialogContentText>
            <b>Upload your PDFs here and click on 'Process'</b>
          </DialogContentText>
          <input
            ref={fileRef}
            style={{ display: "none" }}
            // multiple
            type="file"
            accept="application/msword, application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            onChange={handleFileChange}
          />
          <Button
            variant="outlined"
            startIcon={<CloudUploadIcon />}
            onClick={handleUpload}
          >
            Upload
          </Button>
        </Box>

        <Box my={2}>
          <DialogContentText>
            <b>Choose Model</b>
          </DialogContentText>
          <FormControl>
            <FormLabel id="model-group-label">Choose your model:</FormLabel>
            <RadioGroup
              aria-labelledby="model-group-label"
              defaultValue={DEFAULT_MODEL_VALUE}
              name="model-group"
              onChange={handleModelChange}
            >
              <FormControlLabel
                value="llama2"
                control={<Radio />}
                label="llama2"
              />
              <FormControlLabel
                value="mistral"
                control={<Radio />}
                label="mistral"
              />
            </RadioGroup>
          </FormControl>
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button type="submit">Process</Button>
      </DialogActions>
    </Dialog>
  );
}
