<template>
    <UApp>
        <div class="flex h-screen w-full overflow-hidden bg-[#fff9ec] text-neutral-900">
            <LayoutSideBar />

            <div class="flex flex-col flex-1 min-w-0 min-h-0">
                <LayoutNavBar />

                <main class="flex-1 overflow-y-auto min-w-0">
                    <div class="p-6 lg:p-8 min-h-full">
                        <slot />
                    </div>
                </main>
            </div>
        </div>
    </UApp>
</template>
