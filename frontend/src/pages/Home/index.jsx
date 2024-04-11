import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Summary from "../../components/Summary";


export default function Home() {
  return (
    <Grid container justifyContent="center" my={10} rowGap={3}>
      <Grid item xs={12}>
        <Grid container>
          <Typography component="p" variant="h5">
            Summary
          </Typography>
          {/* <Summary /> */}
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
