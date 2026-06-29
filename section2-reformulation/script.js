/* script.js - Two-Channel Janson Reformulation Toggle & Download Logic */

const statusLabels = {
  'unchanged': 'UNCHANGED',
  'modified': 'MODIFIED',
  'new': 'NEW MACHINERY',
  'tier1': 'TIER 1 — PROVED',
  'tier2': 'TIER 2 — CONJECTURE',
  'gap': 'OPEN GAP'
};

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Toggles
  const toggleAnnotation = document.getElementById('toggle-annotation');
  const toggleAudience = document.getElementById('toggle-audience');

  if (toggleAnnotation) {
    toggleAnnotation.addEventListener('change', e => {
      document.body.classList.toggle('annotated', e.target.checked);
    });
    // Set initial state from checkbox
    document.body.classList.toggle('annotated', toggleAnnotation.checked);
  }

  if (toggleAudience) {
    toggleAudience.addEventListener('change', e => {
      document.body.classList.toggle('advisor-mode', e.target.checked);
    });
    // Set initial state from checkbox
    document.body.classList.toggle('advisor-mode', toggleAudience.checked);
  }

  // 2. Initialize Status Chips in math blocks
  document.querySelectorAll('.math-block').forEach(block => {
    const status = block.getAttribute('data-status');
    if (status && statusLabels[status]) {
      let chip = block.querySelector('.status-chip');
      if (!chip) {
        chip = document.createElement('span');
        chip.className = 'status-chip';
        // Insert as first child so it sits beautifully in DOM flow if absolute positioning is off
        block.insertBefore(chip, block.firstChild);
      }
      chip.innerText = statusLabels[status];
    }
  });

  // 3. Setup Zip Download Button
  const btnDownload = document.getElementById('btn-download');
  if (btnDownload) {
    btnDownload.addEventListener('click', downloadZip);
  }
});

// Download Client-side ZIP containing index.html, style.css, script.js
async function downloadZip() {
  const btn = document.getElementById('btn-download');
  const originalText = btn.innerHTML;
  
  try {
    btn.disabled = true;
    btn.innerHTML = `
      <svg class="animate-spin" viewBox="0 0 24 24" fill="none" style="animation: spin 1s linear infinite;">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" style="opacity: 0.25;"></circle>
        <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Zipping...
    `;

    // Ensure JSZip is loaded (it is loaded via CDN in index.html)
    if (typeof JSZip === 'undefined') {
      throw new Error("JSZip library is not loaded. Please wait and try again.");
    }

    const zip = new JSZip();
    const folder = zip.folder("section2-reformulation");

    // Fetch local files from the server
    const [htmlText, cssText, jsText] = await Promise.all([
      fetch('./index.html').then(res => {
        if (!res.ok) throw new Error("Could not fetch index.html");
        return res.text();
      }),
      fetch('./style.css').then(res => {
        if (!res.ok) throw new Error("Could not fetch style.css");
        return res.text();
      }),
      fetch('./script.js').then(res => {
        if (!res.ok) throw new Error("Could not fetch script.js");
        return res.text();
      })
    ]);

    // Add files to folder
    folder.file("index.html", htmlText);
    folder.file("style.css", cssText);
    folder.file("script.js", jsText);

    // Generate zip blob
    const content = await zip.generateAsync({type: "blob"});
    
    // Trigger download
    const url = URL.createObjectURL(content);
    const a = document.createElement('a');
    a.href = url;
    a.download = "section2-reformulation.zip";
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);

  } catch (error) {
    console.error("ZIP packaging failed:", error);
    alert("An error occurred while packaging the ZIP: " + error.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalText;
  }
}

// Simple keyframe animation style injection for spinner
const style = document.createElement('style');
style.innerHTML = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  .animate-spin {
    animation: spin 1s linear infinite;
  }
`;
document.head.appendChild(style);
