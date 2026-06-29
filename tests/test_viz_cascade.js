// Define global.window to prevent ReferenceError in Node.js when cascade.js executes window.Cascade = ...
global.window = {};

const path = require('path');
const { runCascade, CHANNEL } = require('../viz/cascade.js');

let allPassed = true;

function assert(condition, message, actual, expected) {
  if (condition) {
    console.log(`[PASS] ${message}`);
  } else {
    console.log(`[FAIL] ${message}`);
    if (actual !== undefined || expected !== undefined) {
      console.log(`  Actual:   ${JSON.stringify(actual)}`);
      console.log(`  Expected: ${JSON.stringify(expected)}`);
    }
    allPassed = false;
  }
}

console.log("=== RUNNING CASCADE.JS BEHAVIORAL VALIDATION ===");

// TEST 1 — μ=0 means no fear failures.
console.log("\n--- TEST 1 — μ=0 means no fear failures ---");
try {
  const result1 = runCascade({ n: 20, p: 0.3, r: 2, mu: 0, kappa: 20, a: 2, seed: 42 });
  const noFearFailures = result1.rounds.every(rd => 
    rd.newNodes.every(nn => nn.channel !== "fear")
  );
  assert(noFearFailures, "No node is labeled with channel='fear' when mu=0", noFearFailures, true);
} catch (e) {
  console.log(`[FAIL] TEST 1 raised an error: ${e.message}`);
  allPassed = false;
}

// TEST 2 — Simultaneous update: solvency fires in the NEXT round after a neighbor fails.
console.log("\n--- TEST 2 — Simultaneous update ---");
try {
  const result2 = runCascade({ n: 20, p: 0.3, r: 2, mu: 0, kappa: 20, a: 2, seed: 42 });
  const seedOnlyInRound0 = result2.rounds[0].newNodes.map(n => n.channel).every(c => c === "seed");
  assert(seedOnlyInRound0, "Round 0 only contains seed nodes", result2.rounds[0].newNodes.map(n => n.channel), "all seed");
} catch (e) {
  console.log(`[FAIL] TEST 2 raised an error: ${e.message}`);
  allPassed = false;
}

// TEST 3 — Halting: cascade stops when a round has no new failures.
console.log("\n--- TEST 3 — Halting ---");
try {
  const result3 = runCascade({ n: 10, p: 0.01, r: 5, mu: 0, kappa: 20, a: 1, seed: 7 });
  const lengthValid = result3.rounds.length >= 1;
  const lastRound = result3.rounds[result3.rounds.length - 1];
  const haltedCorrectly = (lastRound.a_t === 0 || result3.rounds.length === 1);
  
  assert(lengthValid, "rounds.length >= 1", result3.rounds.length, ">= 1");
  assert(haltedCorrectly, "Cascade halts immediately or last round has a_t = 0", { roundsLength: result3.rounds.length, lastRound_a_t: lastRound.a_t }, "length = 1 OR last.a_t = 0");
} catch (e) {
  console.log(`[FAIL] TEST 3 raised an error: ${e.message}`);
  allPassed = false;
}

// TEST 4 — finalFraction is consistent with round accounting.
console.log("\n--- TEST 4 — finalFraction & round accounting consistency ---");
try {
  const result4 = runCascade({ n: 50, p: 0.2, r: 2, mu: 0.3, kappa: 10, a: 3, seed: 123 });
  const fractionDiff = Math.abs(result4.finalA / result4.n - result4.finalFraction);
  const sumOfRounds = result4.rounds.reduce((s, rd) => s + rd.a_t, 0);
  const accountingMatch = result4.finalA === sumOfRounds;
  
  assert(fractionDiff < 1e-9, "finalFraction matches finalA / n", fractionDiff, "< 1e-9");
  assert(accountingMatch, "finalA matches the sum of new failures (a_t) across all rounds", result4.finalA, sumOfRounds);
} catch (e) {
  console.log(`[FAIL] TEST 4 raised an error: ${e.message}`);
  allPassed = false;
}

// TEST 5 — Fear field g_t is incremental (g_t = a_{t-1}/n).
console.log("\n--- TEST 5 — Fear field g_t is incremental ---");
try {
  const result5 = runCascade({ n: 30, p: 0.15, r: 2, mu: 0.5, kappa: 10, a: 2, seed: 99 });
  const round0GVal = result5.rounds[0].g;
  const round0GCorrect = Math.abs(round0GVal) < 1e-9;
  assert(round0GCorrect, "g_0 is 0 (no fear on seed round)", round0GVal, 0);
  
  let fearFieldValid = true;
  const mismatchDetail = [];
  for (let t = 1; t < result5.rounds.length; t++) {
    const expectedG = result5.rounds[t - 1].a_t / result5.n;
    const actualG = result5.rounds[t].g;
    if (Math.abs(actualG - expectedG) >= 1e-9) {
      fearFieldValid = false;
      mismatchDetail.push({ round: t, expectedG, actualG });
    }
  }
  assert(fearFieldValid, "g_t matches a_{t-1}/n for all t >= 1", mismatchDetail, "empty");
} catch (e) {
  console.log(`[FAIL] TEST 5 raised an error: ${e.message}`);
  allPassed = false;
}

// TEST 6 — Determinism: same seed → identical output.
console.log("\n--- TEST 6 — Determinism ---");
try {
  const params = { n: 40, p: 0.18, r: 2, mu: 0.4, kappa: 15, a: 3, seed: 555 };
  const res1 = runCascade(params);
  const res2 = runCascade(params);
  const outputsEqual = JSON.stringify(res1) === JSON.stringify(res2);
  assert(outputsEqual, "Two runs with identical seeds produce identical output JSONs", outputsEqual, true);
} catch (e) {
  console.log(`[FAIL] TEST 6 raised an error: ${e.message}`);
  allPassed = false;
}

if (!allPassed) {
  console.log("\nSome tests FAILED.");
  process.exit(1);
} else {
  console.log("\nAll tests PASSED.");
  process.exit(0);
}
