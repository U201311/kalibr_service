
import axios from 'axios';
import type { UploadResponse, FormData, StereoFormData, TaskStatus } from '../types';

const API_BASE_URL = 'http://10.112.12.60:8000/kalib';

export const uploadMonocular = async (formData: FormData): Promise<UploadResponse> => {
  const data = new FormData();
  if (formData.zipFile) {
    data.append('zipFile', formData.zipFile);
  }
  if (formData.yaml_file) {
    data.append('yaml_file', formData.yaml_file);
  }

  try {
    console.log(data,'data')
    const response = await axios.post(`${API_BASE_URL}/kalib_task`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error('Upload failed');
  }
};

export const uploadStereo = async (formData: StereoFormData): Promise<UploadResponse> => {
  const data:any = new FormData();
  if (formData.left_zip) {
    data.append('left_zip', formData.left_zip);
  }
  console.log(formData,'formdata', data)
  if (formData.right_zip) {
    data.append('right_zip', formData.right_zip);
  }
  if (formData.yaml_file) {
    data.append('yaml_file', formData.yaml_file);
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/kalib_task`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error('Upload failed');
  }
};

export const submitStereoTask = async (task_id: string): Promise<{
  yaml_content(yaml_content: any): unknown; task_id: string 
}> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/kalib_task_result/${task_id}`);
    return response.data;
  } catch (error) {
    throw new Error('Task submission failed');
  }
};

export const getTaskStatus = async (task_id: string): Promise<TaskStatus> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/tasks/${task_id}/status`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to get task status');
  }
};


export const getTaskResult = async (task_id: string): Promise<any> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/static/${task_id}/data/camera-camchain.yaml`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to get task result');
  }
};