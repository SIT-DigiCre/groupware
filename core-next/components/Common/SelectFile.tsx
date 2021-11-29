import { Dialog, DialogTitle, Button, Stack } from "@mui/material";
import { useState } from "react";
import { FileObject } from "../../interfaces/storage"
import UploadFile from "../Storage/UploadFile";

type Props = {
  title?: string;
  onClose?: () => void;
  onClickAdd: (fileObject: FileObject) => void;
}
const SelectFile = (props: Props) => {
  const [mode, setMode] = useState("none");
  return (
    <>
      <Dialog onClose={props.onClose} open={true}>
        {props.title ? <DialogTitle>{props.title}</DialogTitle> : <DialogTitle>ファイル選択</DialogTitle>}
        {mode === "none" ?
          <Stack direction="row" spacing={2} style={{ margin: "3px auto" }} >
            <Button variant="contained" onClick={() => { setMode("upload") }} >アップロード</Button>
            {/*<Button variant="contained" onClick={() => { setMode("select") }}>既存のものから選択</Button>*/}
          </Stack>
          :
          <>
            {mode === "upload" ?
              <UploadFile onUploaded={props.onClickAdd} targetContainer="img"/>
              :

              <Button>選択</Button>
            }
          </>
        }

      </Dialog>
    </>
  )
}

export default SelectFile;