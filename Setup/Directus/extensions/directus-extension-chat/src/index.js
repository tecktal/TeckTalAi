import ModuleComponent from './module.vue';

export default {
    id: 'chatbot-module',
    name: 'Chat with LLM',
    icon: 'chat',
    routes: [
        {
            path: '',
            component: ModuleComponent,
        },
    ],
    preRegisterCheck(user, permissions) {
        // Optional: Add permission checks
        return true;
    }
};

