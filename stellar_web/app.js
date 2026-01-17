
// DOM Elements
const els = {
    tapeList: document.getElementById('tape-stream'),
    grid: document.getElementById('main-grid'),
    output: document.getElementById('output-list'),
    log: document.getElementById('log-content'),
    btnStart: document.getElementById('btn-start'),
    btnPause: document.getElementById('btn-pause'),
    speedSlider: document.getElementById('speed-slider'),
    statusBar: document.getElementById('status-bar')
};

// State
let state = {
    isRunning: false,
    isPaused: false,
    delay: 100, // ms
    tapeA: [],
    tapeB: [],
    memory: Array(15).fill(null).map(() => Array(15).fill(0)),
    calcs: [
        { el: document.getElementById('calc-0'), status: document.querySelector('#calc-0 .calc-status'), regs: [] },
        { el: document.getElementById('calc-1'), status: document.querySelector('#calc-1 .calc-status'), regs: [] },
        { el: document.getElementById('calc-2'), status: document.querySelector('#calc-2 .calc-status'), regs: [] }
    ],
    aggregator: {
        el: document.getElementById('calc-3'),
        status: document.querySelector('#calc-3 .calc-status')
    },
    gridCells: []
};

// -- INITIALIZATION --
function init() {
    // Build Calc Registers
    state.calcs.forEach(c => {
        const grid = c.el.querySelector('.register-grid');
        for (let i = 0; i < 38; i++) {
            const cell = document.createElement('div');
            cell.className = 'reg-cell';
            cell.textContent = '00';
            grid.appendChild(cell);
            c.regs.push(cell);
        }
    });

    // Build Main Grid
    for (let r = 0; r < 15; r++) {
        for (let c = 0; c < 15; c++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.id = `cell-${r}-${c}`;
            cell.textContent = '--';
            els.grid.appendChild(cell);
            state.gridCells.push(cell);
        }
    }

    // Bind Listeners
    els.btnStart.addEventListener('click', startSimulation);
    els.btnPause.addEventListener('click', () => {
        state.isPaused = !state.isPaused;
        log(state.isPaused ? "SYSTEM PAUSED" : "SYSTEM RESUMED");
    });
    els.speedSlider.addEventListener('input', (e) => {
        state.delay = parseInt(e.target.value);
    });
}

// -- HELPERS --
const delay = (ms) => new Promise(res => setTimeout(res, ms));
const wait = async () => {
    while (state.isPaused) await delay(100);
    await delay(state.delay);
};

function log(msg) {
    const div = document.createElement('div');
    div.className = 'log-message';
    div.innerText = `> ${msg}`;
    els.log.appendChild(div);
    els.log.scrollTop = els.log.scrollHeight;
}

function updateTape(tapeData, activeIdx) {
    els.tapeList.innerHTML = '';
    tapeData.forEach((item, i) => {
        const div = document.createElement('div');
        div.className = `tape-item ${i === activeIdx ? 'active-read' : ''}`;
        div.innerText = `${item.label}: ${item.val}`;
        els.tapeList.appendChild(div);
    });
    // Scroll to keep active int middle
    if (activeIdx > -1) {
        const itemH = 31;
        els.tapeList.style.transform = `translateY(-${activeIdx * itemH}px)`;
    }
}

function getGridCell(r, c) { return document.getElementById(`cell-${r}-${c}`); }

