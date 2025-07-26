import { mount } from 'svelte';
import './app.css';
import Layout from './Layout.svelte';

const app = mount(Layout, {
  target: document.getElementById('app')
});

export default app;
