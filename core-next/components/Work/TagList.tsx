import { axios } from "../../utils/axios";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import { WorkTag } from "../../interfaces/work";
import { GetServerSideProps } from "next";

const TagList = (props: { tagIds: number[] }) => {
  return (
    <div>
      {props.tagIds.map((tagId) => {
        <Tag tagId={tagId} key={tagId} />;
      })}
    </div>
  );
};

const Tag = (props: { tagId: number }) => {
  const token = useSelector((state: RootState) => state.token.token);
  const [tag, setTag] = useState<WorkTag>(null);
  useEffect(() => {
    axios
      .get("/v1/work/tag/" + String(props.tagId), {
        headers: "JWT " + token.jwt,
      })
      .then((res) => setTag(res.data))
      .catch((error) => console.log(error.message));
  }, []);

  return (
    <>
      {tag === null ? (
        <></>
      ) : (
        <span className="badge bg-primary" key={tag.id}>
          {tag.name}
        </span>
      )}
    </>
  );
};
export default TagList;
