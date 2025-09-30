<script >
	import {useDroppable} from '@dnd-kit-svelte/core';

	let {children, class: className, ...rest} = $props();

	const droppable = useDroppable(rest);
</script>

<div class={[className]} bind:this={droppable.node.current}>
	{@render children()}
</div>
