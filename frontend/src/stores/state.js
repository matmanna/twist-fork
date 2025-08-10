// src/state.js
import { writable } from 'svelte/store';

export const deviceStatus = writable(undefined);
export const deviceDetails = writable(undefined);
export const productName = writable(undefined);
export const currentPreset = writable({ data: undefined, index: undefined });
export const auditionStatus = writable(undefined);
export const memoryUsage = writable(undefined);
export const processorUsage = writable(undefined);
export const firmwareVersion = writable(undefined);
export const playlists = writable([]);
export const playlistItems = writable([]);
export const playlistsLoading = writable(true);
export const playlistItemsLoading = writable(false);
export const creatingPlaylist = writable(false);
export const showPlaylistModal = writable(false);
export const allPresets = writable([]);
export const presetsLoading = writable(true);
