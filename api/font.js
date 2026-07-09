

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const fontUrl = req.query.url;
  if (!fontUrl) {
    return res.status(400).send('Missing url parameter');
  }

  // Validate that the URL points to arabyfont.com upload path to prevent open redirect vulnerabilities
  if (!fontUrl.startsWith('https://arabyfont.com/wp-content/uploads/')) {
    return res.status(403).send('Forbidden destination');
  }

  try {
    const response = await fetch(fontUrl);
    if (!response.ok) {
      return res.status(response.status).send('Failed to fetch font');
    }

    const buffer = await response.arrayBuffer();

    // Set content type based on extension
    let contentType = 'font/ttf';
    if (fontUrl.endsWith('.otf')) {
      contentType = 'font/otf';
    } else if (fontUrl.endsWith('.woff2')) {
      contentType = 'font/woff2';
    } else if (fontUrl.endsWith('.woff')) {
      contentType = 'font/woff';
    }

    res.setHeader('Content-Type', contentType);
    
    // Set cache control for 1 year (Edge CDN + browser cache)
    res.setHeader('Cache-Control', 'public, max-age=31536000, s-maxage=31536000, immutable');
    
    return res.send(Buffer.from(buffer));
  } catch (error) {
    console.error('Error proxying font:', error);
    return res.status(500).send('Internal Server Error');
  }
};
