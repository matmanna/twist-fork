<script>
  let { playlist, className = '' } = $props();

  // icons
  import IconArrowRight from '@lucide/svelte/icons/arrow-right';
  import IconListVideo from '@lucide/svelte/icons/list-video';
  import IconSpeaker from '@lucide/svelte/icons/speaker';

  // ui components
  import { toaster } from '../lib/toaster.js';

  // utils
  import { formatDate, cn } from '../lib/utils.js';
</script>

<div
  class={cn(
    'card shadow-xl bg-base-100 flex flex-col justify-between cursor-pointer hover:shadow-2xl transition-all preset-filled-surface-100-900 py-3 px-6 gap-4',
    className
  )}
>
  <div class="card-body flex-1 flex flex-col gap-2">
    <div class="flex items-center mb-2 gap-2">
      <span class="bg-primary/10 rounded-full">
        <IconListVideo class="w-7 h-7 text-primary" />
      </span>
      <h2 class="card-title text-md font-semibold truncate flex-1">
        {playlist.name}
      </h2>
    </div>
    <p class="text-base-content/80 text-sm line-clamp-2">
      {playlist.description != '~' ? playlist.description : 'No description'}
    </p>
    <div class="flex flex-row flex-wrap items-center gap-1 mt-2 text-sm text-base-content/70">
      <span class="flex items-center gap-1">
        <IconSpeaker class="w-4 h-4" />
        {playlist.size} presets •
      </span>
      <span>Updated {formatDate(playlist.last_updated)}</span>
    </div>
  </div>
  <div class="flex flex-row justify-end">
    <a class="btn preset-filled w-fit" href={`#/playlist/${playlist.id}`}>
      <span>Open</span>
      <IconArrowRight size={18} />
    </a>
  </div>
</div>
