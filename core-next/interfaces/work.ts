export type WorkItem = {
  id?: number;
  name: string;
  intro: string;
  user: number;
  tools: number[];
  tags: number[];
  files: number[];
  created_at?: string;
}

export type WorkTag = {
  id: number;
  name: string;
  intro: string;
}

export type WorkItemList = {
  count: number
  next: string|undefined
  previous: string|undefined
  results: WorkItem[]
}