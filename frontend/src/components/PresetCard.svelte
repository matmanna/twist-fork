<script>
  // dnd kit utils
  import { CSS, styleObjectToString } from '@dnd-kit-svelte/utilities';
  import { useSortable } from '@dnd-kit-svelte/sortable';

  // device state
  import { allPresets } from '../stores/state.js';

  // icons
  import IconTrash from '@lucide/svelte/icons/trash';
	import IconGripVertical from '@lucide/svelte/icons/grip-vertical';

	// props 
  let { item, deleteMe }= $props();

	// dnd state
  const { attributes, activatorNode, listeners, node, transform, transition, isDragging, isSorting } = useSortable(
    {
      id: item.id
    }
  );

  const style = $derived(
    styleObjectToString({
      transform: CSS.Transform.toString(transform.current),
      transition: isSorting.current ? transition.current : undefined,
      zIndex: isDragging.current ? 1 : undefined
    })
  );
</script>

<div
  class="relative select-none w-full"
  bind:this={node.current}
  {style}

>
  <div
    class={[
      ...'flex flex-row items-center w-full  z-10'.split(' '),
      { invisible: isDragging.current }
    ]}
  >
    <p class="w-8 text-center">
      {item.position + 1}.
    </p>

    <div
      class="card preset-filled-surface-50-900 border-[1px] border-surface-200-800 card-hover px-2 py-1 flex flex-row gap-2 items-center gap-2 w-full bg-surface-50-900"
    >
      <div class="flex flex-row items-center gap-2 w-full">
        <div
          class=" bg-tertiary-500/30 rounded-md w-8 h-8 text-center flex items-center justify-center"
        >
          <p class="text-lg text-base-content/70 font-semibold">{item.preset_number}</p>
        </div>
        <p class="text-lg text-base-content/70 font-semibold">
          {$allPresets && $allPresets.length > item.preset_number - 1
            ? $allPresets[item.preset_number - 1].name
            : '????????'}
        </p>

        <p class="text-md italic">{item.note ? '• ' + item.note : ''}</p>
      </div>
      <button type="button" class="btn-icon preset-filled-error-500 cursor-pointer z-10" title="Delete" aria-label="Delete" onclick={deleteMe}
        ><IconTrash size={18} /></button
      >
			<IconGripVertical
				size={18}
				class="text-gray-500 cursor-pointer"
				bind:this={activatorNode.current}
			{...attributes.current}
			{...listeners.current}
		></IconGripVertical>
    </div>
  </div>

  {#if isDragging.current}
    <div class="flex flex-row items-center absolute w-full opacity-25 inset-0 w-full">
      <p class="w-8 text-center">
        {item.position + 1}.
      </p>
      <div
        class="card preset-filled-surface-50-900 border-[1px] border-surface-200-800 card-hover px-2 py-1 flex flex-row gap-2 items-center gap-2 w-full bg-surface-50-900"
      >
        <div
          class=" bg-tertiary-500/30 rounded-md w-8 h-8 text-center flex items-center justify-center"
        >
          <p class="text-lg text-base-content/70 font-semibold">{item.preset_number}</p>
        </div>
        <p class="text-lg text-base-content/70 font-semibold">
          {$allPresets && $allPresets.length > item.preset_number - 1
            ? $allPresets[item.preset_number - 1].name
            : '????????'}
        </p>
        <p class="text-md italic">{item.note ? '• ' + item.note : ''}</p>
      </div>
    </div>
  {/if}
</div>
