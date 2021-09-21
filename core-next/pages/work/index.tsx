import { axios } from "../../utils/axios";
import Link from "next/link";
import { useState } from "react";
import { makeStyles, useTheme } from "@mui/material/styles";
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
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { ArrowBack } from "@mui/icons-material";
import NewWork from "../../components/Work/NewWork";

const WorkIndexPage = (props: { data: WorkItemList }) => {
  const theme = useTheme();
  const transitionDuration = {
    enter: theme.transitions.duration.enteringScreen,
    exit: theme.transitions.duration.leavingScreen,
  };
  const [workItems, setWorkItems] = useState<WorkItem[]>(props.data.results);
  const [workNextUrl, setWorkNextUrl] = useState(props.data.next);
  const [newMode, setNewMode] = useState(false);
  const loader = (
    <div className="loader" key={0}>
      Loading ...
    </div>
  );
  const loadNext = async () => {
    console.log(workNextUrl);
    const resData = axios.get(workNextUrl);
    const data: WorkItemList = (await resData).data;
    setWorkNextUrl(data.next);
    setWorkItems(workItems.concat(data.results));
  };
  return (
    <Grid>
      {newMode ? (
        <>
          <NewWork />
        </>
      ) : (
        <>
          <Grid>
            <h1>Work</h1>
          </Grid>
          <InfiniteScroll
            loadMore={loadNext}
            hasMore={workNextUrl !== null}
            loading={loader}
          >
            <Grid>
              {workItems.map((workItem) => (
                <Grid key={workItem.id}>
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
        </>
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
    </Grid>
  );
};

export default WorkIndexPage;

export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    console.log("hello");
    const resData = axios.get("/v1/work/item");
    const data: WorkItemList = (await resData).data;
    console.log(data);
    return { props: { data } };
  } catch (error) {
    console.log(error.message);
    return { props: { error: error.message } };
  }
};
