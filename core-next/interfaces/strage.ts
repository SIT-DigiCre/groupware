export type FileObject = { 
  id?: number;
  user?: number;
  file_name: string;
  kind: string;
  file_url: string;
  created_at?: string;
}
export const kindList = ['image','video','pptx','pdf','music','other']