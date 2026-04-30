/**
 * Level 8 — The Seal of Integrity: Secure the Control Unit.
 */
GameApp.registerLevel(8, (() => {
    let data, container;
    const sealOrder = [];
    const custodyDone = [];

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        sealOrder.length = 0;
        custodyDone.length = 0;

        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The Seal of Integrity</h4>
            <p class="text-sm text-gray-400">Voting has ended. Apply the numbered seals in the correct order, then complete the chain-of-custody steps.</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Seals -->
            <div>
                <h5 class="font-display font-bold text-sm mb-4">Step 1: Apply Seals</h5>
                <div class="mb-4">
                    <p class="text-xs text-gray-500 mb-2">Available Seals (drag to slots below):</p>
                    <div class="flex flex-wrap gap-2" id="l8-seal-pool">
                        ${data.seals.map(s => `<button class="seal-tag bg-amber-500/20 text-amber-400 border border-amber-500/30" data-seal="${s.position}" id="seal-btn-${s.position}" onclick="window.L8ApplySeal('${s.position}')" aria-label="Seal ${s.number} for ${s.label}">
                            ${s.number}
                        </button>`).join('')}
                    </div>
                </div>
                <div class="space-y-3" id="l8-seal-slots">
                    ${data.seals.map(s => `<div class="seal-slot" id="slot-${s.position}" aria-label="Seal slot: ${s.label}">
                        <p class="text-xs text-gray-500">${s.label}</p>
                        <div class="mt-1" id="slot-content-${s.position}"></div>
                    </div>`).join('')}
                </div>
                <p class="text-xs text-gray-500 mt-3">Seals applied: <span id="l8-seal-count">0</span>/${data.seals.length}</p>
            </div>
            <!-- Custody Chain -->
            <div>
                <h5 class="font-display font-bold text-sm mb-4">Step 2: Chain of Custody</h5>
                <div class="space-y-3" id="l8-custody">
                    ${data.custody_steps.map((s, i) => `<div class="checklist-item ${i === 0 ? 'current' : ''}" id="l8-custody-${i}" role="button" tabindex="0"
                         aria-label="Custody step: ${s.label}"
                         onclick="window.L8DoCustody(${i}, '${s.action}')">
                        <div class="flex items-center gap-3">
                            <span class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold bg-white/5 text-gray-500" id="l8-cicon-${i}">${i + 1}</span>
                            <p class="text-sm">${s.label}</p>
                        </div>
                    </div>`).join('')}
                </div>
                <div class="mt-6 glass-card p-4" id="l8-form" style="display:none">
                    <h6 class="font-display font-bold text-xs text-saffron-400 mb-2">Form 16 (Part I) — Seal Register</h6>
                    <div class="text-xs space-y-1" id="l8-form-entries"></div>
                </div>
            </div>
        </div>`;
    }

    window.L8ApplySeal = function(position) {
        if (sealOrder.includes(position)) return;
        sealOrder.push(position);

        const seal = data.seals.find(s => s.position === position);
        const slot = document.getElementById(`slot-content-${position}`);
        slot.innerHTML = `<span class="seal-tag bg-chakra-500/20 text-chakra-400 border border-chakra-500/30">${seal.number} &#10003;</span>`;

        document.getElementById(`slot-${position}`).classList.add('sealed');
        document.getElementById(`seal-btn-${position}`).disabled = true;
        document.getElementById(`seal-btn-${position}`).classList.add('opacity-30');
        document.getElementById('l8-seal-count').textContent = sealOrder.length;

        // Show form when all seals applied
        if (sealOrder.length === data.seals.length) {
            document.getElementById('l8-form').style.display = 'block';
            const entries = document.getElementById('l8-form-entries');
            entries.innerHTML = data.seals.map(s => `<div class="flex justify-between p-1 border-b border-white/5">
                <span class="text-gray-500">${s.label}</span>
                <span class="font-mono text-chakra-400">${s.number}</span>
            </div>`).join('');
        }
    };

    window.L8DoCustody = function(idx, action) {
        if (idx !== custodyDone.length) return;
        custodyDone.push(action);

        const icon = document.getElementById(`l8-cicon-${idx}`);
        icon.innerHTML = '&#10003;';
        icon.className = 'w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold bg-chakra-500/20 text-chakra-400';
        document.getElementById(`l8-custody-${idx}`).classList.add('completed');
        document.getElementById(`l8-custody-${idx}`).classList.remove('current');

        if (idx + 1 < data.custody_steps.length) {
            document.getElementById(`l8-custody-${idx + 1}`).classList.add('current');
        }
    };

    function getSubmission() {
        return {
            seal_order: sealOrder,
            custody_steps_completed: custodyDone,
        };
    }

    function showHint(n) {
        if (n === 1) alert('Hint: Seal the Result Section first — it contains the vote counts.');
        else if (n === 2) alert('Hint: After sealing, record all seal numbers before signatures.');
        else alert('Hint: The correct seal order: Result Section → Ballot Slot → VVPAT Chamber.');
    }

    return { init, getSubmission, showHint };
})());
