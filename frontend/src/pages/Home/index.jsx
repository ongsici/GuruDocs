import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import SummarizeIcon from '@mui/icons-material/Summarize';
import ChatIcon from '@mui/icons-material/Chat';
import { useParams } from 'react-router';

import Summary from "../../components/Summary";
import ChatBot from "../../components/ChatBot"


export default function Home({ model, setModel, pagesUuidList, setPagesUuidList, vectorstoreUuidList, setVectorstoreUuidList, fileName, setFileName}) {
  console.log("model", model)
  console.log("vector", vectorstoreUuidList)
  return (
    <Grid container justifyContent="center" my={10} rowGap={3}>
      <Grid item xs={12}>
        <Grid container>
          <Typography component="p" variant="h5">
            <SummarizeIcon sx={{ mr: 1 }} />
            Summary
          </Typography>
          <Summary 
          model={model} 
          setModel={setModel} 
          pagesUuidList={pagesUuidList} 
          setPagesUuidList={setPagesUuidList}
          fileName={fileName}
          setFileName={setFileName} />
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container>
          <Typography component="p" variant="h5">
            <ChatIcon sx={{ mr: 1}} />
            Chat with your documents
          </Typography>
            <Grid container justifyContent="center" item xs={12}>
              <ChatBot 
              model={model} 
              setModel={setModel}
              vectorstoreUuidList={vectorstoreUuidList}
              setVectorstoreUuidList={setVectorstoreUuidList} />
            </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}
