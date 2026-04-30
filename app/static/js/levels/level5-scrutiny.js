/**
 * Level 5 — The Scrutiny Chamber: Examine candidate affidavits.
 */
GameApp.registerLevel(5, (() => {
    let data, container;
    const decisions = {};

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        Object.keys(decisions).forEach(k => delete decisions[k]);

        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The Scrutiny Chamber</h4>
            <p class="text-sm text-gray-400">You are the Returning Officer. Review each candidate's affidavit and decide: <strong class="text-chakra-400">ACCEPT</strong> or <strong class="text-red-400">REJECT</strong>.</p>
            <div class="mt-3 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
                <p class="text-xs text-amber-400"><strong>Eligibility Criteria:</strong> Age 25+, No disqualifying convictions (Section 8 RPA), Complete affidavit with assets declared.</p>
            </div>
        </div>
        <div class="space-y-4" id="l5-candidates"></div>
        <div class="mt-4 text-xs text-gray-500">Decisions made: <span id="l5-count">0</span>/${data.candidates.length}</div>`;

        const el2 = document.getElementById('l5-candidates');
        data.candidates.forEach(c => {
            const parties = { blue_lotus: { icon: '\u2727', color: '#3B82F6' }, golden_gear: { icon: '\u2699', color: '#F59E0B' }, rising_sun: { icon: '\u2600', color: '#EF4444' }, eternal_flame: { icon: '\u2B50', color: '#8B5CF6' } };
            const p = parties[c.party] || {};

            const card = document.createElement('div');
            card.className = 'glass-card p-6';
            card.id = `candidate-${c.id}`;
            card.setAttribute('role', 'article');
            card.setAttribute('aria-label', `Candidate: ${c.name}`);

            card.innerHTML = `
                <div class="flex items-start justify-between mb-4">
                    <div class="flex items-center gap-3">
                        <span class="text-2xl" aria-hidden="true">${p.icon || ''}</span>
                        <div>
                            <h5 class="font-display font-bold">${esc(c.name)}</h5>
                            <p class="text-xs" style="color:${p.color}">${c.party.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())} Party</p>
                        </div>
                    </div>
                    <div id="verdict-${c.id}" class="text-sm font-bold"></div>
                </div>
                <div class="grid grid-cols-2 gap-3 mb-4 text-sm">
                    <div class="p-3 rounded-lg bg-white/3">
                        <p class="text-xs text-gray-500">Age</p>
                        <p class="font-bold ${c.age >= 25 ? 'text-chakra-400' : 'text-red-400'}">${c.age} years ${c.age < 25 ? '⚠' : '✓'}</p>
                    </div>
                    <div class="p-3 rounded-lg bg-white/3">
                        <p class="text-xs text-gray-500">Education</p>
                        <p class="font-semibold">${esc(c.education)}</p>
                    </div>
                    <div class="p-3 rounded-lg bg-white/3">
                        <p class="text-xs text-gray-500">Criminal Record</p>
                        <p class="font-bold ${c.criminal_record ? 'text-red-400' : 'text-chakra-400'}">${c.criminal_record ? 'YES ⚠' : 'Clean ✓'}</p>
                        ${c.criminal_details ? `<p class="text-xs text-red-400 mt-1">${esc(c.criminal_details)}</p>` : ''}
                    </div>
                    <div class="p-3 rounded-lg bg-white/3">
                        <p class="text-xs text-gray-500">Assets Declared</p>
                        <p class="font-bold ${c.assets_declared ? 'text-chakra-400' : 'text-red-400'}">${c.assets_declared ? 'Yes ✓' : 'MISSING ⚠'}</p>
                    </div>
                </div>
                <div class="flex gap-3">
                    <button class="flex-1 py-2 rounded-xl bg-chakra-500/20 text-chakra-400 font-bold text-sm hover:bg-chakra-500/30 transition-all" onclick="window.L5Decide('${c.id}', 'accept')" aria-label="Accept ${c.name}">&#10003; Accept</button>
                    <button class="flex-1 py-2 rounded-xl bg-red-500/20 text-red-400 font-bold text-sm hover:bg-red-500/30 transition-all" onclick="window.L5Decide('${c.id}', 'reject')" aria-label="Reject ${c.name}">&#10007; Reject</button>
                </div>`;

            el2.appendChild(card);
        });
    }

    window.L5Decide = function(cid, verdict) {
        decisions[cid] = verdict;
        const el = document.getElementById(`verdict-${cid}`);
        if (verdict === 'accept') {
            el.innerHTML = '<span class="text-chakra-400">ACCEPTED ✓</span>';
        } else {
            el.innerHTML = '<span class="text-red-400">REJECTED ✗</span>';
        }
        document.getElementById('l5-count').textContent = Object.keys(decisions).length;
    };

    function getSubmission() {
        return { decisions };
    }

    function showHint(n) {
        if (n === 1) alert('Hint: Minimum age for Lok Sabha is 25 years.');
        else if (n === 2) alert('Hint: Convictions with 2+ year sentence lead to disqualification.');
        else alert('Hint: Incomplete affidavits (missing asset declaration) must be rejected.');
    }

    function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

    return { init, getSubmission, showHint };
})());
