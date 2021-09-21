import { axios } from "../../utils/axios";
import { useEffect, useState } from "react";
import { WorkTag } from "../../interfaces/work";
import { baseURL } from "../../utils/common";
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
  const [tag, setTag] = useState<WorkTag>(null);
  useEffect(() => {
    axios
      .get(baseURL + "/v1/work/tag" + String(props.tagId), {
        headers: "JWT " + localStorage.getItem("jwt"),
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