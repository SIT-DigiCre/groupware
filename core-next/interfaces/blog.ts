import internal from "stream"

export type ArticleTag = {
  id: number;
  name: string;
  content: string;
  pub_date: string;
}

export type Article = {
  id: number;
  member: number;
  title: string;
  content: string;
  article_image: string;
  article_tags: number[];
  relates_works: number[];
  pub_date: string;
  is_active: boolean;
  view_count: number;
}

export type ArticleList = {
  count: number
  next: string|undefined
  previous: string|undefined
  results: Article[]
}