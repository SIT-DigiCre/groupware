import {useState,useEffect} from "react";
import { Document, Page } from 'react-pdf';
import { Button, Stack } from "@mui/material";
import { pdfjs } from 'react-pdf';
const PDFPreview = (props:{pdfUrl: string, width: number}) => {
  const [numPages, setNumPages] = useState<number>(null);
  const [pageNumber, setPageNumber] = useState(1);
  const onDocumentLoadSuccess = ({ numPages}) => {
    setNumPages(numPages);
  }
  const changePage = (countUp: boolean) => {
    if(countUp){
      if(pageNumber == numPages)return;
      setPageNumber(pageNumber+1);
    }else{
      if(pageNumber == 1)return;
      setPageNumber(pageNumber-1);
    }
  }
  useEffect(() => {
    if (typeof window !== undefined){
      pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;
    }
  }, []);
  return(
    <div>
      <Document
        file={props.pdfUrl}
        onLoadSuccess={onDocumentLoadSuccess}
      >
        <Page pageNumber={pageNumber} width={props.width}/>
        <Stack direction="row" spacing={2} style={{margin:"3px auto"}}>
        <Button variant="contained" onClick={()=>{changePage(false)}}>←</Button>
        <p>{pageNumber}</p>
        <Button variant="contained" onClick={()=>{changePage(true)}}>→</Button>
      </Stack>
      </Document>
      

    </div>
  )
}

export default PDFPreview;