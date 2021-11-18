import { axios } from "../../utils/axios";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import useSWR from "swr";
import { useEffect } from "react";
import { FileObject } from "../../interfaces/storage";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import DeleteIcon from '@mui/icons-material/Delete';
import { useRouter } from "next/dist/client/router";
import {
  IconButton,
  Grid,
} from "@mui/material";
import Breadcrumbs from "../../components/Common/Breadcrumbs";

const fetcher = async (url: string, token: string | null) => {
  if (token) {
    const res = await axios.get(url, {
      headers: { Authorization: "JWT " + token },
    });
    return res.data;
  } else {
    return null;
  }
}

const StorageIndexPage = () => {
  const router = useRouter();
  const user = useSelector((state: RootState) => state.user.user);
  const token = useSelector((state: RootState) => state.token.token);
  let { data: fileObjects } = useSWR(["/v1/storage/myfileobject/", token.jwt], fetcher);
  //if (error) return <div>FAILED</div>;
  if (!fileObjects) return <div>LOADING</div>;
  const deleteFileObject = (target: FileObject) => {
    axios.delete(`/v1/storage/myfileobject/${target.id}/`, {
      headers: { Authorization: "JWT " + token.jwt },
    }).then(res => {
      router.reload();
    })
  }
  return (
    <Grid container alignItems="center" justifyContent="center">
      <Grid item xs={12} sm={11}>
        <Breadcrumbs links={[{name: "Storage"}]} />
        <h1>MyStorage</h1>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 450 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>ファイル名</TableCell>
                <TableCell align="right">作成日</TableCell>
                <TableCell align="right">削除</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {fileObjects.map((fileObject) => (
                <TableRow
                  key={fileObject.id}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    <a href={fileObject.file_url}>{fileObject.file_name}</a>
                  </TableCell>
                  <TableCell align="right">{fileObject.created_at}</TableCell>
                  <TableCell align="right">
                    <IconButton
                      aria-label="delete"
                      onClick={() => { deleteFileObject(fileObject) }}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </Grid>
  );
}
export default StorageIndexPage;