<script>
  import Droppable from '../lib/components/droppable.svelte';
  import PresetCard from './PresetCard.svelte';
  import { DndContext, DragOverlay } from '@dnd-kit-svelte/core';
  import { SortableContext, arrayMove } from '@dnd-kit-svelte/sortable';
  import { dropAnimation, sensors } from '../lib/dnd.js';
  import { crossfade } from 'svelte/transition';

  let { movePresetItem, deletePresetItem, editPresetItem, playPresetItem, position, items } = $props();

  let activeId = $state(null);
  const activeItem = $derived(items.find((item) => item.id === activeId));

  function handleDragStart(event) {
    activeId = event.active.id;
  }

  function handleDragEnd({ active, over }) {
    if (!over) return;

    const oldIndex = items.findIndex((item) => item.id === active.id);
    const newIndex = items.findIndex((item) => item.id === over.id);
    items = arrayMove(items, oldIndex, newIndex);

    movePresetItem(active.id, newIndex);

    activeId = nu;
  }

  function handleDragOver({ active, over }) {
    if (!over) return;
  }

  const [send, recieve] = crossfade({ duration: 100 });
</script>

<DndContext
  {sensors}
  onDragStart={handleDragStart}
  onDragEnd={handleDragEnd}
  onDragOver={handleDragOver}
>
  <div class="w-full flex flex-col gap-2">
    {@render itemList('playlist', items)}
  </div>

  <DragOverlay {dropAnimation}>
    {#if activeItem && activeId}
      <PresetCard item={activeItem} />
    {/if}
  </DragOverlay>
</DndContext>

{#snippet itemList(id, items)}
  <SortableContext {items}>
    <Droppable {id}>
      <div class="w-full flex flex-col gap-2">
        {#if items.length === 0}
          <p class="text-center text-base-content/50">No items in this preset.</p>
        {/if}
        {#each items as item (item.id)}
          <div in:recieve={{ key: item.id }} out:send={{ key: item.id }}>
            <PresetCard
              {item}
              selected={item.position === position }
              deleteMe={deletePresetItem ? () => {
                deletePresetItem(item.id);
              } : null}
              editMe={editPresetItem ? (newPreset, newNote) => {
                editPresetItem(item.id, newPreset, newNote);
              } : null}
              playMe={playPresetItem ? () => {
                playPresetItem(item.id);
              } : null}
            />
          </div>
        {/each}
      </div>
    </Droppable>
  </SortableContext>
{/snippet}
