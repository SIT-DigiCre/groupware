import { Row, Col } from "react-bootstrap";
import { TextField, Button } from "@material-ui/core";
import { CloudUpload } from "@material-ui/icons";
import { Tool } from "../../interfaces/tool";
import React, { useState } from "react";
import { WorkTag, WorkItem } from "../../interfaces/work";
import { FileObject } from "../../interfaces/storage";
import UploadFile from "../Storage/UploadFile";
import FilePreview from "../Storage/FilePreview";
import SaveIcon from "@material-ui/icons/Save";
import { axios } from "../../utils/axios";
const NewWork = () => {
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
    axios.post("/v1/work/item/", item, {
      headers: {
        Authorization: "JWT " + localStorage.getItem("jwt"),
      },
    });
  };
  return (
    <>
      <Row>
        <h1>New Work</h1>
      </Row>
      <Row>
        <TextField
          required
          label="作品名"
          fullWidth
          onChange={handleOnChangeNameField}
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
        />
      </Row>
      <Row>
        {files.map((file) => (
          <FilePreview fileUrl={file.file_url} fileName={file.file_name} />
        ))}
      </Row>

      <Row className="mt-2">
        <UploadFile onUploaded={onUploaded} targetContainer="work-item" />
      </Row>
      <Row className="mt-2">
        <Button
          variant="contained"
          color="primary"
          size="large"
          startIcon={<SaveIcon />}
          onClick={onSave}
        >
          Save
        </Button>
      </Row>
    </>
  );
};
export default NewWork;
