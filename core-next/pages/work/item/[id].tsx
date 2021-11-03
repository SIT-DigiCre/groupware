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
import { Markdown } from "../../../components/Common/Markdown";
import useSWR from "swr";
import Breadcrumbs from "../../../components/Common/Breadcrumbs";

const WorkItemPage = (props: WorkItemPageProps) => {
  const router = useRouter();
  const theme = useTheme();
  const transitionDuration = {
    enter: theme.transitions.duration.enteringScreen,
    exit: theme.transitions.duration.leavingScreen,
  };
  const user = useSelector((state: RootState) => state.user.user);
  const token = useSelector((state: RootState) => state.token.token);
  const [editable, setEditable] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [nameField, setNameField] = useState<string>();
  const [introField, setIntroField] = useState<string>();
  const [editFiles, setEditFiles] = useState<FileObject[]>();
  const fetcher = async (url: string, token: string | null) => {
    if (token) {
      const res = await axios.get(url, {
        headers: { Authorization: "JWT " + token },
      });
      return res.data;
    } else {
      return null;
    }
  };
  const { data: workItem } = useSWR(
    [`/v1/work/item/${props.id}`, token.jwt],
    fetcher
  );
  const [workTags, setWorkTags] = useState<WorkTag[] | null>();
  const [files, setFiles] = useState<FileObject[] | null>();
  useEffect(() => {
    (async () => {
      if (workItem && token.jwt) {
        let tags = [];
        for (const url of workItem.tags.map(
          (tagId: number) => `/v1/work/tag/${tagId}`
        )) {
          tags.push(await fetcher(url, token.jwt));
        }
        setWorkTags(tags);
        let files = [];
        for (const url of workItem.files.map(
          (fileId: number) => `/v1/storage/fileobject/${fileId}`
        )) {
          files.push(await fetcher(url, token.jwt));
        }
        setFiles(files);
      }
    })();
  }, [workItem]);
  const handleOnChangeNameField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setNameField(e.target.value);
  const handleOnChangeIntroField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setIntroField(e.target.value);
  useEffect(() => {
    const userInfo = user;
    if (!workItem) return;
    if (userInfo && workItem.id === userInfo.id) setEditable(true);
  }, [user, workItem]);
  const onUploaded = (fileObject: FileObject) => {
    console.log(fileObject.file_name);
    setEditFiles([...editFiles, fileObject]);
  };
  const onSave = () => {
    const putData: WorkItem = {
      id: workItem.id,
      name: nameField,
      intro: introField,
      user: workItem.user,
      tools: [],
      tags: [],
      files: editFiles.map((file) => file.id),
    };
    axios
      .put(`/v1/work/item/${workItem.id}/`, putData, {
        headers: {
          Authorization: "JWT " + token.jwt,
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
    <>
      {workItem ? (
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
                  <FilePreview
                    fileUrl={file.file_url}
                    fileName={file.file_name}
                  />
                ))}
              </div>
              <UploadFile onUploaded={onUploaded} targetContainer="work-item" />
            </Grid>
          ) : (
            <Grid item xs={11}>
              <Breadcrumbs links={[{name: "Work", url:"/work"}, {name: "Item"}, {name: workItem.name}]} />
              <h1>{workItem.name}</h1>
              <div
                style={{
                  display: "inline",
                  marginLeft: "8px",
                  marginBottom: "3px",
                }}
              >
                {workTags ? (
                  workTags.map((tag) => (
                    <span
                      className="badge rounded-pill bg-primary"
                      style={{ display: "inline", marginLeft: "1px" }}
                    >
                      {tag.name}
                    </span>
                  ))
                ) : (
                  <></>
                )}
              </div>
              <Markdown md={workItem.intro} />
              {files ? (
                files.map((file) => (
                  <FilePreview
                    fileUrl={file.file_url}
                    fileName={file.file_name}
                  />
                ))
              ) : (
                <></>
              )}
            </Grid>
          )}
          {editable ? (
            <>
              <Zoom
                in={editMode}
                timeout={transitionDuration}
                style={{
                  transitionDelay: `${
                    editMode ? transitionDuration.exit : 0
                  }ms`,
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
                  transitionDelay: `${
                    !editMode ? transitionDuration.exit : 0
                  }ms`,
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
      ) : (
        <p>loading</p>
      )}
    </>
  );
};
export default WorkItemPage;

type WorkItemPageProps = {
  id?: number;
  errors?: any;
};
export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const id = params?.id;
    return { props: { id } };
  } catch (error) {
    return { props: { errors: error.message } };
  }
};

const fab = {
  position: "absolute",
  bottom: "16",
  right: "16",
};
