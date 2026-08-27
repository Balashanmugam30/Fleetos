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

async function diagnose() {
  console.log("=== FLEETOS CSS & ASSET DELIVERY DIAGNOSTICS ===");

  // 1. Fetch Homepage HTML
  const pageRes = await fetchUrl('http://localhost:3000/dashboard');
  console.log(`1. /dashboard HTML Status: ${pageRes.status} (${pageRes.body.length} bytes)`);

  // Extract CSS stylesheet links from HTML
  const cssMatches = [...pageRes.body.matchAll(/<link[^>]+rel=["']stylesheet["'][^>]+href=["']([^"']+)["']/g)];
  const cssHrefList = cssMatches.map(m => m[1]);

  console.log(`2. Extracted CSS Links (${cssHrefList.length} found):`);
  cssHrefList.forEach(href => console.log(`   - ${href}`));

  if (cssHrefList.length === 0) {
    console.warn("   [WARNING] No <link rel='stylesheet'> tags found in rendered HTML!");
  }

  // Also check for inline styles or Next.js style tags
  const styleTagsCount = (pageRes.body.match(/<style[^>]*>/g) || []).length;
  console.log(`3. Inline <style> Tags Found: ${styleTagsCount}`);

  // Fetch each CSS file link and check for Tailwind classes
  for (const href of cssHrefList) {
    const fullUrl = href.startsWith('http') ? href : `http://localhost:3000${href}`;
    const cssRes = await fetchUrl(fullUrl);
    console.log(`\n4. Testing CSS Asset: ${fullUrl}`);
    console.log(`   - HTTP Status: ${cssRes.status}`);
    console.log(`   - Content-Type: ${cssRes.headers['content-type']}`);
    console.log(`   - Size: ${cssRes.body.length} bytes`);

    // Check key utility classes
    const hasLogisticsCard = cssRes.body.includes('.logistics-card') || cssRes.body.includes('logistics-card');
    const hasBgSlate = cssRes.body.includes('bg-slate-50') || cssRes.body.includes('f8fafc');
    const hasBrandCol = cssRes.body.includes('0369a1') || cssRes.body.includes('brand-600');

    console.log(`   - Contains .logistics-card: ${hasLogisticsCard ? 'YES' : 'NO'}`);
    console.log(`   - Contains Tailwind slate colors: ${hasBgSlate ? 'YES' : 'NO'}`);
    console.log(`   - Contains Tailwind brand colors: ${hasBrandCol ? 'YES' : 'NO'}`);
  }
}

diagnose();
