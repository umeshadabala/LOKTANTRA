/**
 * Level 1 — The Electoral Maze: Search and verify voter identities.
 */
GameApp.registerLevel(1, (() => {
    let data, container;
    const selected = { legitimate: new Set(), ghosts: new Set() };

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        selected.legitimate.clear();
        selected.ghosts.clear();

        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The Electoral Maze</h4>
            <p class="text-sm text-gray-400">Examine each voter record. Mark legitimate voters with <strong class="text-chakra-400">VERIFY</strong> and flag suspicious entries as <strong class="text-red-400">GHOST</strong>.</p>
            <div class="flex gap-4 mt-3 text-xs">
                <span class="px-2 py-1 rounded bg-chakra-500/20 text-chakra-400">Verified: <span id="l1-legit-count">0</span>/5</span>
                <span class="px-2 py-1 rounded bg-red-500/20 text-red-400">Ghosts: <span id="l1-ghost-count">0</span>/2</span>
            </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="l1-voter-grid"></div>`;

        const grid = document.getElementById('l1-voter-grid');
        data.voters.forEach(v => {
            const card = document.createElement('div');
            card.className = 'glass-card p-4 cursor-pointer transition-all';
            card.id = `voter-${v.id}`;
            card.setAttribute('role', 'button');
            card.setAttribute('tabindex', '0');
            card.setAttribute('aria-label', `Voter: ${v.name}, Age: ${v.age}, ID: ${v.voter_id}`);
            card.innerHTML = `
                <div class="flex items-center justify-between mb-2">
                    <span class="font-bold">${esc(v.name)}</span>
                    <span class="text-xs text-gray-500">Age: ${v.age}</span>
                </div>
                <p class="text-xs text-gray-500">ID: ${v.voter_id}</p>
                <p class="text-xs text-gray-600">Constituency: ${v.constituency}</p>
                <div class="flex gap-2 mt-3">
                    <button class="btn-verify text-xs px-3 py-1 rounded-lg bg-chakra-500/20 text-chakra-400 hover:bg-chakra-500/30 transition-colors" data-vid="${v.id}" data-action="legit" aria-label="Mark ${v.name} as legitimate">&#10003; Verify</button>
                    <button class="btn-ghost text-xs px-3 py-1 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-colors" data-vid="${v.id}" data-action="ghost" aria-label="Flag ${v.name} as ghost voter">&#10007; Ghost</button>
                </div>
                <div class="mt-2 text-xs font-bold hidden" id="tag-${v.id}"></div>`;

            card.querySelectorAll('button').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    handleMark(v.id, btn.dataset.action);
                });
            });

            grid.appendChild(card);
        });
    }

    function handleMark(vid, action) {
        // Remove from both sets first
        selected.legitimate.delete(vid);
        selected.ghosts.delete(vid);

        const tag = document.getElementById(`tag-${vid}`);
        const card = document.getElementById(`voter-${vid}`);

        if (action === 'legit') {
            selected.legitimate.add(vid);
            tag.textContent = '✓ VERIFIED';
            tag.className = 'mt-2 text-xs font-bold text-chakra-400';
            card.style.borderColor = 'rgba(34,197,94,0.3)';
        } else {
            selected.ghosts.add(vid);
            tag.textContent = '✗ FLAGGED AS GHOST';
            tag.className = 'mt-2 text-xs font-bold text-red-400';
            card.style.borderColor = 'rgba(239,68,68,0.3)';
        }
        tag.classList.remove('hidden');

        document.getElementById('l1-legit-count').textContent = selected.legitimate.size;
        document.getElementById('l1-ghost-count').textContent = selected.ghosts.size;
    }

    function getSubmission() {
        return { legitimate: [...selected.legitimate], ghosts: [...selected.ghosts] };
    }

    function showHint(n) {
        if (n === 1) alert('Hint: Check for impossible ages — no one lives to 150!');
        else if (n === 2) alert('Hint: Look for duplicate Voter IDs.');
        else alert('Hint: There are exactly 5 legitimate voters and 2 ghosts.');
    }

    function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

    return { init, getSubmission, showHint };
})());
