import { axios } from "../../utils/axios";
import Link from "next/link";
import { useState } from "react";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import { Container, Row, Col, Card } from "react-bootstrap";
import { WorkItem, WorkTag, WorkItemList } from "../../interfaces/work";
import InfiniteScroll from "react-infinite-scroller";
import TagList from "../../components/Work/TagList";
import { GetServerSideProps } from "next";
import { Fab, IconButton, Button } from "@material-ui/core";
import AddIcon from "@material-ui/icons/Add";
import { ArrowBack } from "@material-ui/icons";
import NewWork from "../../components/Work/NewWork";

const WorkIndexPage = (props: { data: WorkItemList }) => {
  const classes = useStyles();
  const theme = useTheme();
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
    <Container>
      {newMode ? (
        <>
          <NewWork />
          <Fab
            color="primary"
            aria-label="add"
            className={classes.fab}
            onClick={() => {
              setNewMode(false);
            }}
          >
            <ArrowBack />
          </Fab>
        </>
      ) : (
        <>
          <Row>
            <h1>Work</h1>
          </Row>
          <InfiniteScroll
            loadMore={loadNext}
            hasMore={workNextUrl !== null}
            loading={loader}
          >
            <Row>
              {workItems.map((workItem) => (
                <Col md={4} sm={6} className="mt-2" key={workItem.id}>
                  <Link href={"/work/item/" + String(workItem.id)}>
                    <Card>
                      <Card.Body>
                        <Card.Title>{workItem.name}</Card.Title>
                        <div>
                          {String(workItem.tags)}
                          <TagList tagIds={workItem.tags} />
                        </div>
                      </Card.Body>
                    </Card>
                  </Link>
                </Col>
              ))}
            </Row>
          </InfiniteScroll>
          <Fab
            color="primary"
            aria-label="add"
            className={classes.fab}
            onClick={() => {
              setNewMode(true);
            }}
          >
            <AddIcon />
          </Fab>
        </>
      )}
    </Container>
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

const useStyles = makeStyles((theme) => ({
  fab: {
    position: "absolute",
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
}));
