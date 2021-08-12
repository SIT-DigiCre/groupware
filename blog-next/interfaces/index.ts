// You can include shared interfaces/types in a separate file
// and then use them in any component by importing them. For
// example, to import the interface below do:
//
// import { User } from 'path/to/interfaces';

// ↓後で消す
export type User = {
  id: number
  name: string
}

export type Article = {
  id: number
  member: number
  title: string
  content: string
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
