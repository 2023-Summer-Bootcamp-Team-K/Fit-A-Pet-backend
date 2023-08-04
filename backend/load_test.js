import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '3m', target: 25 },     // 먼저 3분 동안 VUser 1에서 25까지 서서히 올린다.
        { duration: '3m',target: 25 },     // Vuser 25에서 10분간 유지한다.
        { duration: '3m', target: 125 },    // 다시 3분간 25에서 125까지 서서히 올린다.
        { duration: '3m',target: 125 },    // 30분간 유지
        { duration: '3m', target: 0 },      // 3분 동안 Vuser 0으로 내려온다.
    ],
    thresholds: {
        http_req_duration: ['p(95)<138'],   // 전체 요청의 95%가 138ms 안에 들어오면 성공
    },
};

const BASE_URL = 'http://localhost:8000/api/pets';

export default function () {
    // 사용자 ID를 2 또는 3으로 설정
    const user_id = Math.random() < 0.5 ? 2 : 3;
    const url = `${BASE_URL}/list/${user_id}/`;

    // API 요청
    const res = http.get(url);

    // 응답 확인
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response has data': (r) => r.json().length > 0,
    });

    // 부하 테스트 간 지연
    sleep(1);
}
