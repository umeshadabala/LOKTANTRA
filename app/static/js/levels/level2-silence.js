/**
 * Level 2 — The Great Silence: Deepfake vs Real news classifier.
 */
GameApp.registerLevel(2, (() => {
    let data, container;
    const classifications = {};
    let currentIndex = 0;

    function init(levelData, meta, el) {
        data = levelData;
        container = el;
        currentIndex = 0;
        Object.keys(classifications).forEach(k => delete classifications[k]);

        container.innerHTML = `
        <div class="glass-card p-6 mb-6">
            <h4 class="font-display font-bold text-lg mb-2">The 48-Hour Silence Period</h4>
            <p class="text-sm text-gray-400">The silence period is active. Classify each news item as <strong class="text-chakra-400">REAL</strong> or <strong class="text-red-400">DEEPFAKE</strong>.</p>
            <div class="mt-3 text-xs text-gray-500">Item <span id="l2-current">1</span> of ${data.news_items.length}</div>
        </div>
        <div class="max-w-xl mx-auto" id="l2-card-area"></div>
        <div class="flex justify-center gap-4 mt-6">
            <button id="l2-fake-btn" class="px-8 py-4 rounded-2xl bg-red-500/20 text-red-400 border border-red-500/30 font-bold text-lg hover:bg-red-500/30 transition-all" aria-label="Mark as Deepfake">
                &#10007; DEEPFAKE
            </button>
            <button id="l2-real-btn" class="px-8 py-4 rounded-2xl bg-chakra-500/20 text-chakra-400 border border-chakra-500/30 font-bold text-lg hover:bg-chakra-500/30 transition-all" aria-label="Mark as Real">
                &#10003; REAL
            </button>
        </div>
        <div id="l2-results" class="mt-6 space-y-2 hidden"></div>`;

        document.getElementById('l2-fake-btn').addEventListener('click', () => classify(false));
        document.getElementById('l2-real-btn').addEventListener('click', () => classify(true));

        showCard();
    }

    function showCard() {
        const area = document.getElementById('l2-card-area');
        if (currentIndex >= data.news_items.length) {
            area.innerHTML = '<div class="glass-card p-8 text-center"><p class="font-display font-bold text-xl text-chakra-400">All items classified!</p><p class="text-sm text-gray-400 mt-2">Click Submit to see your results.</p></div>';
            document.getElementById('l2-fake-btn').disabled = true;
            document.getElementById('l2-real-btn').disabled = true;
            showResults();
            return;
        }

        const item = data.news_items[currentIndex];
        document.getElementById('l2-current').textContent = currentIndex + 1;

        area.innerHTML = `
        <div class="news-card glass-card p-6" id="l2-active-card" aria-label="News item: ${esc(item.headline)}">
            <div class="flex items-center gap-2 mb-3">
                <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse" aria-hidden="true"></span>
                <span class="text-xs text-gray-500 uppercase tracking-wider">Breaking News</span>
            </div>
            <h5 class="font-display font-bold text-lg mb-3">${esc(item.headline)}</h5>
            <div class="flex items-center gap-2 text-xs text-gray-500">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/></svg>
                Source: ${esc(item.source)}
            </div>
        </div>`;
    }

    function classify(isReal) {
        if (currentIndex >= data.news_items.length) return;
        const item = data.news_items[currentIndex];
        classifications[item.id] = isReal;

        const card = document.getElementById('l2-active-card');
        if (card) {
            card.classList.add(isReal ? 'swipe-right' : 'swipe-left');
        }

        setTimeout(() => {
            currentIndex++;
            showCard();
        }, 300);
    }

    function showResults() {
        const results = document.getElementById('l2-results');
        results.classList.remove('hidden');
        let html = '<h5 class="font-display font-bold text-sm text-gray-400 mb-2">Your Classifications:</h5>';
        data.news_items.forEach(item => {
            const answer = classifications[item.id];
            const correct = answer === item.is_real;
            const icon = correct ? '&#10003;' : '&#10007;';
            const color = correct ? 'text-chakra-400' : 'text-red-400';
            html += `<div class="flex items-start gap-2 text-xs p-2 rounded-lg bg-white/3">
                <span class="${color} font-bold">${icon}</span>
                <span class="text-gray-400">${esc(item.headline.substring(0, 60))}...</span>
            </div>`;
        });
        results.innerHTML = html;
    }

    function getSubmission() {
        return { classifications };
    }

    function showHint(n) {
        if (n === 1) alert('Hint: Official sources like PIB, ECI, and courts are usually real.');
        else if (n === 2) alert('Hint: "WhatsApp Forward" and "Anonymous" sources are red flags.');
        else alert('Hint: EVMs are standalone devices — they cannot be hacked remotely.');
    }

    function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

    return { init, getSubmission, showHint };
})());
