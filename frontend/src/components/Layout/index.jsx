import { useState } from "react";
import { Outlet } from "react-router-dom";

import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

import AddIcon from "@mui/icons-material/Add";

import UploadDialog from "../UploadDialog";

export default function Layout() {
  const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false);

  const handleUpload = () => {
    setIsUploadDialogOpen(true);
  };

  const handleDialogClose = () => {
    setIsUploadDialogOpen(false);
  };

  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="fixed" sx={{ top: 0, width: "100%" }}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              GuruDocs
            </Typography>
            <div>
              <Button
                size="medium"
                variant="contained"
                color="primary"
                onClick={handleUpload}
              >
                <AddIcon sx={{ mr: 1 }} />
                Upload
              </Button>
            </div>
          </Toolbar>
        </AppBar>
      </Box>
      {isUploadDialogOpen ? (
        <UploadDialog
          open={isUploadDialogOpen}
          handleClose={handleDialogClose}
        />
      ) : null}
      <Outlet />
    </>
  );
}
