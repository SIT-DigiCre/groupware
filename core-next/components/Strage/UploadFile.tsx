import { TextField, Button } from "@material-ui/core";
import { CloudUpload } from "@material-ui/icons";
import { FileObject } from "../../interfaces/strage";
import FileInputComponent from "react-file-input-previews-base64";
import { axios } from "../../utils/axios";

const UploadFile = (props: Props) => {
  const upload = (file) => {
    axios
      .post(
        "/v1/strage/fileobject/upload",
        {
          file_name: file.name,
          target_container: props.targetContainer,
          kind: checkKind(file.type),
          file: file.base64.split(",")[1],
        },
        {
          headers: {
            Authorization: "JWT " + localStorage.getItem("jwt"),
          },
        }
      )
      .then((res) => {
        const fileObject: FileObject = {
          id: res.data.id,
          file_name: res.data.file_name,
          file_url: res.data.file_url,
          kind: res.data.kind,
        };
        props.onUploaded(fileObject);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <>
      <FileInputComponent
        parentStyle={{}} //スタイル
        imagePreview={false} //ファイルのプレビュー
        multiple={false} //複数ファイル選択
        callbackFunction={(file) => {
          //選択後のコールバック関数
          console.log(file);
          upload(file);
        }}
        buttonComponent={
          <Button
            variant="contained"
            color="default"
            startIcon={<CloudUpload />}
          >
            Upload
          </Button>
        }
        accept="*" //許可するファイルのtype
      />
    </>
  );
};
type Props = {
  onUploaded: (fileObject: FileObject) => void;
  targetContainer: string;
};

export default UploadFile;

const checkKind = (input: string) => {
  switch (input) {
    case "application.pdf":
      return "pdf";
    case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
      return "pptx";
    default:
      const kind = input.split("/")[0];
      switch (kind) {
        case "video":
          return "video";
        case "image":
          return "image";
        case "audio":
          "audio";
        default:
          return "other";
      }
  }
};
