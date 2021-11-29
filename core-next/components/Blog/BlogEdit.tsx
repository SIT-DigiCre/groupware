import React, { ReactEventHandler, useState } from "react";
import { Article, ArticleTag } from "../../interfaces/blog";
import { Button, Fab, TextField, Grid, Zoom, Chip, Stack } from "@mui/material";
import TagSelectBox from "./TagSelectBox";

import { useSelector } from "react-redux";
import { RootState } from "../../store";
import MarkdownEditor from "../Common/MarkdownEditor";

const BlogEdit = (props:{onSave: (saveArticle: Article)=>void, article?: Article, isNew? :boolean}) => {
  if(props.article === null || props.article === undefined && !props.isNew)return<h3>Loading...</h3>
  console.log(props.article)
  const user = useSelector((state: RootState) => state.user.user);
  const [titleField, setTitleField] = useState(props.article ? props.article.title : "");
  const [contentField, setContentField] = useState(props.article ? props.article.content : "");
  const handleOnChangeTitleField = (e: React.ChangeEvent<HTMLInputElement>) =>
    setTitleField(e.target.value);
  
  const [articleImgUrl, setArticleImgUrl] = useState(props.article ? props.article.article_image : "");
  const [editedTags, setEditedTags] = useState<ArticleTag[]>([]);
  const onTagChange = (e: any, value: ArticleTag[]) => {
    setEditedTags(value);
  };
  const onClickSaveBtn = (isPub: boolean) => {
    console.log(contentField)
    const art: Article = {
      id: props.article ? props.article.id : 1,
      member: user.id,
      title: titleField,
      content: contentField,
      article_image: articleImgUrl,
      article_tags: editedTags.map((tag) => tag.id),
      relates_works: [],
      pub_date: props.article ? props.article.pub_date : null,
      is_active: isPub,
      view_count: props.article ? props.article.view_count : 0
    } 
    props.onSave(art);
  }
  return (
    <>
      <TextField
        required
        label="ブログタイトル"
        fullWidth
        onChange={handleOnChangeTitleField}
        defaultValue={props.article ? props.article.title : ""}
        className="mt-2"
      />
      <MarkdownEditor
        default={props.article ? props.article.content : ""}
        onChange={(md)=>{setContentField(md)}}
        label="ブログ本文"
        />
      <TagSelectBox onChange={onTagChange} />
      <Button
        onClick={() => { onClickSaveBtn(true) }}
        variant="contained">
        Save
      </Button>
    </>
  );
}

export default BlogEdit;