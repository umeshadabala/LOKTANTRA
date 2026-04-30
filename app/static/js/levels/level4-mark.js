/**
 * Level 4 — The Indelible Mark: Ink application mini-game.
 */
GameApp.registerLevel(4, (() => {
    let data, container;
    let selectedFinger = null;
    let selectedPosition = null;

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        selectedFinger = null;
        selectedPosition = null;

        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The Indelible Mark</h4>
            <p class="text-sm text-gray-400">Apply indelible ink to the correct finger. Select the <strong>finger</strong> and the <strong>area</strong> where the ink should go.</p>
            <div class="mt-3 p-3 rounded-lg bg-purple-500/10 border border-purple-500/20">
                <p class="text-xs text-purple-400"><strong>Ink:</strong> ${data.ink_properties.chemical} &bull; Made by ${data.ink_properties.manufacturer} &bull; Lasts ${data.ink_properties.duration}</p>
            </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Hand Display -->
            <div class="glass-card p-6">
                <h5 class="font-display font-bold text-sm mb-4">Select the Correct Finger</h5>
                <div class="mb-4">
                    <p class="text-xs text-gray-500 mb-2 font-semibold">LEFT HAND</p>
                    <div class="flex gap-2">
                        ${['left_thumb', 'left_index', 'left_middle', 'left_ring', 'left_pinky'].map(f =>
                            `<button class="finger-btn flex-1 py-4 rounded-xl text-center text-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all" data-finger="${f}" id="finger-${f}" aria-label="${f.replace('_', ' ')}" onclick="window.L4SelectFinger('${f}')">
                                ${f === 'left_thumb' ? '&#x1F44D;' : '&#9995;'}
                                <p class="text-[10px] text-gray-500 mt-1">${f.split('_')[1]}</p>
                            </button>`
                        ).join('')}
                    </div>
                </div>
                <div>
                    <p class="text-xs text-gray-500 mb-2 font-semibold">RIGHT HAND</p>
                    <div class="flex gap-2">
                        ${['right_thumb', 'right_index', 'right_middle', 'right_ring', 'right_pinky'].map(f =>
                            `<button class="finger-btn flex-1 py-4 rounded-xl text-center text-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all" data-finger="${f}" id="finger-${f}" aria-label="${f.replace('_', ' ')}" onclick="window.L4SelectFinger('${f}')">
                                &#9995;
                                <p class="text-[10px] text-gray-500 mt-1">${f.split('_')[1]}</p>
                            </button>`
                        ).join('')}
                    </div>
                </div>
                <p class="text-xs text-gray-500 mt-4">Selected: <strong id="l4-finger-label" class="text-saffron-400">None</strong></p>
            </div>
            <!-- Position Selection -->
            <div class="glass-card p-6">
                <h5 class="font-display font-bold text-sm mb-4">Select Ink Application Area</h5>
                <div class="space-y-3">
                    ${['nail', 'knuckle', 'palm', 'wrist'].map(pos =>
                        `<button class="pos-btn w-full p-4 rounded-xl text-left bg-white/5 border border-white/10 hover:bg-white/10 transition-all" data-pos="${pos}" id="pos-${pos}" aria-label="Apply ink on ${pos}" onclick="window.L4SelectPos('${pos}')">
                            <p class="font-semibold text-sm">${pos.charAt(0).toUpperCase() + pos.slice(1)}</p>
                            <p class="text-xs text-gray-500">${pos === 'nail' ? 'From cuticle to fingertip' : pos === 'knuckle' ? 'On the finger joint' : pos === 'palm' ? 'On the palm surface' : 'On the wrist area'}</p>
                        </button>`
                    ).join('')}
                </div>
                <p class="text-xs text-gray-500 mt-4">Selected: <strong id="l4-pos-label" class="text-saffron-400">None</strong></p>
            </div>
        </div>
        <div id="l4-preview" class="mt-6 hidden">
            <div class="glass-card p-6 text-center">
                <div class="text-5xl mb-3" id="l4-ink-preview" aria-hidden="true">&#9995;</div>
                <p class="font-display font-bold text-lg" id="l4-preview-text"></p>
            </div>
        </div>`;
    }

    window.L4SelectFinger = function(finger) {
        selectedFinger = finger;
        document.querySelectorAll('.finger-btn').forEach(b => {
            b.classList.remove('border-saffron-500', 'bg-saffron-500/10');
            b.classList.add('border-white/10');
        });
        document.getElementById(`finger-${finger}`).classList.add('border-saffron-500', 'bg-saffron-500/10');
        document.getElementById(`finger-${finger}`).classList.remove('border-white/10');
        document.getElementById('l4-finger-label').textContent = finger.replace('_', ' ');
        updatePreview();
    };

    window.L4SelectPos = function(pos) {
        selectedPosition = pos;
        document.querySelectorAll('.pos-btn').forEach(b => {
            b.classList.remove('border-saffron-500', 'bg-saffron-500/10');
            b.classList.add('border-white/10');
        });
        document.getElementById(`pos-${pos}`).classList.add('border-saffron-500', 'bg-saffron-500/10');
        document.getElementById(`pos-${pos}`).classList.remove('border-white/10');
        document.getElementById('l4-pos-label').textContent = pos;
        updatePreview();
    };

    function updatePreview() {
        if (selectedFinger && selectedPosition) {
            const preview = document.getElementById('l4-preview');
            preview.classList.remove('hidden');
            const correct = selectedFinger === 'left_index' && selectedPosition === 'nail';
            document.getElementById('l4-preview-text').textContent = `Ink on ${selectedFinger.replace('_', ' ')} → ${selectedPosition}`;
            document.getElementById('l4-ink-preview').style.color = correct ? '#8B5CF6' : '#F97316';
        }
    }

    function getSubmission() {
        return { finger: selectedFinger, position: selectedPosition };
    }

    function showHint(n) {
        if (n === 1) alert('Hint: The ink goes on the LEFT hand.');
        else if (n === 2) alert('Hint: It\'s applied to the INDEX finger.');
        else alert('Hint: The ink is applied on the NAIL, from cuticle to tip.');
    }

    return { init, getSubmission, showHint };
})());
