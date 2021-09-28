import { GetServerSideProps } from "next";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../../../store";
import FilePreview from "../../../components/Storage/FilePreview";
import { FileObject } from "../../../interfaces/storage";
import { WorkItem, WorkTag } from "../../../interfaces/work";
import { UserInfo } from "../../../interfaces/account";
import { axios } from "../../../utils/axios";
import { Button, Fab, TextField, Grid, Zoom } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import SaveIcon from "@mui/icons-material/Save";
import UploadFile from "../../../components/Storage/UploadFile";
import { useTheme } from "@mui/material/styles";
import { useRouter } from "next/dist/client/router";

const WorkItemPage = (props: WorkItemPageProps) => {
  const router = useRouter();
  const theme = useTheme();
  const transitionDuration = {
    enter: theme.transitions.duration.enteringScreen,
    exit: theme.transitions.duration.leavingScreen,
  };
  const user = useSelector((state: RootState) => state.user);
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
    const userInfo: UserInfo = user.user;
    if (props.data.user === userInfo.id) setEditable(true);
  }, []);
  const onUploaded = (fileObject: FileObject) => {
    console.log(fileObject.file_name);
    setEditFiles([...editFiles, fileObject]);
  };
  const onSave = () => {
    const putData: WorkItem = {
      id: props.data.id,
      name: nameField,
      intro: introField,
      user: props.data.user,
      tools: [],
      tags: [],
      files: editFiles.map((file) => file.id),
    };
    axios
      .put(`/v1/work/item/${props.data.id}/`, putData, {
        headers: {
          Authorization: "JWT " + localStorage.getItem("jwt"),
        },
      })
      .then((res) => {
        router.reload();
      })
      .catch((error) => {
        alert(`保存に失敗 ${error.message}`);
      });
  };
  return (
    <Grid container alignItems="center" justifyContent="center">
      {editMode ? (
        <Grid item xs={11}>
          <h1>Edit Work</h1>
          <TextField
            required
            label="作品名"
            fullWidth
            onChange={handleOnChangeNameField}
            defaultValue={nameField}
            className="mt-2"
          />
          <TextField
            required
            label="作品説明"
            fullWidth
            multiline
            maxRows={4}
            onChange={handleOnChangeIntroField}
            defaultValue={introField}
            className="mt-2"
          />
          <div className="mt-2">
            {editFiles.map((file) => (
              <FilePreview fileUrl={file.file_url} fileName={file.file_name} />
            ))}
          </div>
          <UploadFile onUploaded={onUploaded} targetContainer="work-item" />
        </Grid>
      ) : (
        <Grid item xs={11}>
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
          <p>{props.data.intro}</p>
          {props.files.map((file) => (
            <FilePreview fileUrl={file.file_url} fileName={file.file_name} />
          ))}
        </Grid>
      )}
      {editable ? (
        <>
          <Zoom
            in={editMode}
            timeout={transitionDuration}
            style={{
              transitionDelay: `${editMode ? transitionDuration.exit : 0}ms`,
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
              onClick={onSave}
            >
              <SaveIcon />
            </Fab>
          </Zoom>
          <Zoom
            in={!editMode}
            timeout={transitionDuration}
            style={{
              transitionDelay: `${!editMode ? transitionDuration.exit : 0}ms`,
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
                setEditMode(true);
              }}
            >
              <EditIcon />
            </Fab>
          </Zoom>
        </>
      ) : (
        <></>
      )}
    </Grid>
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

const fab = {
  position: "absolute",
  bottom: "16",
  right: "16",
};
