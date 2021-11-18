import {
  Button,
  Grid,
} from "@mui/material";
import Breadcrumbs from "../../components/Common/Breadcrumbs";

const SettingIndexPage = () => {
  return(
    <Grid container alignItems="center" justifyContent="center">
      <Grid item xs={12} sm={11}>
        <Breadcrumbs links={[{name: "Setting"}]} />
        <h1>Setting</h1>
        <Button href="/storage">ストレージの管理</Button>
      </Grid>
    </Grid>
  );
}

export default SettingIndexPage;