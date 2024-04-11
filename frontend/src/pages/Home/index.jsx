import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { useParams } from 'react-router';

import Summary from "../../components/Summary";


export default function Home({ model, setModel, pagesUuidList, setPagesUuidList, vectorstoreUuidList, setVectorstoreUuidList }) {
  console.log(3, pagesUuidList)
  return (
    <Grid container justifyContent="center" my={10} rowGap={3}>
      <Grid item xs={12}>
        <Grid container>
          <Typography component="p" variant="h5">
            Summary
          </Typography>
          <Summary 
          model={model} 
          setModel={setModel} 
          pagesUuidList={pagesUuidList} 
          setPagesUuidList={setPagesUuidList} />
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <Grid container>
          <Typography component="p" variant="h5">
            Chat with your documents
          </Typography>
          {/* Chat content */}
        </Grid>
      </Grid>
    </Grid>
  );
}
