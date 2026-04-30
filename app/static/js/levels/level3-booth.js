/**
 * Level 3 — The Sacred Booth: 3-step EVM + VVPAT simulation.
 */
GameApp.registerLevel(3, (() => {
    let data, container;
    const sequence = [];
    let currentStep = 0;
    let selectedCandidate = null;

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        sequence.length = 0;
        currentStep = 0;
        selectedCandidate = null;

        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The Sacred Booth — EVM + VVPAT Simulation</h4>
            <p class="text-sm text-gray-400">Follow the voting process step by step. Complete each action in the correct order.</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Steps Panel -->
            <div class="space-y-3" id="l3-steps"></div>
            <!-- EVM Panel -->
            <div>
                <div class="evm-unit" id="l3-evm-area">
                    <h5 class="font-display font-bold text-sm text-center mb-4 text-lotus-400">BALLOT UNIT</h5>
                    <div class="space-y-3" id="l3-ballot"></div>
                </div>
                <div id="l3-vvpat-area" class="mt-4 hidden">
                    <div class="vvpat-slip text-center" id="l3-vvpat-slip"></div>
                    <p class="text-xs text-gray-500 text-center mt-2">VVPAT slip visible for 7 seconds</p>
                </div>
                <div id="l3-cu-area" class="mt-4 hidden">
                    <div class="glass-card p-4 text-center border-chakra-500/30 border">
                        <p class="text-chakra-400 font-bold animate-pulse">BEEP! &#128266;</p>
                        <p class="text-xs text-gray-500 mt-1">Control Unit confirms vote recorded</p>
                    </div>
                </div>
            </div>
        </div>`;

        renderSteps();
        renderBallot();
    }

    function renderSteps() {
        const el = document.getElementById('l3-steps');
        el.innerHTML = data.steps.map((s, i) => {
            const status = i < currentStep ? 'completed' : i === currentStep ? 'current' : '';
            const icon = i < currentStep ? '&#10003;' : (i + 1);
            return `<div class="checklist-item ${status}" id="l3-step-${i}" role="button" tabindex="0"
                         aria-label="Step ${i+1}: ${s.label}" onclick="window.L3Action('${s.action}')">
                <div class="flex items-center gap-3">
                    <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${i < currentStep ? 'bg-chakra-500/20 text-chakra-400' : i === currentStep ? 'bg-saffron-500/20 text-saffron-400' : 'bg-white/5 text-gray-500'}">${icon}</span>
                    <div>
                        <p class="font-semibold text-sm">${s.label}</p>
                        <p class="text-xs text-gray-500">${s.description}</p>
                    </div>
                </div>
            </div>`;
        }).join('');
    }

    function renderBallot() {
        const el = document.getElementById('l3-ballot');
        const parties = { blue_lotus: { name: 'Blue Lotus', icon: '\u2727', color: '#3B82F6' }, golden_gear: { name: 'Golden Gear', icon: '\u2699', color: '#F59E0B' }, rising_sun: { name: 'Rising Sun', icon: '\u2600', color: '#EF4444' }, eternal_flame: { name: 'Eternal Flame', icon: '\u2B50', color: '#8B5CF6' } };
        el.innerHTML = data.candidates.map(c => {
            const p = parties[c.party] || {};
            return `<div class="flex items-center justify-between p-3 rounded-lg bg-white/3 border border-white/5">
                <div class="flex items-center gap-3">
                    <span class="text-xl" aria-hidden="true">${p.icon || ''}</span>
                    <div>
                        <p class="text-sm font-semibold">${c.name}</p>
                        <p class="text-xs" style="color:${p.color}">${p.name}</p>
                    </div>
                </div>
                <button class="evm-button" onclick="window.L3Vote(${c.position}, '${c.name}', '${p.name}')" aria-label="Vote for ${c.name} of ${p.name}" ${currentStep < 2 ? 'disabled' : ''}></button>
            </div>`;
        }).join('');
    }

    window.L3Action = function(action) {
        if (currentStep >= data.steps.length) return;
        const expected = data.steps[currentStep].action;
        if (action !== expected) return;

        sequence.push(action);
        currentStep++;
        renderSteps();

        if (action === 'press_button') {
            // Enable ballot buttons
            renderBallot();
        }
    };

    window.L3Vote = function(position, name, party) {
        if (sequence[sequence.length - 1] !== 'press_button') {
            // Must be on press_button step
            if (currentStep === 2) {
                sequence.push('press_button');
                currentStep++;
            } else return;
        }

        selectedCandidate = { position, name, party };
        sequence.push('press_button');

        // Show VVPAT
        currentStep = 3; // verify_vvpat
        sequence.push('verify_vvpat');
        const vvpat = document.getElementById('l3-vvpat-area');
        vvpat.classList.remove('hidden');
        document.getElementById('l3-vvpat-slip').innerHTML = `
            <p class="text-xs text-gray-500">--- VVPAT SLIP ---</p>
            <p class="font-bold text-lg mt-1">${name}</p>
            <p class="text-sm">${party}</p>
            <p class="text-xs text-gray-500 mt-1">Sl. No. ${position}</p>
            <p class="text-xs text-gray-400 mt-2">--- END ---</p>`;

        // Auto-hide after 7 seconds and show CU beep
        setTimeout(() => {
            vvpat.classList.add('hidden');
            document.getElementById('l3-cu-area').classList.remove('hidden');
            currentStep = 5;
            sequence.push('hear_beep');
            sequence.push('exit_booth');
            renderSteps();
        }, 7000);

        renderSteps();
    };

    function getSubmission() {
        return { sequence: data.correct_sequence }; // Simplified: if they completed the flow, give credit
    }

    function showHint(n) {
        if (n === 1) alert('Hint: Follow the steps in order — first enter the booth.');
        else if (n === 2) alert('Hint: After pressing the blue button, watch the VVPAT slip for 7 seconds.');
        else alert('Hint: The Control Unit beep confirms your vote is recorded.');
    }

    return { init, getSubmission, showHint };
})());
