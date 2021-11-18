import { useSelector } from "react-redux";
import { RootState } from "../../store";
import { TextField, Button, Grid, Box } from "@mui/material";
import { CloudUpload } from "@mui/icons-material";
import { Tool } from "../../interfaces/tool";
import React, { useState } from "react";
import { WorkTag, WorkItem } from "../../interfaces/work";
import { FileObject } from "../../interfaces/storage";
import UploadFile from "../Storage/UploadFile";
import FilePreview from "../Storage/FilePreview";
import SaveIcon from "@mui/icons-material/Save";
import { axios } from "../../utils/axios";
import { useRouter } from "next/dist/client/router";
import Breadcrumbs from "../Common/Breadcrumbs";
const NewWork = () => {
  const router = useRouter();
  const token = useSelector((state: RootState) => state.token.token);
  const [tools, setTools] = useState<Tool[]>([]);
  const [tags, setTags] = useState<WorkTag[]>([]);
  const [files, setFiles] = useState<FileObject[]>([]);
  const [nameField, setNameField] = useState("");
  const [introField, setIntroField] = useState("");
  const handleOnChangeNameField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setNameField(e.target.value);
  const handleOnChangeIntroField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setIntroField(e.target.value);

  const onUploaded = (fileObject: FileObject) => {
    console.log(fileObject.file_name);
    setFiles([...files, fileObject]);
  };
  const onSave = () => {
    const fs = files.map((file) => console.log(file.id));
    console.log(fs);
    const item: WorkItem = {
      name: nameField,
      intro: introField,
      user: 1,
      tools: [],
      tags: [],
      files: files.map((file) => file.id),
    };
    console.log(item);
    axios
      .post("/v1/work/item/", item, {
        headers: {
          Authorization: "JWT " + token.jwt,
        },
      })
      .then((res) => {
        router.push(`/work/item/${res.data.id}`);
      })
      .catch((error) => {
        router.reload()
      });
  };
  return (
    <Grid container spacing={2} alignItems="center" justifyContent="center">
      <Grid item xs={11}>
        <Breadcrumbs links={[{name: "Work", url: "/work"}, {name: "NewWork"}]} />
        <h1>New Work</h1>
        <TextField
          required
          label="作品名"
          onChange={handleOnChangeNameField}
          variant="outlined"
          fullWidth
          className="mt-2"
        />
        <TextField
          required
          label="作品説明"
          multiline
          maxRows={4}
          onChange={handleOnChangeIntroField}
          variant="outlined"
          fullWidth
          className="mt-2"
        />
        <div className="mt-2">
          {files.map((file) => (
            <FilePreview fileUrl={file.file_url} fileName={file.file_name} />
          ))}
        </div>
        <UploadFile onUploaded={onUploaded} targetContainer="work-item" />
        <Button
          variant="contained"
          color="primary"
          size="large"
          startIcon={<SaveIcon />}
          onClick={onSave}
          className="mt-2"
          fullWidth
        >
          Save
        </Button>
      </Grid>
    </Grid>
  );
};
export default NewWork;
