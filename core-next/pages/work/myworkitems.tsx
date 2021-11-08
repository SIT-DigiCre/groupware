import { axios } from "../../utils/axios";
import Link from "next/link";
import { useState, useEffect } from "react";
import { useTheme } from "@mui/material/styles";
import { WorkItem, WorkTag, WorkItemList } from "../../interfaces/work";
import InfiniteScroll from "react-infinite-scroller";
import TagList from "../../components/Work/TagList";
import { GetServerSideProps } from "next";
import {
  Fab,
  IconButton,
  Button,
  Zoom,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  TableContainer,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Table,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { ArrowBack } from "@mui/icons-material";
import NewWork from "../../components/Work/NewWork";
import useSWR from "swr";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import Breadcrumbs from "../../components/Common/Breadcrumbs";
import DeleteIcon from '@mui/icons-material/Delete';
import DeleteWarnDialog from "../../components/Common/DeleteWarnDialog";
const MyWorkItemsPage = () => {
  const theme = useTheme();
  const token = useSelector((state: RootState) => state.token.token);
  const transitionDuration = {
    enter: theme.transitions.duration.enteringScreen,
    exit: theme.transitions.duration.leavingScreen,
  };
  const [workItems, setWorkItems] = useState<WorkItem[]>([]);
  const [workNextUrl, setWorkNextUrl] = useState("");
  const [newMode, setNewMode] = useState(false);
  const loader = (
    <div className="loader" key={0}>
      Loading ...
    </div>
  );
  const loadNext = async () => {
    if (workNextUrl === "") return;
    const resData = axios.get(workNextUrl);
    const data: WorkItemList = (await resData).data;
    setWorkNextUrl(data.next);
    setWorkItems(workItems.concat(data.results));
  };
  const fetcher = (url: string, token: string | null) => {
    if (token) {
      axios
        .get(url, { headers: { Authorization: "JWT " + token } })
        .then((res) => {
          setWorkItems(res.data.results);
          setWorkNextUrl(res.data.next);
          return res.data;
        });
    } else {
      return null;
    }
  };
  const { data } = useSWR(["/v1/work/myitem", token.jwt], fetcher);
  useEffect(() => {
    if (data) {
      setWorkItems(data.result);
      setWorkNextUrl(data.next);
    }
  }, [data]);


  return (

    <Grid container alignItems="center" justifyContent="center">
      <Grid item xs={11}>
        <Breadcrumbs links={[{name: "Work", url: "/work"}, {name: "MyWorkItems"}]} />
        <h1>My Work Items</h1>
        <InfiniteScroll
          loadMore={loadNext}
          hasMore={workNextUrl !== null}
          loading={loader}
        >
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

                {workItems.map((workItem) => (
                  <WorkItemRow workItem={workItem} />
                ))}

              </TableBody>
            </Table>
          </TableContainer>
        </InfiniteScroll>
      </Grid>

    </Grid>);
}
export default MyWorkItemsPage;

const WorkItemRow = (props: { workItem: WorkItem }) => {
  const [view, setView] = useState(true);
  const token = useSelector((state: RootState) => state.token.token);
  const [deleteWarnDialogOpen, setDeleteWarnDialog] = useState(false);
  const [deleteAllFileWarnDialogOpen, setDeleteAllFileWarnDialog] = useState(false);
  const deleteWorkItem = () => {
    axios.delete('v1/work/item/'+props.workItem.id , { headers: { Authorization: "JWT " + token.jwt } })
      .then((res) => {
        setView(false);
        setDeleteAllFileWarnDialog(true);

      })
  }
  const deleteAllFile = () => {
    props.workItem.files.map(file => {
      axios.delete('v1/storage/myfileobject/'+file, { headers: { Authorization: "JWT " + token.jwt } })
    })
    setDeleteAllFileWarnDialog(false);
  }
  return (
    <>
      {
        view ?
          <TableRow
            key={props.workItem.id}
            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
          >
            <TableCell component="th" scope="row">
              <Link href={"/work/item/" + String(props.workItem.id)}>{props.workItem.name}</Link>
            </TableCell>
            <TableCell align="right">{props.workItem.created_at}</TableCell>
            <TableCell align="right">
              <IconButton
                aria-label="delete"
                onClick={() => { setDeleteWarnDialog(true) }}>
                <DeleteIcon />
              </IconButton>
              <DeleteWarnDialog open={deleteWarnDialogOpen} onClickDelete={deleteWorkItem} onClickCancel={() => { setDeleteWarnDialog(false) }} />
              
            </TableCell>
          </TableRow >
          :
          <></>
      }
      <DeleteWarnDialog title="このWorkItemに紐付けられたファイルも削除しますか？" open={deleteAllFileWarnDialogOpen} onClickDelete={deleteAllFile} onClickCancel={() => { setDeleteAllFileWarnDialog(false) }} />
    </>
  )
}