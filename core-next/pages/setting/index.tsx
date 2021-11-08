import {
  Button,
  Grid,
} from "@mui/material";

const SettingIndexPage = () => {
  return(
    <Grid container alignItems="center" justifyContent="center">
      <Grid item xs={12} sm={11}>
        <h1>Setting</h1>
        <Button href="/storage">ストレージの管理</Button>
      </Grid>
    </Grid>
  );
}

export default SettingIndexPage;