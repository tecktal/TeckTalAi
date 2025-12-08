<template>
    <private-view title="Chat with LLM">
        <template #headline>
            <v-breadcrumb :items="[{ name: 'Chat with LLM', to: '/chatbot-module' }]" />
        </template>
        
        <div class="chat-container">
            <h2>Chat with LLM</h2>
            <div id="anythingllm-chat"></div>
        </div>
    </private-view>
</template>

<script>
import { onMounted } from 'vue';

export default {
    name: 'ChatModule',
    setup() {
        onMounted(() => {
            const script = document.createElement('script');
            script.setAttribute('data-embed-id', 'a7ad8aa7-080d-45d9-9cd2-d9ad69ade09e');
            script.setAttribute('data-base-api-url', 'https://teach.tecktal.ai/api/embed');
            script.src = 'https://teach.tecktal.ai/embed/anythingllm-chat-widget.min.js';
            document.body.appendChild(script);
        });
    }
};
</script>

<style scoped>
.chat-container {
    padding: 20px;
    height: calc(100vh - 200px);
}
</style>

