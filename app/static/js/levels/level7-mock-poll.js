/**
 * Level 7 — The Dawn Protocol: Mock poll coordination checklist.
 */
GameApp.registerLevel(7, (() => {
    let data, container;
    const completedSteps = [];
    let signaturesCollected = false;

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        completedSteps.length = 0;
        signaturesCollected = false;

        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The Dawn Protocol — Mock Poll</h4>
            <p class="text-sm text-gray-400">It's <strong class="text-saffron-400">${data.start_time} AM</strong>. Complete the mock poll checklist in the correct order before <strong class="text-red-400">${data.deadline}</strong>.</p>
            <div class="flex gap-4 mt-3">
                <div class="text-xs px-2 py-1 rounded bg-saffron-500/20 text-saffron-400">Steps: <span id="l7-step-count">0</span>/${data.steps.length}</div>
            </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Checklist -->
            <div class="lg:col-span-2 space-y-3" id="l7-checklist"></div>
            <!-- Agents Panel -->
            <div class="glass-card p-5">
                <h5 class="font-display font-bold text-sm mb-4">Party Agents Present</h5>
                <div class="space-y-3" id="l7-agents">
                    ${data.agents.map(a => {
                        const colors = { blue_lotus: '#3B82F6', golden_gear: '#F59E0B', rising_sun: '#EF4444', eternal_flame: '#8B5CF6' };
                        return `<div class="flex items-center gap-3 p-2 rounded-lg bg-white/3">
                            <span class="w-2 h-2 rounded-full" style="background:${colors[a.party] || '#666'}"></span>
                            <div>
                                <p class="text-sm font-semibold">${a.name}</p>
                                <p class="text-xs text-gray-500">${a.party.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</p>
                            </div>
                            <span class="ml-auto text-xs" id="agent-sig-${a.party}">&#9744;</span>
                        </div>`;
                    }).join('')}
                </div>
                <button class="btn-secondary w-full mt-4 text-sm" id="l7-collect-sigs" onclick="window.L7CollectSignatures()" aria-label="Collect signatures from all agents" disabled>
                    Collect Signatures (Form 16A)
                </button>
            </div>
        </div>`;

        renderChecklist();
    }

    function renderChecklist() {
        const el = document.getElementById('l7-checklist');
        const nextIdx = completedSteps.length;

        el.innerHTML = data.steps.map((s, i) => {
            const done = i < nextIdx;
            const current = i === nextIdx;
            const icon = done ? '&#10003;' : (i + 1);
            return `<div class="checklist-item ${done ? 'completed' : current ? 'current' : ''}" 
                         id="l7-item-${i}"
                         role="button" tabindex="0"
                         aria-label="Step ${i+1}: ${s.label}${done ? ' - completed' : current ? ' - current' : ''}"
                         onclick="window.L7DoStep(${i})">
                <div class="flex items-center gap-3">
                    <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${done ? 'bg-chakra-500/20 text-chakra-400' : current ? 'bg-saffron-500/20 text-saffron-400 animate-pulse' : 'bg-white/5 text-gray-500'}">${icon}</span>
                    <div class="flex-1">
                        <p class="font-semibold text-sm">${s.label}</p>
                        <p class="text-xs text-gray-500">~${s.time_minutes} minutes</p>
                    </div>
                    ${done ? '<span class="text-chakra-400 text-sm">&#10003;</span>' : ''}
                </div>
            </div>`;
        }).join('');

        document.getElementById('l7-step-count').textContent = completedSteps.length;

        // Enable signature button after all steps done
        const sigBtn = document.getElementById('l7-collect-sigs');
        if (sigBtn) {
            sigBtn.disabled = completedSteps.length < data.steps.length;
        }
    }

    window.L7DoStep = function(idx) {
        if (idx !== completedSteps.length) return; // Must be in order
        completedSteps.push(data.steps[idx].action);
        renderChecklist();
    };

    window.L7CollectSignatures = function() {
        if (completedSteps.length < data.steps.length) return;
        signaturesCollected = true;
        data.agents.forEach(a => {
            const el = document.getElementById(`agent-sig-${a.party}`);
            if (el) {
                el.innerHTML = '<span class="text-chakra-400">&#10003;</span>';
            }
        });
        document.getElementById('l7-collect-sigs').innerHTML = '&#10003; All Signatures Collected';
        document.getElementById('l7-collect-sigs').disabled = true;
        document.getElementById('l7-collect-sigs').classList.add('border-chakra-500/30', 'text-chakra-400');
    };

    function getSubmission() {
        return { order: completedSteps, signatures_collected: signaturesCollected };
    }

    function showHint(n) {
        if (n === 1) alert('Hint: First set up the EVM hardware (BU + CU + VVPAT).');
        else if (n === 2) alert('Hint: You must invite agents BEFORE running mock votes.');
        else alert('Hint: After verifying counts, collect signatures, then reset the EVM.');
    }

    return { init, getSubmission, showHint };
})());
