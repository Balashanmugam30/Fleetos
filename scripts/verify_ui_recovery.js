const http = require('http');

async function fetchUrl(url) {
  return new Promise((resolve) => {
    http.get(url, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body }));
    }).on('error', err => resolve({ status: 'ERROR', error: err.message }));
  });
}

async function run() {
  console.log("=== FLEETOS PHASE 5 UI RECOVERY VERIFICATION ===");

  // 1. Check Backend
  const health = await fetchUrl('http://127.0.0.1:8000/api/v1/health');
  console.log("1. Backend Health:", health.status === 200 ? "OK" : "FAIL");

  // 2. Fetch Dashboard HTML
  const dashHtml = await fetchUrl('http://localhost:3000/dashboard');
  console.log(`2. /dashboard HTML Status: ${dashHtml.status} (${dashHtml.body.length} bytes)`);

  // 3. Verify CSS Asset Delivery
  const cssMatches = [...dashHtml.body.matchAll(/<link[^>]+rel=["']stylesheet["'][^>]+href=["']([^"']+)["']/g)];
  const cssHrefList = cssMatches.map(m => m[1]);

  console.log(`3. Extracted CSS Assets (${cssHrefList.length} found):`);
  let cssOk = true;

  for (const href of cssHrefList) {
    const fullUrl = href.startsWith('http') ? href : `http://localhost:3000${href}`;
    const cssRes = await fetchUrl(fullUrl);
    console.log(`   - CSS URL: ${fullUrl}`);
    console.log(`   - HTTP Status: ${cssRes.status}`);
    console.log(`   - Content-Type: ${cssRes.headers['content-type']}`);
    console.log(`   - Bundle Size: ${cssRes.body.length} bytes`);

    if (cssRes.status !== 200 || cssRes.body.length === 0) {
      cssOk = false;
    }
  }

  if (cssOk) {
    console.log("   [SUCCESS] CSS Asset Delivery Verified 100% OK!");
  } else {
    console.error("   [FAILURE] CSS Asset returned 404 or empty payload!");
  }

  // 4. Verify Web Routes
  const routes = ['/', '/dashboard', '/fleet', '/shipments', '/routes', '/events', '/optimization', '/ai', '/settings'];
  console.log("\n4. Web Route Verification:");
  for (const r of routes) {
    const res = await fetchUrl(`http://localhost:3000${r}`);
    console.log(`   - Route ${r.padEnd(15)} => HTTP ${res.status} (${res.body.length} bytes)`);
  }
}

run();
