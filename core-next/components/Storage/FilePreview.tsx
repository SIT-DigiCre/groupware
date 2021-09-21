const FilePreview = (props: { fileUrl: string; fileName: string }) => {
  switch (getFileKind(props.fileName)) {
    case "image":
      return <img src={props.fileUrl} style={{ maxWidth: "100%" }} />;
    case "office":
      return (
        <iframe
          src={
            "https://view.officeapps.live.com/op/embed.aspx?src=" +
            props.fileUrl
          }
          width="100%"
          height="300px"
          frameBorder="0"
        />
      );
    case "video":
      return <video src={props.fileUrl} style={{ maxWidth: "100%" }} />;
    case "audio":
      return <a href={props.fileUrl}>{props.fileName}</a>;
    case "exe":
      return (
        <>
          <a href={props.fileUrl}>{props.fileName}</a>
          <p>注意！実行形式ファイル</p>
        </>
      );
    case "other":
      return <a href={props.fileUrl}>{props.fileName}</a>;
  }
};

export default FilePreview;

export const getFileKind = (fileName: string) => {
  const tmp = fileName.split(".");
  const ext = tmp[tmp.length - 1];
  if (ext in imageExtList) return "image";
  else if (ext in officeExtList) return "office";
  else if (ext in videoExtList) return "video";
  else if (ext in audioExtList) return "audio";
  else if (ext in exeExtList) return "exe";
  return "other";
};

const imageExtList = ["jpg", "jpeg", "png", "gif", "svg"];
const officeExtList = ["pptx", "docx", "xlsx", "pdf"];
const videoExtList = ["mp4", "mov"];
const audioExtList = ["mp3", "m4a", "flac", "wav"];
const exeExtList = ["exe", "msi", "app", "jar", "apk", "sh"];
