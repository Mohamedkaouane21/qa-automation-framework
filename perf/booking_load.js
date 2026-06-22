// Lightweight k6 load test for the restful-booker API.
// Run locally:  k6 run perf/booking_load.js
// In CI it runs as an informational (non-blocking) job.
//
// Goal: demonstrate a non-functional / performance check with explicit SLOs,
// not stress the public demo service -- hence a small, short load profile.

import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = __ENV.API_BASE_URL || "https://restful-booker.herokuapp.com";

export const options = {
  stages: [
    { duration: "10s", target: 5 }, // ramp up to 5 virtual users
    { duration: "20s", target: 5 }, // hold
    { duration: "5s", target: 0 }, // ramp down
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"], // <1% errors
    http_req_duration: ["p(95)<800"], // 95% of requests under 800ms
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/booking`);
  check(res, {
    "status is 200": (r) => r.status === 200,
    "body is a list": (r) => Array.isArray(r.json()),
  });
  sleep(1);
}
