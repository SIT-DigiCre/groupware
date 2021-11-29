import { AddOutlined } from "@mui/icons-material";
import { Button, Fab, TextField, Grid, Zoom, Chip, Stack } from "@mui/material";
import { useState } from "react";
import { FileObject } from "../../interfaces/storage";
import { Markdown } from "./Markdown";
import SelectFile from "./SelectFile";
const MarkdownEditor = (props: { default: string, label: string, onChange: (md: string) => void }) => {
  const [md, setMd] = useState(props.default);
  const handleOnChangeContentField = (e: React.ChangeEvent<HTMLInputElement>) => {
    props.onChange(e.target.value);
    setMd(e.target.value);
  }
  const insertText = (kind: string) => {
    switch (kind) {
      case 'H1':
        document.execCommand('insertText', false, '\n# H1');
        return;
      case 'H2':
        document.execCommand('insertText', false, '\n## H2');
        return;
      case 'H3':
        document.execCommand('insertText', false, '\n### H3');
        return;
      case 'IMG':
        document.execCommand('insertText', false, '\n![デジクリ](https://digicre.net/image/omochabako.png)');
        return;
    }

  }
  const addImg = (fileObject: FileObject) => {
    document.execCommand('insertText', false, '\n!['+fileObject.file_name+']('+fileObject.file_url+')');
    SetImgDialogOpen(false);
  }
  const [imgDialogOpen, SetImgDialogOpen] = useState(false);
  const insertList = ['H1', 'H2', 'H3', 'IMG'];
  return (
    <Grid container>
      <Grid item xs={12}>
        <div>
          {insertList.map(i => (
            <Button onClick={()=>{insertText(i)}}>{i}</Button>
          ))}
          <Button onClick={()=>{SetImgDialogOpen(true)}}>画像追加</Button>
          {imgDialogOpen ? <SelectFile onClickAdd={addImg} onClose={()=>{SetImgDialogOpen(false)}}/> : <></>}
        </div>
      </Grid>
      <Grid item xs={6}>
        <TextField
          required
          label={props.label}
          fullWidth
          onChange={handleOnChangeContentField}
          defaultValue={md}
          multiline
          className="mt-2"
        />
      </Grid>
      <Grid item xs={6}>
        <Markdown md={md} />
      </Grid>

    </Grid>
  )
}

export default MarkdownEditor;