<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { uploadMonocular } from '../api/upload';
import type { FormData } from '../types';

const zipFile = ref<File | null>(null);
const yaml_file = ref<File | null>(null);
const loading = ref(false);

const handleZipUpload = (files: FileList) => {
  if (files[0]) {
    zipFile.value = files[0];
  }
};

const handleYamlUpload = (files: FileList) => {
  if (files[0]) {
    yaml_file.value = files[0];
  }
};

const handleSubmit = async () => {
  if (!zipFile.value) {
    ElMessage.warning('Please upload a ZIP file');
    return;
  }
  if (!yaml_file.value) {
    ElMessage.warning('Please upload a YAML file');
    return;
  }

  loading.value = true;
  try {
    const formData: FormData = {
      zipFile: zipFile.value,
      yaml_file: yaml_file.value,
    };
    await uploadMonocular(formData);
    ElMessage.success('Upload successful');
    // Reset form
    zipFile.value = null;
    yaml_file.value = null;
  } catch (error) {
    ElMessage.error('Upload failed');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="upload-container">
    <el-form>
      <el-form-item label="ZIP File">
        <el-upload
          action=""
          :auto-upload="false"
          :on-change="(file) => handleZipUpload(file.raw)"
          accept=".zip"
          :limit="1"
        >
          <el-button type="primary">Select ZIP File</el-button>
        </el-upload>
      </el-form-item>

      <el-form-item label="YAML File">
        <el-upload
          action=""
          :auto-upload="false"
          :on-change="(file) => handleYamlUpload(file.raw)"
          accept=".yaml,.yml"
          :limit="1"
        >
          <el-button type="primary">Select YAML</el-button>
        </el-upload>
      </el-form-item>

      <el-form-item>
        <el-button type="success" @click="handleSubmit" :loading="loading">
          Submit
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.upload-container {
  padding: 20px;
}
</style>