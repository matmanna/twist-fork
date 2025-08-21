<script>
  // routing
  import Router from 'svelte-spa-router';
  import { location as routerLocation } from 'svelte-spa-router';
  import routes from './routes.js';

  const pageNames = {
    '/': 'Home',
    '/device': 'Device',
    '/playlists': 'Playlists',
    '/settings': 'Settings'
  };

  // ui components
  import { AppBar, Navigation, Toaster } from '@skeletonlabs/skeleton-svelte';

  import Lightswitch from './components/Lightswitch.svelte';
  import { toaster } from './lib/toaster';

  // lucide icons
  import IconArrowLeft from '@lucide/svelte/icons/arrow-left';
  import IconHouse from '@lucide/svelte/icons/house';
  import IconWrench from '@lucide/svelte/icons/wrench';
  import IconListMusic from '@lucide/svelte/icons/list-music';
  import IconSettings2 from '@lucide/svelte/icons/settings-2';
  import IconCheckCircle from '@lucide/svelte/icons/check-circle';
  import IconAlertTriangle from '@lucide/svelte/icons/alert-triangle';
  import IconXCircle from '@lucide/svelte/icons/x-circle';
  import IconListVideo from '@lucide/svelte/icons/list-video';
  import IconGlobe from '@lucide/svelte/icons/globe';

  // setup/handle device websockets
  import { onMount } from 'svelte';
  import {
    deviceStatus,
    deviceDetails,
    productName,
    currentPreset,
    auditionStatus,
    memoryUsage,
    processorUsage,
    firmwareVersion,
    activePlaylist,
    playlists,
    playlistsLoading,
    playlistItems,
    playlistItemsLoading,
    creatingPlaylist,
    showPlaylistModal,
    allPresets,
    presetsLoading
  } from './stores/state.js';

  let oldDeviceStatus = $state('offline');

  function waitForSync() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if ($deviceStatus == 'online') {
          oldDeviceStatus = $deviceStatus;
          resolve(undefined);
        } else {
          oldDeviceStatus = $deviceStatus;
          reject();
        }
      }, 1500);
    });
  }

  $effect(() => {
    if (
      $deviceStatus == 'online' &&
      $deviceStatus != oldDeviceStatus &&
      oldDeviceStatus != 'syncing'
    ) {
      oldDeviceStatus = $deviceStatus;
      toaster.success({
        title: 'Device Connected',
        description: `You are now connected to ${$productName} with firmware version ${$firmwareVersion}.`
      });
    } else if (
      $deviceStatus == 'offline' &&
      $deviceStatus != oldDeviceStatus &&
      oldDeviceStatus != 'syncing'
    ) {
      oldDeviceStatus = $deviceStatus;
      toaster.error({
        title: 'Device Disconnected',
        description: `You have been disconnected from ${$productName && $productName.length > 0 ? $productName : 'the device'}.`
      });
    } else if (
      $deviceStatus == 'warning' &&
      $deviceStatus != oldDeviceStatus &&
      oldDeviceStatus != 'syncing'
    ) {
      oldDeviceStatus = $deviceStatus;

      toaster.warning({
        title: 'Device Warning',
        description: `There is a warning with your device. Please check the status.`
      });
    } else if (
      $deviceStatus == 'syncing' &&
      $deviceStatus != oldDeviceStatus &&
      oldDeviceStatus != 'syncing'
    ) {
      oldDeviceStatus = $deviceStatus;
      toaster.promise(waitForSync(), {
        loading: {
          title: 'Syncing...',
          description: 'Please wait while the device is syncing.'
        },
        success: () => ({
          title: 'Device Connected',
          description: `You are now connected to ${$productName} with firmware version ${$firmwareVersion}.`
        }),
        error: () => ({
          title: 'Device Error',
          description: 'An error occurred while attempting to connect.'
        })
      });
    }
  });

  let wsDevice = null;

  function connectDeviceWS() {
    wsDevice = new WebSocket(`ws://${location.host}/ws/device`);
    wsDevice.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.type === 'status_update') {
          deviceStatus.set(msg.status);
          deviceDetails.set(msg.details ?? {});
          productName.set(msg.product_name ?? productName);
          currentPreset.set(msg.current_preset ?? currentPreset);
          auditionStatus.set(msg.audition_status ?? auditionStatus);
          memoryUsage.set(msg.memory_usage ?? memoryUsage);
          processorUsage.set(msg.processor_usage ?? processorUsage);
          firmwareVersion.set(msg.firmware_version ?? firmwareVersion);
          allPresets.set(msg.presets ?? allPresets);
          activePlaylist.set(msg.active_playlist ?? null);
          if ($allPresets && $allPresets.length > 0) {
            presetsLoading.set(false);
          }
        }
      } catch (e) {
        toaster.error({
          title: 'Error processing device message',
          description: e.message
        });
      }
    };
    wsDevice.onclose = () => {
      deviceStatus.set('offline');
      setTimeout(connectDeviceWS, 2000);
    };
  }

  function wsSend(msg) {
    if (wsDevice && wsDevice.readyState === 1) {
      wsDevice.send(JSON.stringify(msg));
    }
  }

  // playlist management
  async function fetchPlaylists() {
    playlistsLoading.set(true);
    try {
      const res = await fetch(`http://${location.host}/playlists/`);
      if (!res.ok) throw new Error('Failed to fetch playlists');
      playlists.set(await res.json());
    } catch (e) {
      toaster.error({
        title: 'Error fetching playlists',
        description: e.message
      });
    }
  }

  async function createPlaylist(newName, newDescription) {
    creatingPlaylist.set(true);
    try {
      const res = await fetch(`http://${location.host}/playlists/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newName,
          description: newDescription
        })
      });
      if (!res.ok) {
        const data = await res.json();
        toaster.error({
          title: 'Error creating playlist',
          description: data.message || 'Failed to create playlist'
        });
      }
      showPlaylistModal.set(false);
      await fetchPlaylists();
    } catch (e) {
      toaster.error({
        title: 'Error creating playlist',
        description: e.message
      });
    } finally {
      creatingPlaylist.set(false);
    }
  }

  async function refreshPlaylistItems() {
    playlistItemsLoading.set(true);
    try {
      const res = await fetch(
        `http://${location.host}/playlists/${$routerLocation.split('/')[2]}/items`
      );

      if (!res.ok) throw new Error('Failed to fetch playlist items');
      playlistItems.set(await res.json());
    } catch (e) {
      toaster.error({
        title: 'Error fetching playlist items',
        description: e.message
      });
    } finally {
      playlistItemsLoading.set(false);
    }
  }

  $effect(async () => {
    if ($routerLocation.split('/').includes('playlist')) {
      await refreshPlaylistItems();
    }
  });

  onMount(() => {
    connectDeviceWS();
    fetchPlaylists();
    return () => wsDevice && wsDevice.close();
  });

  // handle events from pages
  import { layoutEvents } from './stores/events.js';

  $effect(() => {
    if ($layoutEvents) {
      if ($layoutEvents.type === 'connect') {
        wsSend({ action: 'connect' });
      } else if ($layoutEvents.type === 'disconnect') {
        wsSend({ action: 'disconnect' });
      } else if ($layoutEvents.type === 'reconnect') {
        wsSend({ action: 'reconnect' });
      } else if ($layoutEvents.type === 'refresh') {
        wsSend({ action: 'refresh_status' });
      } else if ($layoutEvents.type === 'set_preset') {
        wsSend({ action: 'set_preset', index: Number($layoutEvents.presetIndex) });
      } else if ($layoutEvents.type === 'audition_preset') {
        try {
          const jsonData = JSON.parse($layoutEvents.auditionJson);
          wsSend({ action: 'audition_preset', data: jsonData });
        } catch (e) {
          toaster.error({
            title: 'Invalid JSON for audition preset'
          });
        }
      } else if ($layoutEvents.type === 'create_playlist') {
        if ($layoutEvents.name && $layoutEvents.description) {
          createPlaylist($layoutEvents.name, $layoutEvents.description);
        } else {
          toaster.error({
            title: 'Invalid playlist data',
            description: 'Name and description are required to create a playlist.'
          });
        }
      } else if ($layoutEvents.type === 'refetch_playlist_items') {
        if ($routerLocation.split('/').includes('playlist')) {
          refreshPlaylistItems();
        }
      } else if ($layoutEvents.type === 'playlist_deleted') {
        toaster.success({
          title: 'Playlist Deleted',
          description: 'The playlist has been successfully deleted.'
        });
        fetchPlaylists();

        if ($routerLocation.split('/').includes('playlist')) {
          window.location.href = '/#/playlists';
        }
      } else if ($layoutEvents.type === 'playlist_started') {
        toaster.success({
          title: 'Playlist Started',
          description: `The playlist has been started successfully.`
        });
      } else if ($layoutEvents.type === 'playlist_stopped') {
        toaster.success({
          title: 'Playlist Stopped',
          description: `The playlist has been stopped successfully.`
        });
      }

      layoutEvents.set(null);
    }
  });
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
  <header class="sticky top-0 z-10 preset-filled-surface-100-900">
    <div class="mx-auto w-full max-w-5xl">
      <AppBar>
        {#snippet lead()}
          {#if $routerLocation.split('/').includes('playlist')}
            <a href="/#/playlists" class="btn btn-ghost">
              <IconArrowLeft size={24} />
            </a>
          {:else if $routerLocation != '/'}
            <a href="/#/">
              <IconHouse size={24} />
            </a>
          {:else}
            <a href="/#/">
              <IconGlobe size={24} />
            </a>
          {/if}
        {/snippet}
        {#snippet trail()}
          <div class="flex flex-row gap-2 items-center"><Lightswitch /></div>
        {/snippet}
        {#snippet headline()}
          <h2 class="h2">
            {#if $routerLocation
              .split('/')
              .includes('playlist') && $playlists && $playlists.length > 0}
              {#if $playlists.find((p) => p.id == $routerLocation.split('/')[2])}
                <div class="flex flex-row gap-2 items-center">
                  <IconListVideo class="w-9 h-9 text-primary" />
                  {$playlists.find((p) => p.id == $routerLocation.split('/')[2]).name}
                </div>
              {:else}
                Unknown Playlist
              {/if}
            {:else}
              {pageNames[$routerLocation] ?? 'Unknown'}
            {/if}
          </h2>
        {/snippet}
        <img src="/logo.svg" alt="Bender Logo" class="h-8 mx-auto" />
      </AppBar>
    </div>
  </header>

  <main class="w-full relative overflow-y-hidden max-h-full">
    <Toaster {toaster}></Toaster>

    <Router {routes} let:Component let:params>
      <Component {params} />
    </Router>
  </main>

  <footer class="sticky bottom-0 preset-filled-surface-100-900">
    <div
      class="w-full h-[35px] bg-gradient-to-t from-surface-100 dark:from-surface-950 to-transparent absolute top-[-35px] left-0"
    ></div>
    <div class="mx-auto w-full max-w-5xl">
      <Navigation.Bar value={$routerLocation}>
        <Navigation.Tile id="/" href="/#" label="Home">
          <IconHouse />
        </Navigation.Tile>
        <Navigation.Tile id="/device" href="/#/device" label="Device">
          <IconWrench />
        </Navigation.Tile>
        <Navigation.Tile id="/playlists" href="/#/playlists" label="Playlists">
          <IconListMusic />
        </Navigation.Tile>
        <Navigation.Tile id="/settings" href="/#/settings" label="Settings">
          <IconSettings2 />
        </Navigation.Tile>
      </Navigation.Bar>
    </div>
  </footer>
</div>
