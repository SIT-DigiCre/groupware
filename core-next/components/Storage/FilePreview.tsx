import dynamic from 'next/dynamic';
import ElementResizeListener from '../Common/ElementResizeListener';
import {useEffect, useRef, useState} from "react";
const PDFPreview = dynamic(() => import('./PDFPreview'), {ssr: false})
const FilePreview = (props: { fileUrl: string; fileName: string; width?: number }) => {
  const contentRef: React.RefObject<HTMLDivElement> = useRef(null);
  const [contentWidth, setContentWidth] = useState(100);
  const [contentHight, setContentHight] = useState(100);
  const onResize = (event: Event) => {
    console.log(contentRef.current.getBoundingClientRect().width);
    setContentWidth(contentRef.current.getBoundingClientRect().width);
    setContentHight(contentRef.current.getBoundingClientRect().width*10/16);
  }
  
  useEffect(()=>{
    setContentWidth(contentRef.current.getBoundingClientRect().width);
    setContentHight(contentRef.current.getBoundingClientRect().width*10/16);
  },[]);
  switch (getFileKind(props.fileName)) {
    case "image":
      return <img src={props.fileUrl} style={{ maxWidth: "100%" }} />;
    case "office":
      return (
        <div ref={contentRef} style={{width:"100%"}}>
        <ElementResizeListener onResize={onResize}/>
        <iframe
          src={
            "https://view.officeapps.live.com/op/embed.aspx?src=" +
            props.fileUrl
          }
          width={props.width?props.width:contentWidth}
          height={props.width?props.width*10/16:contentHight}
          frameBorder="0"
        />
      </div>
      );
    case "pdf":
      return (
      <div ref={contentRef} style={{width:"100%"}}>
        <ElementResizeListener onResize={onResize}/>
        <PDFPreview pdfUrl={props.fileUrl} width={props.width?props.width:contentWidth}/>
      </div>);
    case "video":
      return <video src={props.fileUrl} style={{ maxWidth: "100%" }} controls />;
    case "audio":
      return (
      <>
        <p>{props.fileName}</p>
        <audio src={props.fileUrl} controls></audio>
      </>);
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
  console.log(ext);
  if (imageExtList.indexOf(ext) !== -1) return "image";
  else if (officeExtList.indexOf(ext) !== -1) return "office";
  else if (pdfExtList.indexOf(ext) !== -1) return "pdf";
  else if (videoExtList.indexOf(ext) !== -1) return "video";
  else if (audioExtList.indexOf(ext) !== -1) return "audio";
  else if (exeExtList.indexOf(ext) !== -1) return "exe";
  return "other";
};

const imageExtList = ["jpg", "jpeg", "png", "gif", "svg"];
const officeExtList = ["pptx", "docx", "xlsx"];
const pdfExtList = ["pdf"]
const videoExtList = ["mp4", "mov"];
const audioExtList = ["mp3", "m4a", "flac", "wav"];
const exeExtList = ["exe", "msi", "app", "jar", "apk", "sh"];
