import { GetServerSideProps } from "next";
import { Container, Row, Col } from "react-bootstrap";
import FilePreview from "../../../components/Strage/FilePreview";
import { FileObject } from "../../../interfaces/strage";
import { WorkItem, WorkTag } from "../../../interfaces/work";
import { axios } from "../../../utils/axios";

const WorkItemPage = (props: WorkItemPageProps) => (
  <Container>
    <Row>
      <h1>{props.data.name}</h1>
      <div
        style={{ display: "inline", marginLeft: "8px", marginBottom: "3px" }}
      >
        {props.tags.map((tag) => (
          <span
            className="badge rounded-pill bg-primary"
            style={{ display: "inline", marginLeft: "1px" }}
          >
            {tag.name}
          </span>
        ))}
      </div>
    </Row>
    <Row>
      <p>{props.data.intro}</p>
    </Row>
    {props.files.map((file) => (
      <FilePreview
        fileKind={file.kind}
        fileUrl={file.file_url}
        fileName={file.file_name}
      />
    ))}
  </Container>
);
export default WorkItemPage;

type WorkItemPageProps = {
  data?: WorkItem;
  tags?: WorkTag[];
  files?: FileObject[];
  errors?: any;
};
export const getServerSideProps: GetServerSideProps = async ({ params }) => {
  try {
    const id = params?.id;
    const resData = axios.get("/v1/work/item/" + String(id));
    const data: WorkItem = (await resData).data;
    const tags: WorkTag[] = await Promise.all(
      data.tags.map(
        async (tagId) => (await axios.get("/v1/work/tag/" + String(tagId))).data
      )
    );
    const files: FileObject[] = await Promise.all(
      data.files.map(
        async (fileId) =>
          (
            await axios.get("/v1/strage/fileobject/" + String(fileId))
          ).data
      )
    );
    return { props: { data, tags, files } };
  } catch (error) {
    return { props: { errors: error.message } };
  }
};
