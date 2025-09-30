import Home from './pages/Home.svelte';
import Device from './pages/Device.svelte';
import Playlists from './pages/Playlists.svelte';
import Playlist from './pages/Playlist.svelte';

export default {
  '/': Home,
  '/device': Device,
  '/playlists': Playlists,
  '/playlist/:id': Playlist
};
