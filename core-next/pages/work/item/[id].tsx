import { GetServerSideProps } from "next";
import { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import FilePreview from "../../../components/Storage/FilePreview";
import { FileObject } from "../../../interfaces/storage";
import { WorkItem, WorkTag } from "../../../interfaces/work";
import { UserInfo } from "../../../interfaces/account";
import { axios } from "../../../utils/axios";
import { Button, Fab, makeStyles, TextField } from "@material-ui/core";
import EditIcon from "@material-ui/icons/Edit";
import SaveIcon from "@material-ui/icons/Save";
import UploadFile from "../../../components/Storage/UploadFile";

const WorkItemPage = (props: WorkItemPageProps) => {
  const classes = useStyles();
  const [editable, setEditable] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [nameField, setNameField] = useState(props.data.name);
  const [introField, setIntroField] = useState(props.data.intro);
  const [editFiles, setEditFiles] = useState(props.files);
  const handleOnChangeNameField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setNameField(e.target.value);
  const handleOnChangeIntroField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setIntroField(e.target.value);
  useEffect(() => {
    const json = localStorage.getItem("user-info");
    if (json === undefined) return;
    const userInfo: UserInfo = JSON.parse(json);
    if (props.data.user === userInfo.id) setEditable(true);
  }, []);
  const onUploaded = (fileObject: FileObject) => {
    console.log(fileObject.file_name);
    setEditFiles([...editFiles, fileObject]);
  };
  const onSave = () => {
    axios;
  };
  return (
    <Container>
      {editMode ? (
        <>
          <Row>
            <h1>Edit Work</h1>
          </Row>
          <Row>
            <TextField
              required
              label="作品名"
              fullWidth
              onChange={handleOnChangeNameField}
              defaultValue={nameField}
            />
          </Row>
          <Row>
            <TextField
              required
              label="作品説明"
              fullWidth
              multiline
              maxRows={4}
              onChange={handleOnChangeIntroField}
              defaultValue={introField}
            />
          </Row>
          <Row>
            {editFiles.map((file) => (
              <FilePreview fileUrl={file.file_url} fileName={file.file_name} />
            ))}
          </Row>

          <Row className="mt-2">
            <UploadFile onUploaded={onUploaded} targetContainer="work-item" />
          </Row>
          <Fab
            color="primary"
            aria-label="add"
            className={classes.fab}
            onClick={() => {
              setEditMode(true);
            }}
          >
            <SaveIcon />
          </Fab>
        </>
      ) : (
        <>
          <Row>
            <h1>{props.data.name}</h1>
            <div
              style={{
                display: "inline",
                marginLeft: "8px",
                marginBottom: "3px",
              }}
            >
              {props.tags.map((tag) => (
                <span
                  className="badge rounded-pill bg-primary"
                  style={{ display: "inline", marginLeft: "1px" }}
                >
                  {tag.name}
                </span>
              ))}
            </div>
          </Row>
          <Row>
            <p>{props.data.intro}</p>
          </Row>
          {props.files.map((file) => (
            <FilePreview fileUrl={file.file_url} fileName={file.file_name} />
          ))}
          {editable ? (
            <Fab
              color="primary"
              aria-label="add"
              className={classes.fab}
              onClick={() => {
                setEditMode(true);
              }}
            >
              <EditIcon />
            </Fab>
          ) : (
            <></>
          )}
        </>
      )}
    </Container>
  );
};
export default WorkItemPage;

type WorkItemPageProps = {
  data?: WorkItem;
  tags?: WorkTag[];
  files?: FileObject[];
  errors?: any;
};
export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const id = params?.id;
    const resData = axios.get("/v1/work/item/" + String(id));
    const data: WorkItem = (await resData).data;
    const tags: WorkTag[] = await Promise.all(
      data.tags.map(
        async (tagId) => (await axios.get("/v1/work/tag/" + String(tagId))).data
      )
    );
    const files: FileObject[] = await Promise.all(
      data.files.map(
        async (fileId) =>
          (
            await axios.get("/v1/storage/fileobject/" + String(fileId))
          ).data
      )
    );
    return { props: { data, tags, files } };
  } catch (error) {
    return { props: { errors: error.message } };
  }
};

const useStyles = makeStyles((theme) => ({
  fab: {
    position: "absolute",
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
}));
