<script>
  import HomeHero from '../components/HomeHero.svelte';
  import DeviceStatusCard from '../components/DeviceStatusCard.svelte';
  import PlaylistsSection from '../components/HomePlaylistsSection.svelte';
</script>

<div class="overflow-y-auto flex flex-col gap-8 px-4 lg:px-8 py-4 pb-10 max-h-[calc(100vh-201px)]">
  <HomeHero />

  <DeviceStatusCard />

  <PlaylistsSection />
</div>
