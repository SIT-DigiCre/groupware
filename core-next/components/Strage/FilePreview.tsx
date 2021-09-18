const FilePreview = (props: {
  fileUrl: string;
  fileKind: string;
  fileName: string;
}) => {
  switch (props.fileKind) {
    case "image":
      return <img src={props.fileUrl} style={{ maxWidth: "100%" }} />;
    case "pptx":
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
    case "other":
      return <a href={props.fileUrl}>{props.fileName}</a>;
  }
};

export default FilePreview;
