import React, { ReactEventHandler, useState } from "react";
import { useRouter } from "next/router";
import { axios } from "../../utils/axios";
import useSWR from "swr";
import { useSelector } from "react-redux";
import { RootState } from "../../store";
import { Article, ArticleTag } from "../../interfaces/blog";
import { Button, Fab, TextField, Grid, Zoom, Chip, Stack } from "@mui/material";
import BlogEdit from "../../components/Blog/BlogEdit";

const BlogNewPage = () => {
  const router = useRouter();
  const user = useSelector((state: RootState) => state.user.user);
  const token = useSelector((state: RootState) => state.token.token);

  const onSave = (article: Article) => {
    console.log(article)
    axios.post(`/v1/blog/my_article/`, article, {
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
          <h1>{"ブログ作成"}</h1>
          <BlogEdit onSave={onSave} isNew={true}/>
        </Grid>
      </Grid>
    </>);
};

export default BlogNewPage;