// -- SIMULATION LOGIC --
async function startSimulation() {
    if (state.isRunning) return;
    state.isRunning = true;
    state.isPaused = false;
    els.btnStart.disabled = true;
    els.statusBar.textContent = "STATUS: RUNNING";
    els.output.innerHTML = '';

    // Generate Data
    log("INIT: GENERATING DATA TAPES (BLOCK A & BLOCK B)...");

    // Tape A (Baseline)
    state.tapeA = [];
    state.tapeB = [];

    for (let i = 0; i < 225; i++) {
        const valA = Math.floor(Math.random() * 40) + 10;
        const spread = Math.random() < 0.2 ? Math.floor(Math.random() * 10) + 6 : Math.floor(Math.random() * 6);
        const valB = valA + spread;

        state.tapeA.push({ idx: i, val: valA, label: `A-${String(i).padStart(3, '0')}` });
        state.tapeB.push({ idx: i, val: valB, label: `B-${String(i).padStart(3, '0')}` });
    }

    // PHASE 1: INGEST
    log("PHASE 1 START: INGEST BASELINE DATA (BLOCK A)\nLoading Block A (Opening Prices) into Memory Grid.");
    updateTape(state.tapeA, -1);
    await wait();

    let lastCalcId = -1;

    for (let i = 0; i < state.tapeA.length; i++) {
        const item = state.tapeA[i];
        const r = Math.floor(item.idx / 15);
        const c = item.idx % 15;
        const calcId = Math.floor(r / 5) % 3;
        const regId = item.idx % 38;

        // Context Switch Check
        if (calcId !== lastCalcId && lastCalcId !== -1) {
            log(`ARCHITECTURAL SWITCH: Moving to Calculator ${calcId}.\nReason: Crossing Stripe Boundary (Row ${r}).`);
            state.calcs[lastCalcId].el.classList.remove('active-calc');
            state.calcs[calcId].el.classList.add('active-calc');
            await wait();
        }
        lastCalcId = calcId;
        state.calcs[calcId].el.classList.add('active-calc');

        // 1. Read Tape
        updateTape(state.tapeA, i);
        // log(`Reading Tape: ${item.val}`);

        // 2. Route/Store
        state.calcs[calcId].status.textContent = `ROUTING ${item.val} -> GRID[${r},${c}]`;
        const reg = state.calcs[calcId].regs[regId];
        reg.textContent = item.val;
        reg.classList.add('highlight');

        // 3. Latch Grid
        const cell = getGridCell(r, c);
        cell.textContent = item.val;
        cell.className = 'grid-cell latched';
        state.memory[r][c] = item.val;

        await wait();

        // Cleanup
        reg.classList.remove('highlight');
        if (i % 5 === 0) await delay(10); // Slight speedup on renders?
    }

    state.calcs.forEach(c => c.el.classList.remove('active-calc'));
    log("PHASE 1 COMPLETE: MEMORY LOADED.\nReady for Real-Time Streaming Computation.");
    await wait(); await wait();

    // PHASE 2: STREAM
    log("PHASE 2 START: STREAMING COMPUTATION (BLOCK B)\nCrucial: Block B is NOT stored. It is subtracted on the fly.");
    updateTape(state.tapeB, -1);
    await wait();

    lastCalcId = -1;
    state.calcs.forEach(c => {
        c.regs.forEach(r => { r.textContent = '--'; r.classList.remove('highlight'); });
    });

    for (let i = 0; i < state.tapeB.length; i++) {
        const item = state.tapeB[i];
        const r = Math.floor(item.idx / 15);
        const c = item.idx % 15;
        const calcId = Math.floor(r / 5) % 3;

        // Switch
        if (calcId !== lastCalcId) {
            state.calcs.forEach(u => u.el.classList.remove('active-calc'));
            state.calcs[calcId].el.classList.add('active-calc');
            lastCalcId = calcId;
        }

        // 1. Read
        updateTape(state.tapeB, i);

        // 2. Compute
        const baseVal = state.memory[r][c];
        const diff = item.val - baseVal;

        state.calcs[calcId].status.textContent = `OP: ${item.val} - ${baseVal} = ${diff}`;

        const cell = getGridCell(r, c);
        cell.classList.add('active-compute');

        await wait();

        // 3. Output
        if (diff > 5) {
            log(`SIGNAL FIRED: [${r},${c}] Spread +${diff}>5. BUY!`);
            cell.className = 'grid-cell buy-signal';

            // AGGREGATOR STEP
            state.aggregator.el.classList.add('active-calc'); // Highlight Aggregator
            state.aggregator.status.textContent = `SWEEPING SIGNAL FROM NODE [${r},${c}]`;
            
            await wait(); // Visualize Aggregator Catch

            state.aggregator.status.textContent = `SENDING TO OUTPUT...`;
            const line = document.createElement('div');
            line.className = 'out-line buy';
            line.textContent = `[${r},${c}] BUY: +${diff}`;
            els.output.appendChild(line);
            els.output.scrollTop = els.output.scrollHeight;

            await wait();
            state.aggregator.el.classList.remove('active-calc');
            state.aggregator.status.textContent = `WAITING FOR SIGNAL...`;

        } else {
            cell.className = 'grid-cell latched'; // Revert
        }

        cell.classList.remove('active-compute');
    }

    log("SIMULATION COMPLETE.");
    state.isRunning = false;
    els.btnStart.disabled = false;
    state.calcs.forEach(u => u.el.classList.remove('active-calc'));
}

init();
