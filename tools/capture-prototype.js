const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const allScenes = [
  'home-first', 'welcome', 'progress-1', 'progress-2', 'progress-3', 'progress-4',
  'details', 'transfer', 'review', 'success', 'transactions', 'home-active', 'home-post-transfer',
  'returning-1', 'returning-2', 'returning-3', 'returning-4', 'halted',
  'nudge-after'
];
const requested = process.argv.slice(2);
const scenes = requested.length ? requested : allScenes;
const frames = path.join(__dirname, 'frames');
fs.mkdirSync(frames, { recursive: true });

const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
  for (let i = 0; i < scenes.length; i++) {
    const scene = scenes[i];
    const output = path.join(frames, `${scene}.png`);
    if (fs.existsSync(output)) fs.unlinkSync(output);
    const profile = path.join('/private/tmp', `ap-chrome-${Date.now()}-${i}`);
    const child = spawn(chrome, [
      '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
      `--user-data-dir=${profile}`, '--window-size=1280,800',
      `--screenshot=${output}`,
      `http://127.0.0.1:8765/anytimepay-q2-prototype.html?scene=${scene}`
    ], { stdio: 'ignore' });
    let attempts = 0;
    while (!fs.existsSync(output) && attempts < 80) { await wait(100); attempts++; }
    if (!child.killed) child.kill('SIGKILL');
    if (!fs.existsSync(output)) throw new Error(`Failed to render ${scene}`);
  }
  console.log(`Rendered ${scenes.length} prototype scenes.`);
})();
