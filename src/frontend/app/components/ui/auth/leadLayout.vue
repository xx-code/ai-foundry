<template>
    <div
        class="relative h-full p-10 flex flex-col overflow-hidden
            bg-linear-to-b from-secondary-500 from-0% via-[#ff9802] via-50% via-[#ff8205] via-75% to-primary-500 to-100%">
            <Logo class="anim-fade-down" />

            <div class="mt-16 leading-[0.9] tracking-tight">
                <h1 class="anim-slide-up font-black text-9xl text-neutral-900" style="--delay: 100ms">BUILD.</h1>
                <h1 class="anim-slide-up font-black text-9xl text-neutral-900" style="--delay: 220ms">TUNE.</h1>
                <h1 class="anim-slide-up font-bold text-9xl text-white" style="--delay: 340ms">SHIP.</h1>
            </div>

            <p class="anim-slide-up mt-6 text-neutral-900 text-xl font-medium" style="--delay: 460ms">
                De l'idée au modèle<br />déployé
            </p>

            <div class="mt-auto mb-4 anim-pop" style="--delay: 700ms">
                <div
                    class="float-card p-4 bg-[#fff9ec] w-fit font-mono text-sm border-2 border-neutral-900
                           shadow-[6px_6px_0_#171717] -rotate-6
                           transition-all duration-300 ease-out
                           hover:-rotate-3 hover:scale-105 hover:shadow-[10px_10px_0_#171717]"
                >
                    <p>epoch 12/20 - loss</p>
                    <p>
                        <span class="text-blue-600">0.042</span>
                        <span class="text-green-600 ml-1 inline-block anim-check">✓</span>
                    </p>
                </div>
            </div>
        </div>
</template>