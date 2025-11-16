const fs = require('fs');

const inputFile = 'all_readmes.txt';

function findLinesWithFlag(content) {
  const lines = content.split('\n');
  // Search for lines containing "flag" (case insensitive) and also digits (for hash)
  const linesWithFlag = lines.filter(line => {
    const lowerLine = line.toLowerCase();
    return lowerLine.includes('flag') && /\d/.test(line);
  });
  return linesWithFlag;
}

function main() {
  if (!fs.existsSync(inputFile)) {
    console.error(`Error: ${inputFile} not found. Run fetch.js first.`);
    process.exit(1);
  }
  
  const content = fs.readFileSync(inputFile, 'utf-8');
  const linesWithFlag = findLinesWithFlag(content);
  
  console.log(`Found ${linesWithFlag.length} line(s) containing "flag" and digits:\n`);
  linesWithFlag.forEach((line, index) => {
    console.log(`${index + 1}. ${line.trim()}`);
  });
  
  if (linesWithFlag.length === 1) {
    // Extract the flag hash (assuming it's a hex string)
    const flagMatch = linesWithFlag[0].match(/[a-f0-9]{32,}/i);
    if (flagMatch) {
      console.log('\n✓ Flag found:', flagMatch[0]);
    } else {
      console.log('\n✓ Flag line found:', linesWithFlag[0].trim());
    }
  } else if (linesWithFlag.length > 1) {
    console.log('\n⚠ Multiple lines found. Check the output above.');
  } else {
    console.log('\n✗ No lines containing "flag" and digits found.');
    console.log('Trying alternative search (lines with digits only)...');
    const linesWithDigits = content.split('\n').filter(line => /\d/.test(line));
    if (linesWithDigits.length > 0) {
      console.log(`Found ${linesWithDigits.length} line(s) with digits:`);
      linesWithDigits.slice(0, 10).forEach((line, index) => {
        console.log(`${index + 1}. ${line.trim()}`);
      });
      if (linesWithDigits.length > 10) {
        console.log(`... and ${linesWithDigits.length - 10} more`);
      }
    }
  }
}

main();
