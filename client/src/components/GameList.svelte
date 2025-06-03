<script lang="ts">
    import { onMount } from "svelte";

    interface Game {
        id: number;
        title: string;
        description: string;
        publisher?: { id: number; name: string };
        category?: { id: number; name: string };
        starRating?: number;
    }

    interface Category {
        id: number;
        name: string;
        description?: string;
        game_count?: number;
    }

    interface Publisher {
        id: number;
        name: string;
        description?: string;
        game_count?: number;
    }

    export let games: Game[] = [];
    let loading = true;
    let error: string | null = null;
    let categories: Category[] = [];
    let publishers: Publisher[] = [];
    let selectedCategories: number[] = [];
    let selectedPublishers: number[] = [];
    let showFilters = false;

    const fetchGames = async () => {
        loading = true;
        try {
            // Build query parameters for filtering
            const params = new URLSearchParams();
            if (selectedCategories.length > 0) {
                params.append('category', selectedCategories.join(','));
            }
            if (selectedPublishers.length > 0) {
                params.append('publisher', selectedPublishers.join(','));
            }
            
            const url = `/api/games${params.toString() ? '?' + params.toString() : ''}`;
            const response = await fetch(url);
            if(response.ok) {
                games = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    const fetchCategories = async () => {
        try {
            const response = await fetch('/api/categories');
            if (response.ok) {
                categories = await response.json();
            }
        } catch (err) {
            console.error('Failed to fetch categories:', err);
        }
    };

    const fetchPublishers = async () => {
        try {
            const response = await fetch('/api/publishers');
            if (response.ok) {
                publishers = await response.json();
            }
        } catch (err) {
            console.error('Failed to fetch publishers:', err);
        }
    };

    const toggleCategory = (categoryId: number) => {
        if (selectedCategories.includes(categoryId)) {
            selectedCategories = selectedCategories.filter(id => id !== categoryId);
        } else {
            selectedCategories = [...selectedCategories, categoryId];
        }
        fetchGames();
    };

    const togglePublisher = (publisherId: number) => {
        if (selectedPublishers.includes(publisherId)) {
            selectedPublishers = selectedPublishers.filter(id => id !== publisherId);
        } else {
            selectedPublishers = [...selectedPublishers, publisherId];
        }
        fetchGames();
    };

    const clearFilters = () => {
        selectedCategories = [];
        selectedPublishers = [];
        fetchGames();
    };

    onMount(() => {
        fetchCategories();
        fetchPublishers();
        fetchGames();
    });
</script>

<div>
    <!-- Header with filter toggle -->
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-medium text-slate-100">Featured Games</h2>
        <button 
            class="flex items-center gap-2 px-4 py-2 text-sm bg-slate-800/60 text-slate-300 hover:text-slate-100 hover:bg-slate-700/60 rounded-lg border border-slate-700/50 transition-colors"
            on:click={() => showFilters = !showFilters}
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.207A1 1 0 013 6.5V4z" />
            </svg>
            Filters
        </button>
    </div>

    <!-- Collapsible filter section -->
    {#if showFilters}
        <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl p-6 mb-6 border border-slate-700/50">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Category filters -->
                <div>
                    <h3 class="text-lg font-medium text-slate-200 mb-3">Categories</h3>
                    <div class="space-y-2">
                        {#each categories as category}
                            <label class="flex items-center gap-3 cursor-pointer group">
                                <input
                                    type="checkbox"
                                    class="w-4 h-4 text-blue-600 bg-slate-700 border-slate-600 rounded focus:ring-blue-500 focus:ring-2"
                                    checked={selectedCategories.includes(category.id)}
                                    on:change={() => toggleCategory(category.id)}
                                />
                                <span class="text-slate-300 group-hover:text-slate-100 transition-colors">
                                    {category.name}
                                    <span class="text-xs text-slate-500 ml-1">({category.game_count})</span>
                                </span>
                            </label>
                        {/each}
                    </div>
                </div>

                <!-- Publisher filters -->
                <div>
                    <h3 class="text-lg font-medium text-slate-200 mb-3">Publishers</h3>
                    <div class="space-y-2">
                        {#each publishers as publisher}
                            <label class="flex items-center gap-3 cursor-pointer group">
                                <input
                                    type="checkbox"
                                    class="w-4 h-4 text-purple-600 bg-slate-700 border-slate-600 rounded focus:ring-purple-500 focus:ring-2"
                                    checked={selectedPublishers.includes(publisher.id)}
                                    on:change={() => togglePublisher(publisher.id)}
                                />
                                <span class="text-slate-300 group-hover:text-slate-100 transition-colors">
                                    {publisher.name}
                                    <span class="text-xs text-slate-500 ml-1">({publisher.game_count})</span>
                                </span>
                            </label>
                        {/each}
                    </div>
                </div>
            </div>

            <!-- Filter actions -->
            {#if selectedCategories.length > 0 || selectedPublishers.length > 0}
                <div class="mt-6 pt-4 border-t border-slate-700/50">
                    <div class="flex items-center justify-between">
                        <div class="text-sm text-slate-400">
                            {selectedCategories.length + selectedPublishers.length} filter{selectedCategories.length + selectedPublishers.length !== 1 ? 's' : ''} applied
                        </div>
                        <button
                            class="text-sm text-blue-400 hover:text-blue-300 transition-colors"
                            on:click={clearFilters}
                        >
                            Clear all filters
                        </button>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
    
    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-3 bg-slate-700 rounded w-full mb-3"></div>
                            <div class="h-3 bg-slate-700 rounded w-5/6 mb-4"></div>
                            <div class="h-2 bg-slate-700 rounded-full w-full mb-2"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-4"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if games.length === 0}
        <!-- no games found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No games available at the moment.</p>
        </div>
    {:else}
        <!-- game list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="games-grid">
            {#each games as game (game.id)}
                <a 
                    href={`/game/${game.id}`} 
                    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                >
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors" data-testid="game-title">{game.title}</h3>
                            
                            {#if game.category || game.publisher}
                                <div class="flex gap-2 mb-3">
                                    {#if game.category}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-blue-900/60 text-blue-300" data-testid="game-category">
                                            {game.category.name}
                                        </span>
                                    {/if}
                                    {#if game.publisher}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-purple-900/60 text-purple-300" data-testid="game-publisher">
                                            {game.publisher.name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}
                            
                            <p class="text-slate-400 mb-4 text-sm line-clamp-2" data-testid="game-description">{game.description}</p>
                            
                            <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>