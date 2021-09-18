import { Row, Col } from "react-bootstrap";
import { TextField, Button } from "@material-ui/core";
import { CloudUpload } from "@material-ui/icons";
import { Tool } from "../../interfaces/tool";
import { useState } from "react";
import { WorkTag } from "../../interfaces/work";
import { FileObject } from "../../interfaces/strage";
import UploadFile from "../Strage/UploadFile";
import FilePreview from "../Strage/FilePreview";
const NewWork = () => {
  const [tools, setTools] = useState<Tool[]>([]);
  const [tags, setTags] = useState<WorkTag[]>([]);
  const [files, setFiles] = useState<FileObject[]>([]);

  const onUploaded = (fileObject: FileObject) => {
    console.log(fileObject.file_name);
    const tmpFiles = files;
    tmpFiles.push(fileObject);
    setFiles([...files, fileObject]);
    console.log(tmpFiles);
  };
  return (
    <>
      <Row>
        <h1>New Work</h1>
      </Row>
      <Row>
        <TextField required label="作品名" fullWidth />
      </Row>
      <Row>
        <TextField required label="作品説明" fullWidth multiline maxRows={4} />
      </Row>
      <Row>
        {files.map((file) => (
          <FilePreview fileKind={file.kind} fileUrl={file.file_url} />
        ))}
      </Row>

      <Row className="mt-2">
        <UploadFile onUploaded={onUploaded} targetContainer="work-item" />
      </Row>
    </>
  );
};
export default NewWork;
