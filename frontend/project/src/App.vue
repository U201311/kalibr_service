<script setup lang="ts">
import { ref } from 'vue';
import MonocularUpload from './components/MonocularUpload.vue';
import StereoUpload from './components/StereoUpload.vue';

const activeTab = ref('monocular');
</script>

<template>
  <div class="app-container">
    <el-container>
      <el-tabs
        v-model="activeTab"
        class="left-tabs"
        tab-position="left"
        :style="{ height: '100vh' }"
      >
        <el-tab-pane label="单目" name="monocular">
          <div class="content-area">
            <MonocularUpload />
          </div>
        </el-tab-pane>
        <el-tab-pane label="双目" name="stereo">
          <div class="content-area">
            <StereoUpload />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-container>
  </div>
</template>

<style>
.app-container {
  width: 100%;
  height: 100vh;
  background-color: #f5f7fa;
}

.left-tabs {
  border-right: 1px solid #dcdfe6;
}

.content-area {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

/* Override Element Plus default styles for left tabs */
.left-tabs .el-tabs__header.is-left {
  margin-right: 0;
  background-color: #fff;
  min-width: 150px;
}

.left-tabs .el-tabs__content {
  background-color: #fff;
  height: 100%;
  padding: 0;
}

.left-tabs .el-tabs__item {
  text-align: left;
  padding: 15px 20px;
}

.left-tabs .el-tabs__item.is-active {
  background-color: #ecf5ff;
  border-right: 2px solid #409eff;
}

/* Reset body margin and padding */
body {
  margin: 0;
  padding: 0;
  height: 100vh;
}

#app {
  height: 100vh;
  margin: 0;
  padding: 0;
  max-width: none;
}
</style>