/**
 * LOKTANTRA — API Client
 * Handles all communication with the Flask backend.
 */
const ApiClient = {
    async getLevel(levelId, playerId) {
        const resp = await fetch(`/game/level/${levelId}?player_id=${playerId || 'anonymous'}`);
        if (!resp.ok) throw new Error(`Failed to load level ${levelId}`);
        return resp.json();
    },

    async submitLevel(levelId, submission) {
        const resp = await fetch(`/game/level/${levelId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(submission),
        });
        if (!resp.ok) throw new Error('Submission failed');
        return resp.json();
    },

    async getExplanation(levelId, playerId, context) {
        const resp = await fetch('/api/explain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ level_id: levelId, player_id: playerId, context }),
        });
        if (!resp.ok) throw new Error('Explanation request failed');
        return resp.json();
    },

    async getLeaderboard(limit, saga) {
        const params = new URLSearchParams();
        if (limit) params.set('limit', limit);
        if (saga) params.set('saga', saga);
        const resp = await fetch(`/leaderboard/data?${params}`);
        return resp.json();
    },

    async submitScore(playerName, totalScore, levelsCompleted, sagaType, age, email, voterScore, officerScore) {
        const resp = await fetch('/leaderboard/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                player_name: playerName, 
                total_score: totalScore, 
                levels_completed: levelsCompleted, 
                saga_type: sagaType,
                age: age,
                email: email,
                voter_score: voterScore,
                officer_score: officerScore
            }),
        });
        return resp.json();
    },

    async saveProgress(sessionId, data) {
        const resp = await fetch('/api/progress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, ...data }),
        });
        return resp.json();
    },

    async getProgress(sessionId) {
        const resp = await fetch(`/api/progress/${sessionId}`);
        return resp.json();
    },
};

window.ApiClient = ApiClient;
