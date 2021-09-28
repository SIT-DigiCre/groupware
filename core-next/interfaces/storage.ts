export type FileObject = { 
  id?: number;
  user?: number;
  file_name: string;
  is_download_only: boolean;
  file_url: string;
  created_at?: string;
}