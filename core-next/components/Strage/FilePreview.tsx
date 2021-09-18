const FilePreview = (props: { fileUrl: string; fileKind: string }) => {
  switch (props.fileKind) {
    case "image":
      return <img src={props.fileUrl} />;
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
  }
};

export default FilePreview;
