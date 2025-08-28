<script>
  import HomeHero from '../components/HomeHero.svelte';
  import DeviceStatusCard from '../components/DeviceStatusCard.svelte';
  import ActivePlaylistCard from '../components/ActivePlaylistCard.svelte';
  import DeviceControlCard from '../components/DeviceControlCard.svelte';
  import PlaylistsSection from '../components/HomePlaylistsSection.svelte';
</script>

<div class="overflow-y-auto flex flex-col gap-8 px-4 lg:px-8 py-4 pb-10 max-h-[calc(100vh-201px)]">
  <HomeHero />

  <DeviceStatusCard />

  <ActivePlaylistCard />

  <DeviceControlCard />

  <PlaylistsSection />
</div>
