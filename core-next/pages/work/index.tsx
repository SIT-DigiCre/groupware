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
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { ArrowBack } from "@mui/icons-material";
import NewWork from "../../components/Work/NewWork";
import useSWR from "swr";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import Breadcrumbs from "../../components/Common/Breadcrumbs";

const WorkIndexPage = () => {
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
  const { data } = useSWR(["/v1/work/item", token.jwt], fetcher);
  useEffect(() => {
    if (data) {
      setWorkItems(data.result);
      setWorkNextUrl(data.next);
    }
  }, [data]);
  return (
    <>
      {newMode ? (
        <>
          <NewWork />
        </>
      ) : (
        <Grid container alignItems="center" justifyContent="center">
          <Grid item xs={11}>
            <Breadcrumbs links={[{name: "Work"}]} />
            <Paper>
              <Button 
                variant="contained" 
                onClick={()=>{setNewMode(true)}} 
                style={{margin:"5px"}}>
                  New Work Items
              </Button>
              <Button 
                variant="contained" 
                href="/work/myworkitems" 
                style={{margin:"5px"}}>
                  My Work Items
              </Button>
            </Paper>
            <h1>WorkItems</h1>
            <InfiniteScroll
              loadMore={loadNext}
              hasMore={workNextUrl !== null}
              loading={loader}
            >
              <Grid>
                {workItems.map((workItem) => (
                  <Grid key={workItem.id} className="mt-2">
                    <Link href={"/work/item/" + String(workItem.id)}>
                      <Card sx={{ minWidth: 275 }}>
                        <CardContent>
                          <Typography variant="h5">{workItem.name}</Typography>
                          <div>
                            {String(workItem.tags)}
                            <TagList tagIds={workItem.tags} />
                          </div>
                        </CardContent>
                      </Card>
                    </Link>
                  </Grid>
                ))}
              </Grid>
            </InfiniteScroll>
          </Grid>
        </Grid>
      )}
      <>
        <Zoom
          in={newMode}
          timeout={transitionDuration}
          style={{
            transitionDelay: `${newMode ? transitionDuration.exit : 0}ms`,
          }}
          unmountOnExit
        >
          <Fab
            sx={{
              position: "absolute",
              bottom: 16,
              right: 16,
            }}
            color="primary"
            onClick={() => {
              setNewMode(false);
            }}
          >
            <ArrowBack />
          </Fab>
        </Zoom>
        <Zoom
          in={!newMode}
          timeout={transitionDuration}
          style={{
            transitionDelay: `${!newMode ? transitionDuration.exit : 0}ms`,
          }}
          unmountOnExit
        >
          <Fab
            sx={{
              position: "absolute",
              bottom: 16,
              right: 16,
            }}
            color="primary"
            onClick={() => {
              setNewMode(true);
            }}
          >
            <AddIcon />
          </Fab>
        </Zoom>
      </>
    </>
  );
};

export default WorkIndexPage;
