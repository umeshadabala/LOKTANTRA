/**
 * Level 6 — The 2km Mandate: Polling booth placement puzzle.
 */
GameApp.registerLevel(6, (() => {
    let data, container;
    const booths = [];

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        booths.length = 0;

        const size = data.grid_size;
        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The 2km Mandate</h4>
            <p class="text-sm text-gray-400">Place <strong>${data.max_booths} polling booths</strong> on the map so every village is within <strong>${data.radius_km}km</strong>. Click on empty cells to place booths.</p>
            <div class="flex gap-4 mt-3 text-xs">
                <span class="px-2 py-1 rounded bg-lotus-500/20 text-lotus-400">Booths: <span id="l6-booth-count">0</span>/${data.max_booths}</span>
                <span class="px-2 py-1 rounded bg-chakra-500/20 text-chakra-400">Covered: <span id="l6-covered">0</span>/${data.villages.length}</span>
            </div>
        </div>
        <div class="flex gap-4 mb-3 text-xs text-gray-500">
            <span class="flex items-center gap-1"><span class="w-3 h-3 rounded bg-chakra-500/30"></span> Village</span>
            <span class="flex items-center gap-1"><span class="w-3 h-3 rounded bg-lotus-500/40"></span> Booth</span>
            <span>Each cell = ${data.cell_km}km</span>
        </div>
        <div class="grid gap-1" id="l6-grid" style="grid-template-columns: repeat(${size}, 1fr); max-width: 500px;" role="grid" aria-label="District map grid"></div>
        <button class="btn-secondary mt-4 text-sm" onclick="window.L6Clear()" aria-label="Clear all booths">Clear All Booths</button>`;

        renderGrid();
    }

    function renderGrid() {
        const grid = document.getElementById('l6-grid');
        grid.innerHTML = '';
        const size = data.grid_size;
        const villageMap = {};
        data.villages.forEach(v => { villageMap[`${v.x},${v.y}`] = v; });
        const boothMap = {};
        booths.forEach(b => { boothMap[`${b.x},${b.y}`] = true; });

        for (let y = 0; y < size; y++) {
            for (let x = 0; x < size; x++) {
                const key = `${x},${y}`;
                const cell = document.createElement('div');
                cell.className = 'map-cell';
                cell.setAttribute('role', 'gridcell');

                if (villageMap[key]) {
                    const v = villageMap[key];
                    cell.classList.add('village');
                    cell.innerHTML = `<span class="text-xs" title="${v.name} (pop: ${v.population})">&#127968;</span>`;
                    cell.setAttribute('aria-label', `Village: ${v.name}, Population: ${v.population}`);

                    // Check if covered
                    const covered = booths.some(b => {
                        const dist = Math.sqrt((v.x - b.x) ** 2 + (v.y - b.y) ** 2) * data.cell_km;
                        return dist <= data.radius_km;
                    });
                    if (covered) cell.classList.add('covered');
                } else if (boothMap[key]) {
                    cell.classList.add('booth');
                    cell.innerHTML = '<span class="text-xs">&#127971;</span>';
                    cell.setAttribute('aria-label', `Polling booth at ${x},${y}`);
                    cell.onclick = () => removeBooth(x, y);
                } else {
                    cell.setAttribute('aria-label', `Empty cell ${x},${y} - click to place booth`);
                    cell.onclick = () => placeBooth(x, y);
                }

                grid.appendChild(cell);
            }
        }

        updateCounts();
    }

    function placeBooth(x, y) {
        if (booths.length >= data.max_booths) {
            alert(`Maximum ${data.max_booths} booths allowed!`);
            return;
        }
        // Don't place on a village
        if (data.villages.some(v => v.x === x && v.y === y)) return;
        booths.push({ x, y });
        renderGrid();
    }

    function removeBooth(x, y) {
        const idx = booths.findIndex(b => b.x === x && b.y === y);
        if (idx >= 0) booths.splice(idx, 1);
        renderGrid();
    }

    window.L6Clear = function() {
        booths.length = 0;
        renderGrid();
    };

    function updateCounts() {
        document.getElementById('l6-booth-count').textContent = booths.length;
        let covered = 0;
        data.villages.forEach(v => {
            const isCovered = booths.some(b => {
                const dist = Math.sqrt((v.x - b.x) ** 2 + (v.y - b.y) ** 2) * data.cell_km;
                return dist <= data.radius_km;
            });
            if (isCovered) covered++;
        });
        document.getElementById('l6-covered').textContent = covered;
    }

    function getSubmission() {
        return { booths: booths.map(b => ({ x: b.x, y: b.y })) };
    }

    function showHint(n) {
        if (n === 1) alert('Hint: Try placing booths between clusters of villages.');
        else if (n === 2) alert('Hint: Each cell equals 1km. The radius is 2km (2 cells diagonal ≈ 1.4km).');
        else alert('Hint: Optimal positions are roughly at (2,1), (6,2), (2,6), (6,6).');
    }

    return { init, getSubmission, showHint };
})());
