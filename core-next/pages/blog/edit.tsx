import React, { ReactEventHandler, useState } from "react";
import { useRouter } from "next/router";
import { axios } from "../../utils/axios";
import useSWR from "swr";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import { Article, ArticleTag } from "../../interfaces/blog";
import { Button, Fab, TextField, Grid, Zoom, Chip, Stack } from "@mui/material";
import TagSelectBox from "../../components/Blog/TagSelectBox"

const BlogEditPage = () => {
  const router = useRouter();
  const { mode, articleId } = router.query;
  const user = useSelector((state: RootState) => state.user.user);
  const token = useSelector((state: RootState) => state.token.token);
  const fetcher = async (url: string, token: string | null) => {
    if (token) {
      const res = await axios.get(url, {
        headers: { Authorization: "JWT " + token },
      });
      return res.data;
    } else {
      return null;
    }
  };
  const { data: article } = mode==="new" ? { data: null } :  useSWR<Article>(
    [`/v1/blog/my_article/${articleId}/`, token.jwt],
    fetcher
  )
  const [titleField, setTitleField] = useState(article ? article.title : "");
  const [contentField, setContentField] = useState(article ? article.content : "");
  const handleOnChangeTitleField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setTitleField(e.target.value);
  const handleOnChangeContentField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setContentField(e.target.value);
  const [articleImgUrl, setArticleImgUrl] = useState(article!==undefined ? article.article_image : "");
  const [editedTags, setEditedTags] = useState<ArticleTag[]>([]);
  const onTagChange = (e: any, value: ArticleTag[]) => {
    setEditedTags(value);
  };
  const onSave = (isActive: boolean) => {
    const putData: Article = {
      id: article ? article.id : null,
      member: user.id,
      title: titleField,
      content: contentField,
      article_image: articleImgUrl,
      article_tags: editedTags.map((tag) => tag.id),
      relates_works: [],
      pub_date: article ? article.pub_date : null,
      is_active: isActive,
      view_count: article ? article.view_count : 0
    }
    console.log(putData);
    if (mode === "new") {
      axios.post(`/v1/blog/my_article/`, putData, {
        headers: {
          Authorization: "JWT " + token.jwt,
        },
      })
        .then((res) => {
          router.reload();
        })
        .catch((error) => {
          alert(`保存に失敗 ${error.message}`);
        });
    } else {
      axios
        .put(`/v1/blog/my_article/${articleId}/`, putData, {
          headers: {
            Authorization: "JWT " + token.jwt,
          },
        })
        .then((res) => {
          router.reload();
        })
        .catch((error) => {
          alert(`保存に失敗 ${error.message}`);
        });
    }
  }
  return (
    <>
      <Grid container alignItems="center" justifyContent="center">
        <Grid item xs={11}>
          <h1>{mode === "new" ? "ブログ投稿" : "ブログ編集"}</h1>
          <TextField
            required
            label="ブログタイトル"
            fullWidth
            onChange={handleOnChangeTitleField}
            defaultValue={article ? article.title : ""}
            className="mt-2"
          />
          <TextField
            required
            label="ブログ本文"
            fullWidth
            onChange={handleOnChangeContentField}
            defaultValue={article ? article.content : ""}
            className="mt-2"
          />
          <TagSelectBox onChange={onTagChange} />
          <Button 
            onClick={()=>{onSave(true)}}
            variant="contained">
            Save
          </Button>
        </Grid>
      </Grid>
    </>);
};

export default BlogEditPage;
