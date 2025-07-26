<script>
  // icons
  import IconX from '@lucide/svelte/icons/x';
  import IconShell from '@lucide/svelte/icons/shell';
  import IconBinoculars from '@lucide/svelte/icons/binoculars';

  // ui components
  import { toaster } from '../lib/toaster';
</script>

<section class="container mx-auto w-full max-w-5xl flex justify-center md:px-10 pb-5 relative">
  <IconX
    onclick={() =>
      toaster.info({
        title: 'Coming soon!',
        description: 'When implemented, you will be able to dismiss this hero.'
      })}
    class="absolute top-8 right-0"
  />
  <div
    class="grid grid-cols-1 md:grid-cols-[172px_550px] gap-8 md:gap-20 pt-2 lg:pt-8 md:pt-0 md:justify-items-start lg:justify-items-center px-4 md:px-8"
  >
    <div class="flex justify-center items-center">
      <div class="relative size-32 md:size-64 aspect-square flex">
        <div
          class="absolute top-0 left-0 size-full aspect-square rounded-full bg-conic from-success-500 to-primary-500 blur-3xl"
        ></div>
        <IconShell class="z-10 size-32 md:size-48 text-black dark:text-white m-auto" />
      </div>
    </div>
    <div class="self-center space-y-6">
      <div class="space-y-4 text-center md:text-start">
        <h1 class="heading-font-family text-3xl md:text-4xl font-bold xl:text-balance">
          Welcome to The Twist control panel
        </h1>
        <p class="xl:text-balance">
          Enabling remote control and unique features such as preset playlist management, learn
          about your gadget's capabilities <a
            href="https://github.com/bendertools/the-twist/wiki"
            target="_blank"
            class="anchor">here</a
          >.
        </p>
      </div>
      <div class="flex flex-row flex-wrap gap-3 justify-center md:justify-start">
        <button
          type="button"
          class="btn preset-filled-tertiary-500"
          onclick={() =>
            toaster.info({
              title: 'Coming soon!',
              description: 'When implemented, you will be able to take a tour.'
            })}><IconBinoculars /> Take a Tour</button
        >
        <button
          type="button"
          class="btn preset-outlined-surface-500"
          onclick={() =>
            toaster.info({
              title: 'Coming soon!',
              description: 'When implemented, you will be able to dismiss this hero.'
            })}>Don't show again</button
        >
      </div>
    </div>
  </div>
</section>
