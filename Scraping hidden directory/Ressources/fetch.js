const http = require('http');
const fs = require('fs');

const baseUrl = 'http://localhost:8080/.hidden/';
const outputFile = 'all_readmes.txt';

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function findReadmeFiles(url, visited = new Set()) {
  // Normalize URL to always end with /
  const normalizedUrl = url.endsWith('/') ? url : url + '/';
  
  if (visited.has(normalizedUrl)) return [];
  visited.add(normalizedUrl);

  try {
    const html = await fetchUrl(normalizedUrl);
    const readmeFiles = [];
    
    // Extract links from HTML directory listing
    // Match: <a href="link">text</a>
    const linkRegex = /<a href="([^"]+)">([^<]+)<\/a>/g;
    let match;
    
    while ((match = linkRegex.exec(html)) !== null) {
      const link = match[1];
      const text = match[2].trim();
      
      // Skip parent directory links
      if (link === '../' || link === './') continue;
      
      // Handle README file
      if (link === 'README' || text === 'README') {
        const readmeUrl = normalizedUrl + 'README';
        readmeFiles.push(readmeUrl);
      } 
      // Handle directories (links ending with /)
      else if (link.endsWith('/')) {
        const dirUrl = normalizedUrl + link;
        const subReadmes = await findReadmeFiles(dirUrl, visited);
        readmeFiles.push(...subReadmes);
      }
    }
    
    return readmeFiles;
  } catch (error) {
    console.error(`Error fetching ${normalizedUrl}:`, error.message);
    return [];
  }
}

async function main() {
  console.log('Fetching all README files from .hidden directory...');
  const readmeUrls = await findReadmeFiles(baseUrl);
  console.log(`\nFound ${readmeUrls.length} README files`);
  
  if (readmeUrls.length === 0) {
    console.error('No README files found! Check if the server is running at http://localhost:8080');
    process.exit(1);
  }
  
  const allContent = [];
  let count = 0;
  for (const url of readmeUrls) {
    try {
      const content = await fetchUrl(url);
      allContent.push(`\n=== ${url} ===\n${content}`);
      count++;
      if (count % 10 === 0) {
        process.stdout.write(`\nFetched ${count}/${readmeUrls.length}...`);
      } else {
        process.stdout.write('.');
      }
    } catch (error) {
      console.error(`\nError fetching ${url}:`, error.message);
    }
  }
  
  fs.writeFileSync(outputFile, allContent.join('\n'));
  console.log(`\n\nAll README content written to ${outputFile}`);
  console.log(`Total files: ${readmeUrls.length}, Content length: ${allContent.join('\n').length} characters`);
}

main().catch(console.error);
