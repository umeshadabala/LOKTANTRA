/**
 * LOKTANTRA — Game Engine
 * Core state machine, timer, scoring, insight system, and level lifecycle.
 */
const GameApp = (() => {
    // Level insight messages shown in the insight bar during gameplay
    const LEVEL_INSIGHTS = {
        1: { title: 'Why Verified Rolls Matter', text: 'Under Article 325, no citizen can be excluded from electoral rolls on grounds of religion, race, caste, or sex. Ghost voters undermine this right — every fake entry dilutes a real citizen\'s vote.' },
        2: { title: 'The 48-Hour Shield', text: 'The silence period before polling, enforced under Article 324, prevents last-minute propaganda and deepfakes from manipulating voter decisions. It protects your right to think independently.' },
        3: { title: 'Digital Vote, Physical Proof', text: 'The EVM+VVPAT system under Article 324 creates a verifiable paper trail. The 7-second VVPAT slip display lets you confirm your vote was recorded correctly — bridging digital efficiency with physical trust.' },
        4: { title: 'One Person, One Vote', text: 'Indelible ink (silver nitrate) applied to the left index finger nail is the simplest yet most effective anti-fraud technology. Under Article 326, it enforces universal adult suffrage — ensuring nobody votes twice.' },
        5: { title: 'Transparency in Candidacy', text: 'Under Article 327 and the RPA 1951, candidates must be 25+, disclose criminal records, and declare assets. This transparency empowers voters to make informed choices about their leaders.' },
        6: { title: 'Democracy at Your Doorstep', text: 'ECI guidelines under Article 324 mandate that no voter should travel more than 2km to vote. Even if just one voter lives in a remote area, a polling booth is set up — democracy comes to the citizen.' },
        7: { title: 'Trust Through Witness', text: 'The mock poll at dawn, witnessed by agents from ALL contesting parties, ensures EVMs start at zero. This multi-party observation under Article 324 converts skepticism into documented trust.' },
        8: { title: 'The Unbreakable Chain', text: 'After voting, numbered seals on the Control Unit, recorded in Form 16 and witnessed by agents, create an unbreakable chain of custody under Article 324. From booth to counting hall — zero room for tampering.' },
    };

    // State
    const citizen = JSON.parse(localStorage.getItem('loktantra_citizen')) || {};
    const state = {
        playerId: citizen.email || ('player_' + Math.random().toString(36).slice(2, 10)),
        playerDetails: citizen,
        currentLevel: null,
        levelData: null,
        levelMeta: null,
        levelScores: {},
        totalScore: 0,
        timer: null,
        timeElapsed: 0,
        hintsUsed: 0,
        maxHints: 3,
        phase: 'select', // select | playing | complete
    };

    const levelHandlers = {};

    /** Register a level handler */
    function registerLevel(id, handler) {
        levelHandlers[id] = handler;
    }

    /** Start a level */
    async function startLevel(levelId) {
        // Enforce registration
        if (!state.playerDetails.name) {
            window.location.href = '/?register=true';
            return;
        }

        try {
            state.currentLevel = levelId;
            state.hintsUsed = 0;
            state.timeElapsed = 0;
            state.phase = 'playing';

            // Fetch level data from backend
            const resp = await ApiClient.getLevel(levelId, state.playerId);
            state.levelData = resp.data;
            state.levelMeta = resp.meta;

            // Update UI
            document.getElementById('level-select-screen').classList.add('hidden');
            document.getElementById('level-complete-screen').classList.add('hidden');
            document.getElementById('level-play-screen').classList.remove('hidden');
            document.getElementById('active-level-title').textContent = resp.meta.title;
            document.getElementById('active-level-objective').textContent = resp.meta.objective;
            document.getElementById('level-score').textContent = '0';
            document.getElementById('hints-count').textContent = `(${state.maxHints} left)`;

            // Set contextual insight bar
            const insight = LEVEL_INSIGHTS[levelId];
            if (insight) {
                document.getElementById('insight-title').textContent = insight.title;
                document.getElementById('insight-text').textContent = insight.text;
            }

            // Initialize level handler
            const handler = levelHandlers[levelId];
            if (handler && handler.init) {
                handler.init(resp.data, resp.meta, document.getElementById('level-content'));
            }

            // Start timer
            startTimer(resp.meta.max_time || 120);
        } catch (err) {
            console.error('Failed to start level:', err);
            showToast('Failed to load level. Please try again.', 'error');
        }
    }

    /** Submit current level */
    async function submitLevel() {
        if (state.phase !== 'playing') return;
        stopTimer();

        const handler = levelHandlers[state.currentLevel];
        if (!handler || !handler.getSubmission) return;

        const submission = handler.getSubmission();
        submission.time_seconds = state.timeElapsed;
        submission.hints_used = state.hintsUsed;
        submission.player_id = state.playerId;

        try {
            const result = await ApiClient.submitLevel(state.currentLevel, submission);
            state.levelScores[state.currentLevel] = result.score;
            state.totalScore = Object.values(state.levelScores).reduce((a, s) => a + s.score, 0);

            // Auto-submit to leaderboard
            await autoSubmitToLeaderboard();

            showCompleteScreen(result);
        } catch (err) {
            console.error('Submit failed:', err);
            showToast('Submission failed. Please try again.', 'error');
            startTimer(0);
        }
    }

    /** Auto-submit current progress to global leaderboard */
    async function autoSubmitToLeaderboard() {
        if (!state.playerDetails.name) return;

        const levelsCompleted = Object.keys(state.levelScores).length;
        
        // Calculate saga-specific scores
        let voterScore = 0;
        let officerScore = 0;
        
        Object.entries(state.levelScores).forEach(([id, scoreObj]) => {
            const levelId = parseInt(id);
            if (levelId <= 4) voterScore += scoreObj.score;
            else if (levelId >= 5) officerScore += scoreObj.score;
        });

        // Determine saga type based on completed levels
        const sagaType = (voterScore > 0 && officerScore > 0) ? 'both' : (voterScore > 0 ? 'voter' : 'officer');

        try {
            await ApiClient.submitScore(
                state.playerDetails.name,
                state.totalScore,
                levelsCompleted,
                sagaType,
                state.playerDetails.age,
                state.playerDetails.email,
                voterScore,
                officerScore
            );
        } catch (err) {
            console.error('Leaderboard auto-sync failed:', err);
        }
    }

    /** Show level complete screen */
    function showCompleteScreen(result) {
        state.phase = 'complete';

        document.getElementById('level-play-screen').classList.add('hidden');
        document.getElementById('level-complete-screen').classList.remove('hidden');

        const score = result.score;
        const icons = ['&#128546;', '&#128079;', '&#127881;', '&#127942;'];
        document.getElementById('complete-icon').innerHTML = icons[score.stars] || icons[0];
        document.getElementById('complete-title').textContent = score.stars >= 3 ? 'Outstanding!' : score.stars >= 2 ? 'Excellent Work!' : score.stars >= 1 ? 'Good Job!' : 'Keep Practicing!';
        document.getElementById('complete-message').textContent =
            `You scored ${score.score} out of ${score.max_score} on ${state.levelMeta.title}`;

        // Stars
        const starsEl = document.getElementById('complete-stars');
        const starSpans = starsEl.querySelectorAll('.star');
        starSpans.forEach((s, i) => {
            s.classList.toggle('earned', i < score.stars);
        });

        // Breakdown
        document.getElementById('breakdown-accuracy').textContent = score.base_accuracy;
        document.getElementById('breakdown-time').textContent = `+${score.time_bonus}`;
        document.getElementById('breakdown-completion').textContent = `+${score.completion_bonus}`;
        document.getElementById('breakdown-hints').textContent = `-${score.hint_penalty}`;
        document.getElementById('breakdown-total').textContent = `${score.score}/${score.max_score}`;

        // Update global displays
        document.getElementById('total-score').textContent = state.totalScore;
        const completedCount = Object.keys(state.levelScores).length;
        document.getElementById('levels-done').textContent = `${completedCount}/8`;
        const pct = (completedCount / 8) * 100;
        document.getElementById('progress-fill').style.width = `${pct}%`;
        const pctEl = document.getElementById('progress-pct');
        if (pctEl) pctEl.textContent = `${Math.round(pct)}%`;

        // Update stars on level select card
        const cardStars = document.getElementById(`stars-${state.currentLevel}`);
        if (cardStars) {
            cardStars.querySelectorAll('.star').forEach((s, i) => {
                s.classList.toggle('earned', i < score.stars);
            });
        }

        // Show complete badge on level card
        const badge = document.getElementById(`complete-badge-${state.currentLevel}`);
        if (badge) badge.classList.remove('hidden');

        // Auto-load ECI insight on completion
        loadCompletionInsight();
    }

    /** Load ECI insight into the completion screen */
    async function loadCompletionInsight() {
        const titleEl = document.getElementById('complete-insight-title');
        const textEl = document.getElementById('complete-insight-text');
        const refEl = document.getElementById('complete-insight-ref');

        titleEl.textContent = 'Loading ECI Insight...';
        textEl.textContent = '';
        refEl.textContent = '';

        try {
            const resp = await ApiClient.getExplanation(state.currentLevel, state.playerId);
            const exp = resp.explanation;
            titleEl.textContent = exp.title;
            textEl.textContent = exp.explanation;
            refEl.textContent = `${exp.article_reference} · Source: ${resp.source}`;

            if (exp.fun_fact) {
                refEl.textContent += `\n💡 Fun Fact: ${exp.fun_fact}`;
            }
        } catch (err) {
            titleEl.textContent = 'ECI Insight';
            textEl.textContent = LEVEL_INSIGHTS[state.currentLevel]?.text || 'Every aspect of India\'s electoral process upholds constitutional democracy.';
            refEl.textContent = 'Part XV — Articles 324-329';
        }
    }

    /** Show ECI explanation modal (deep dive from "Learn More" button) */
    async function showInsightModal() {
        const modal = document.getElementById('explanation-modal');
        const body = document.getElementById('modal-body');
        modal.classList.remove('hidden');

        body.innerHTML = '<div class="space-y-2"><div class="animate-shimmer rounded-lg h-4 bg-white/5"></div><div class="animate-shimmer rounded-lg h-4 bg-white/5 w-3/4"></div><div class="animate-shimmer rounded-lg h-3 bg-white/5 w-1/2 mt-4"></div></div>';

        try {
            const resp = await ApiClient.getExplanation(state.currentLevel, state.playerId);
            const exp = resp.explanation;
            body.innerHTML = `
                <h5 class="font-display font-bold text-lg">${esc(exp.title)}</h5>
                <p class="text-gray-300 leading-relaxed text-sm">${esc(exp.explanation)}</p>
                <div class="glass-card p-3 mt-4 border-l-4 border-saffron-500/40">
                    <p class="text-xs text-saffron-400 font-semibold">${esc(exp.article_reference)}</p>
                </div>
                ${exp.fun_fact ? `<div class="mt-3 p-3 rounded-xl bg-chakra-500/10 border border-chakra-500/20">
                    <p class="text-xs text-chakra-400"><strong>Fun Fact:</strong> ${esc(exp.fun_fact)}</p>
                </div>` : ''}
                <p class="text-[10px] text-gray-600 mt-4">Source: ${esc(resp.source)} · Grounded in ECI Constitutional Principles</p>`;
        } catch (err) {
            body.innerHTML = '<p class="text-red-400">Failed to load explanation. Try again later.</p>';
        }
    }

    /** Show explanation (alias for backward compat) */
    function showExplanation() { showInsightModal(); }

    function closeExplanation() {
        document.getElementById('explanation-modal').classList.add('hidden');
    }

    /** Show How to Play modal */
    function showHowToPlay() {
        document.getElementById('how-to-play-modal').classList.remove('hidden');
    }

    /** Navigate back to level selection */
    function backToSelect() {
        stopTimer();
        state.phase = 'select';
        state.currentLevel = null;
        document.getElementById('level-play-screen').classList.add('hidden');
        document.getElementById('level-complete-screen').classList.add('hidden');
        document.getElementById('level-select-screen').classList.remove('hidden');
    }

    /** Navigate to next level */
    function nextLevel() {
        const next = (state.currentLevel || 0) + 1;
        if (next <= 8) {
            startLevel(next);
        } else {
            showToast('Congratulations! You\'ve completed all 8 levels! 🎉', 'success');
            backToSelect();
        }
    }

    /** Request a hint */
    function requestHint() {
        if (state.hintsUsed >= state.maxHints) {
            showToast('No hints remaining!', 'warning');
            return;
        }
        state.hintsUsed++;
        document.getElementById('hints-count').textContent = `(${state.maxHints - state.hintsUsed} left)`;

        const handler = levelHandlers[state.currentLevel];
        if (handler && handler.showHint) {
            handler.showHint(state.hintsUsed);
        }
    }

    // Timer
    function startTimer(maxTime) {
        stopTimer();
        state.timeElapsed = 0;
        const timerEl = document.getElementById('level-timer');
        state.timer = setInterval(() => {
            state.timeElapsed++;
            const remaining = Math.max(0, maxTime - state.timeElapsed);
            const m = Math.floor(remaining / 60);
            const s = remaining % 60;
            timerEl.textContent = `${m}:${s.toString().padStart(2, '0')}`;

            // Color change when time is running low
            if (remaining <= 10) {
                timerEl.classList.add('text-red-400');
                timerEl.classList.remove('text-amber-400');
            } else if (remaining <= 30) {
                timerEl.classList.add('text-amber-400');
                timerEl.classList.remove('text-red-400');
            } else {
                timerEl.classList.remove('text-red-400', 'text-amber-400');
            }

            if (remaining <= 0) {
                showToast('Time\'s up! Submitting your answers...', 'warning');
                submitLevel();
            }
        }, 1000);
    }

    function stopTimer() {
        if (state.timer) clearInterval(state.timer);
        state.timer = null;
    }

    /** Simple toast notification */
    function showToast(message, type) {
        const existing = document.getElementById('game-toast');
        if (existing) existing.remove();

        const colors = { success: 'bg-chakra-500/20 border-chakra-500/30 text-chakra-400', error: 'bg-red-500/20 border-red-500/30 text-red-400', warning: 'bg-amber-500/20 border-amber-500/30 text-amber-400' };
        const toast = document.createElement('div');
        toast.id = 'game-toast';
        toast.className = `fixed top-20 right-4 z-[200] px-5 py-3 rounded-xl border text-sm font-medium ${colors[type] || colors.success} animate-slide-up`;
        toast.setAttribute('role', 'alert');
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

    function esc(str) {
        const d = document.createElement('div');
        d.textContent = str || '';
        return d.innerHTML;
    }

    function getState() {
        return { ...state, levelScores: { ...state.levelScores } };
    }

    return {
        startLevel, submitLevel, backToSelect, nextLevel,
        requestHint, showExplanation, showInsightModal, closeExplanation,
        showHowToPlay, registerLevel, getState,
    };
})();

window.GameApp = GameApp;
