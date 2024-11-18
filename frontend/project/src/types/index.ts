export interface UploadResponse {
  success: boolean;
  message: string;
  task_id?: string;
}

export interface FormData {
  zipFile: File | null;
  yaml_file: File | null;
}

export interface StereoFormData {
  left_zip: File | null;
  right_zip: File | null;
  yaml_file: File | null;
}

export interface TaskStatus {
  status: '1' | '2' | '3' ;
  progress: number;
  message: string;
  yaml_url?: '';
}