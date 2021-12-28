import React, { ReactEventHandler, useState } from "react";
import { useRouter } from "next/router";
import { axios } from "../../utils/axios";
import useSWR from "swr";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import { Article, ArticleTag } from "../../interfaces/blog";
import { Button, Fab, TextField, Grid, Zoom, Chip, Stack } from "@mui/material";
import BlogEdit from "../../components/Blog/BlogEdit";

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
const BlogEditPage = () => {
  const router = useRouter();
  const { articleId } = router.query;
  const user = useSelector((state: RootState) => state.user.user);
  const token = useSelector((state: RootState) => state.token.token);

  const { data: article } = useSWR<Article>(
    [`/v1/blog/my_article/${articleId}/`, token.jwt],
    fetcher
  )


  const onSave = (article: Article) => {
    console.log(article)
    axios
      .put(`/v1/blog/my_article/${articleId}/`, article, {
        headers: {
          Authorization: "JWT " + token.jwt,
        },
      })
      .then((res) => {
        router.push('/blog');
      })
      .catch((error) => {
        alert(`保存に失敗 ${error.message}`);
      });
  }
  return (
    <>
      <Grid container alignItems="center" justifyContent="center">
        <Grid item xs={11}>
          <h1>{"ブログ編集"}</h1>
          <BlogEdit onSave={onSave} article={article} />
        </Grid>
      </Grid>
    </>);
};

export default BlogEditPage;
