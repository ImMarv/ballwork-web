import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const SEARCH_LIMIT = Number(__ENV.SEARCH_LIMIT || 10);
const YEAR = __ENV.SEASON_YEAR || '2023';
const TEAM_COMPETITION_ID = Number(__ENV.TEAM_COMPETITION_ID || 39);

const QUERIES = (__ENV.SEARCH_QUERIES || 'messi,ronaldo,arsenal,barcelona,premier,brazil')
  .split(',')
  .map((q) => q.trim())
  .filter(Boolean);

const failureRate = new Rate('scenario1_failure_rate');

export const options = {
  scenarios: {
    search_and_fetch: {
      executor: 'ramping-arrival-rate',
      startRate: Number(__ENV.START_RATE || 5),
      timeUnit: '1s',
      preAllocatedVUs: Number(__ENV.PREALLOCATED_VUS || 20),
      maxVUs: Number(__ENV.MAX_VUS || 100),
      stages: [
        { target: Number(__ENV.STAGE1_TARGET || 20), duration: __ENV.STAGE1_DURATION || '1m' },
        { target: Number(__ENV.STAGE2_TARGET || 60), duration: __ENV.STAGE2_DURATION || '3m' },
        { target: Number(__ENV.STAGE3_TARGET || 80), duration: __ENV.STAGE3_DURATION || '2m' },
        { target: 0, duration: __ENV.STAGE4_DURATION || '30s' },
      ],
      tags: { scenario: 'scenario1-search-and-fetch' },
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1200', 'p(99)<2500'],
    scenario1_failure_rate: ['rate<0.05'],
  },
};

export function setup() {
  const health = http.get(`${BASE_URL}/health`, { tags: { endpoint: 'health' } });
  const ok = check(health, {
    'health status is 200': (r) => r.status === 200,
  });

  if (!ok) {
    throw new Error(`Health check failed. status=${health.status}, body=${health.body}`);
  }

  return { queries: QUERIES };
}

function randomFrom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function parseSearchPayload(response) {
  let payload = null;
  try {
    payload = response.json();
  } catch (_err) {
    return { players: [], teams: [], competitions: [] };
  }

  return {
    players: Array.isArray(payload?.players) ? payload.players : [],
    teams: Array.isArray(payload?.teams) ? payload.teams : [],
    competitions: Array.isArray(payload?.competitions) ? payload.competitions : [],
  };
}

export default function (data) {
  const q = randomFrom(data.queries);

  group('search', () => {
    const searchRes = http.get(
      `${BASE_URL}/stats/search?query=${encodeURIComponent(q)}&limit=${SEARCH_LIMIT}`,
      { tags: { endpoint: 'stats-search' } }
    );

    const searchOk = check(searchRes, {
      'search status is 200': (r) => r.status === 200,
      'search content-type json': (r) => (r.headers['Content-Type'] || '').includes('application/json'),
    });

    if (!searchOk) {
      failureRate.add(1);
      return;
    }

    const { players, teams, competitions } = parseSearchPayload(searchRes);

    const player = players[0];
    const team = teams[0];
    const competition = competitions[0];

    let detailRes = null;

    if (player?.id) {
      detailRes = http.get(
        `${BASE_URL}/stats/player/${player.id}?year=${YEAR}`,
        { tags: { endpoint: 'stats-player-detail', entity: 'player' } }
      );
    } else if (team?.id) {
      const compId = competition?.id || TEAM_COMPETITION_ID;
      detailRes = http.get(
        `${BASE_URL}/stats/team/${team.id}?competition_id=${compId}&year=${YEAR}`,
        { tags: { endpoint: 'stats-team-detail', entity: 'team' } }
      );
    } else if (competition?.id) {
      detailRes = http.get(
        `${BASE_URL}/stats/competition?competition_id=${competition.id}`,
        { tags: { endpoint: 'stats-competition-detail', entity: 'competition' } }
      );
    }

    if (!detailRes) {
      failureRate.add(1);
      return;
    }

    const detailOk = check(detailRes, {
      'detail status is 200': (r) => r.status === 200,
      'detail content-type json': (r) => (r.headers['Content-Type'] || '').includes('application/json'),
    });

    failureRate.add(detailOk ? 0 : 1);
  });

  sleep(Number(__ENV.THINK_TIME_SECONDS || 0.3));
}
