<script setup lang="ts">
import yaml from 'js-yaml';

import { ref, onUnmounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { uploadStereo, submitStereoTask,getTaskResult, getTaskStatus } from '../api/upload';
import type { StereoFormData, TaskStatus } from '../types';

const BASE_URL=""
const left_zip = ref<File | null>(null);
const right_zip = ref<File | null>(null);
const yaml_file = ref<File | null>(null);
const loading = ref(false);
const task_id = ref<string | null>(null);
const taskStatus = ref<TaskStatus | null>(null);
const pollingInterval = ref<number | null>(null);

const handleLeftZipUpload = (file: any) => {
  console.log(file,'file')
  if (file.raw) {
    left_zip.value = file.raw;
  }
};

const handleRightZipUpload = (file: any) => {
  if (file.raw) {
    right_zip.value = file.raw;
  }
};

const handleYamlUpload = (file: any) => {
  if (file.raw) {
    yaml_file.value = file.raw;
  }
};

const startPolling = async () => {
  if (!task_id.value) return;

  const pollStatus = async () => {
    try {
      const taskResponse = await submitStereoTask(task_id.value!);
      taskStatus.value = taskResponse;

      if (taskResponse.status === '1' || taskResponse.status === '3') {
        if (pollingInterval.value) {
          clearInterval(pollingInterval.value);
          pollingInterval.value = null;
        }

        if (taskResponse.status === '1') {
          ElMessage.success('Task completed successfully');
          // Reset form after successful completion
          taskStatus.value.yaml_url = taskResponse.yaml_url;
          if (taskResponse.pdf_url) {
            taskStatus.value.pdf_url = taskResponse.pdf_url;
          } else {
            console.error('taskResponse.pdf_url is null or undefined');
          }
          stopPolling();          
        } else {
          ElMessage.error(`Task failed: ${taskResponse.message || 'Unknown error'}`);
        }
      }
    } catch (error) {
      console.error('Polling error:', error);
      stopPolling();
      ElMessage.error('Failed to get task status');
    }
  };

  // Poll every 5 seconds
  await pollStatus(); // Initial check
  pollingInterval.value = window.setInterval(pollStatus, 50000);
};

const stopPolling = () => {
  if (pollingInterval.value) {
    window.clearInterval(pollingInterval.value);
    pollingInterval.value = null;
  }
};

const resetForm = () => {
  left_zip.value = null;
  right_zip.value = null;
  yaml_file.value = null;
  task_id.value = null;
  taskStatus.value = null;
};

const handleSubmit = async () => {
  if (!left_zip.value || !right_zip.value) {
    ElMessage.warning('Please upload both left and right ZIP files');
    return;
  }
  if (!yaml_file.value) {
    ElMessage.warning('Please upload a YAML file');
    return;
  }

  loading.value = true;
  try {
    const formData: StereoFormData = {
      left_zip: left_zip.value,
      right_zip: right_zip.value,
      yaml_file: yaml_file.value,
    };

    // First upload the files
    const uploadResponse = await uploadStereo(formData);
    if (!uploadResponse.task_id) {
      throw new Error('No task ID received from upload');
    }

    task_id.value = uploadResponse.task_id;
    
    // // Submit the task for processing
    //const taskResponse: any = await submitStereoTask(uploadResponse.task_id);
    //yaml_url.value = taskResponse.yaml_url;
    //console.log(yaml_url,'yaml_url')
    ElMessage.success('Task submitted successfully');
    
    // // Start polling for status
    await startPolling();
  } catch (error) {
    console.error('Submission error:', error);
    ElMessage.error(error instanceof Error ? error.message : 'Upload or task submission failed');
    resetForm();
  } finally {
    loading.value = false;
  }
};



const downloadFile = () => {
  if (taskStatus.value?.yaml_url) {
    const yamlContent = yaml.dump(taskStatus.value.yaml_url);
    const blob = new Blob([yamlContent], { type: 'application/x-yaml' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'camera-camchain.yaml'; // 提供下载的文件名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } else {
    console.error('taskStatus.yaml_url is null or undefined');
  }
};

const downloadReport = () => {
  if (taskStatus.value?.pdf_url) {
    const base64String = taskStatus.value.pdf_url;
    const byteCharacters = atob(base64String);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'application/pdf' });

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'report.pdf'; // 提供下载的文件名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } else {
    console.error(`taskStatus.report_url is null or undefined ${taskStatus.value?.report_url}`);
  }
};


// Clean up polling when component is unmounted
onUnmounted(() => {
  stopPolling();
});
</script>

<template>
  <div class="upload-container">
    <el-form>
      <el-form-item label="Left ZIP File">
        <el-upload
          action="/kalib_task"
          :auto-upload="false"
          :on-change="handleLeftZipUpload"
          :on-remove="() => { left_zip = null }"
          accept=".zip"
          :limit="1"
          :disabled="loading"
        >
          <el-button type="primary" :disabled="loading">Select Left ZIP</el-button>
          <template #tip>
            <div class="el-upload__tip">Please upload a ZIP file</div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item label="Right ZIP File">
        <el-upload
          action=""
          :auto-upload="false"
          :on-change="handleRightZipUpload"
          :on-remove="() => { right_zip = null }"
          accept=".zip"
          :limit="1"
          :disabled="loading"
        >
          <el-button type="primary" :disabled="loading">Select Right ZIP</el-button>
          <template #tip>
            <div class="el-upload__tip">Please upload a ZIP file</div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item label="YAML File">
        <el-upload
          action=""
          :auto-upload="false"
          :on-change="handleYamlUpload"
          :on-remove="() => { yaml_file = null }"
          accept=".yaml,.yml"
          :limit="1"
          :disabled="loading"
        >
          <el-button type="primary" :disabled="loading">Select YAML</el-button>
          <template #tip>
            <div class="el-upload__tip">Please upload a YAML configuration file</div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item>
        <el-button 
          type="success" 
          @click="handleSubmit" 
          :loading="loading"
          :disabled="!left_zip || !right_zip || !yaml_file"
        >
          Submit
        </el-button>
      </el-form-item>

      <!-- Task Status Display -->
      <div v-if="taskStatus?.yaml_url">
          <el-button type="primary" @click="downloadFile">下载文件</el-button>
          <el-button type="primary" @click="downloadReport">下载报告</el-button>
      </div>

    </el-form>
  </div>
</template>

<style scoped>
.upload-container {
  padding: 20px;
}

.download {
  text-decoration: none;
  color: inherit;
}

.status-card {
  margin-top: 20px;
}

.card-header {
  font-weight: bold;
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.progress-bar {
  margin: 10px 0;
}

.status-message {
  margin: 0;
  color: #666;
}

.el-upload__tip {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}
</style>