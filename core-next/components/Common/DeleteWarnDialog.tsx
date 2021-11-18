import { Dialog, DialogTitle, Button, Stack } from "@mui/material";

type Props = {
  title?: string;
  onClose?: ()=>void;
  open: boolean;
  onClickDelete: ()=>void;
  onClickCancel: ()=>void;
}

const DeleteWarnDialog = (props: Props) => {
  return (
    <Dialog onClose={props.onClickCancel} open={props.open}>
      {props.title ? <DialogTitle>{props.title}</DialogTitle> : <DialogTitle>削除しますか</DialogTitle> }
      <Stack direction="row" spacing={2} style={{margin:"3px auto"}} >
      <Button variant="contained" color="error" onClick={props.onClickDelete} >削除</Button>
      <Button variant="contained" onClick={props.onClickCancel}>キャンセル</Button>
      </Stack>
    </Dialog>
  )
}

export default DeleteWarnDialog;