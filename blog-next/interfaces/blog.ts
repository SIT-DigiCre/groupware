import ArticlePage from "../pages/article/[id]"

export type Article = {
  id: number
  member: number
  title: string
  content: string
  article_image: string
  article_tags: number[]
  is_active: boolean
  pub_date: string
}

export type ArticleTag = {
  id: number
  name: string
  content: string
  pub_date: string
}

export type ArticleList = {
  count: number
  next: string|undefined
  previous: string|undefined
  results: Article[]
}