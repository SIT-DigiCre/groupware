import { TextField, Button } from "@material-ui/core";
import { CloudUpload } from "@material-ui/icons";
import { FileObject } from "../../interfaces/storage";
import FileInputComponent from "react-file-input-previews-base64";
import { axios } from "../../utils/axios";

const UploadFile = (props: Props) => {
  const upload = (file) => {
    axios
      .post(
        "/v1/storage/fileobject/upload",
        {
          file_name: file.name,
          target_container: props.targetContainer,
          is_download_only: false,
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
          is_download_only: res.data.is_download_only,
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
