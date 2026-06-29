const path = require('path');
const { buildWalkthrough, WT_EXAMPLE, WT_PART_B } = require('../viz/walkthrough.js');

let allPassed = true;

function assert(condition, message, actual, expected) {
  if (condition) {
    console.log(`[PASS] ${message}`);
  } else {
    console.log(`[FAIL] ${message}`);
    console.log(`  Actual:   ${JSON.stringify(actual)}`);
    console.log(`  Expected: ${JSON.stringify(expected)}`);
    allPassed = false;
  }
}

function assertArrayEquals(actual, expected, message) {
  const sortedActual = [...actual].sort((a, b) => a - b);
  const sortedExpected = [...expected].sort((a, b) => a - b);
  const condition = sortedActual.length === sortedExpected.length &&
                    sortedActual.every((val, idx) => val === sortedExpected[idx]);
  assert(condition, message, sortedActual, sortedExpected);
}

console.log("=== RUNNING VIZ WALKTHROUGH LOGIC VALIDATION ===");

// --- PART A ---
console.log("\n--- PART A (WT_EXAMPLE) ---");
const resultA = buildWalkthrough(WT_EXAMPLE);
const framesA = resultA.frames;
const solvencyFramesA = framesA.filter(f => f.type === "solvency");
const fearFramesA     = framesA.filter(f => f.type === "fear");

// Assert solvency frame at k=0 has hi.solvency = [2,3,5] (sorted)
assertArrayEquals(solvencyFramesA[0].hi.solvency, [2, 3, 5], "Gen k=0: solvency frame has hi.solvency = [2, 3, 5]");
// Assert fear frame at k=0 has hi.fear = [] (μ=0, no fear)
assertArrayEquals(fearFramesA[0].hi.fear, [], "Gen k=0: fear frame has hi.fear = []");

// Assert solvency frame at k=1 has hi.solvency = [6]
assertArrayEquals(solvencyFramesA[1].hi.solvency, [6], "Gen k=1: solvency frame has hi.solvency = [6]");
// Assert fear frame at k=1 has hi.fear = []
assertArrayEquals(fearFramesA[1].hi.fear, [], "Gen k=1: fear frame has hi.fear = []");

// Assert solvency frame at k=2 has hi.solvency = [7]
assertArrayEquals(solvencyFramesA[2].hi.solvency, [7], "Gen k=2: solvency frame has hi.solvency = [7]");

// Assert last frame has type === "halt"
const lastFrameA = framesA[framesA.length - 1];
assert(lastFrameA.type === "halt", "Last frame type is 'halt'", lastFrameA.type, "halt");

// Assert all 7 nodes are active in the final table snapshot
const allActiveA = lastFrameA.table.every(row => row.active === true);
assert(allActiveA, "All 7 nodes are active in final table snapshot", lastFrameA.table.map(row => `${row.node}:${row.active}`), "all active");


// --- PART B ---
console.log("\n--- PART B (WT_PART_B) ---");
const resultB = buildWalkthrough(WT_PART_B);
const framesB = resultB.frames;
const solvencyFramesB = framesB.filter(f => f.type === "solvency");
const fearFramesB     = framesB.filter(f => f.type === "fear");

// Assert solvency frame at k=0 has hi.solvency = []
assertArrayEquals(solvencyFramesB[0].hi.solvency, [], "Gen k=0: solvency frame has hi.solvency = []");
// Assert fear frame at k=0: hi.fear sorted = [2,6]
assertArrayEquals(fearFramesB[0].hi.fear, [2, 6], "Gen k=0: fear frame has hi.fear = [2, 6]");
// Assert the fear frame caption contains "1/7"
assert(fearFramesB[0].caption.includes("1/7"), "Gen k=0: fear frame caption contains '1/7'", fearFramesB[0].caption, "contains '1/7'");

// Assert solvency frame at k=1 has hi.solvency = [5]
assertArrayEquals(solvencyFramesB[1].hi.solvency, [5], "Gen k=1: solvency frame has hi.solvency = [5]");
// Assert fear frame at k=1: hi.fear sorted = [3]
assertArrayEquals(fearFramesB[1].hi.fear, [3], "Gen k=1: fear frame has hi.fear = [3]");
// Assert the fear frame caption contains "2/7"
assert(fearFramesB[1].caption.includes("2/7"), "Gen k=1: fear frame caption contains '2/7'", fearFramesB[1].caption, "contains '2/7'");

// Assert solvency frame at k=2 has hi.solvency sorted = [4,7]
assertArrayEquals(solvencyFramesB[2].hi.solvency, [4, 7], "Gen k=2: solvency frame has hi.solvency = [4, 7]");
// Assert fear frame at k=2 has hi.fear = []
assertArrayEquals(fearFramesB[2].hi.fear, [], "Gen k=2: fear frame has hi.fear = []");

// Assert last frame has type === "halt"
const lastFrameB = framesB[framesB.length - 1];
assert(lastFrameB.type === "halt", "Last frame type is 'halt'", lastFrameB.type, "halt");

// Assert all 7 nodes are active in the final table snapshot
const allActiveB = lastFrameB.table.every(row => row.active === true);
assert(allActiveB, "All 7 nodes are active in final table snapshot", lastFrameB.table.map(row => `${row.node}:${row.active}`), "all active");

if (!allPassed) {
  console.log("\nSome assertions FAILED.");
  process.exit(1);
} else {
  console.log("\nAll assertions PASSED.");
}
