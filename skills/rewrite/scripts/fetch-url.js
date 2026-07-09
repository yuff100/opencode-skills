#!/usr/bin/env node
// Fetch and extract clean main content from a URL
// Usage: node scripts/fetch-url.js <url> <output-file>

const https = require('https');
const http = require('http');
const { JSDOM } = require('jsdom');

function fetchUrl(url) {
    return new Promise((resolve, reject) => {
        const client = url.startsWith('https') ? https : http;
        client.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                res.statusCode >= 200 && res.statusCode < 300
                    ? resolve(data)
                    : reject(new Error(`HTTP ${res.statusCode}: ${data}`));
            });
        }).on('error', reject);
    });
}

function extractMainContent(html) {
    const dom = new JSDOM(html);
    const doc = dom.window.document;

    const mainSelectors = [
        'article',
        'main',
        '.post-content',
        '.entry-content',
        '.article-content',
        '#content',
        '.content'
    ];

    let mainElement = null;
    for (const selector of mainSelectors) {
        mainElement = doc.querySelector(selector);
        if (mainElement && mainElement.textContent.trim().length > 500) {
            break;
        }
    }

    if (!mainElement) {
        mainElement = doc.querySelector('body');
    }

    const unwantedSelectors = [
        'nav', 'header', 'footer', 'sidebar', '.sidebar', '#sidebar',
        '.navigation', '.menu', '.advertisement', '.ads', '.social-share',
        '.comments', '#comments', '.footer', 'script', 'style', 'iframe', 'noscript'
    ];

    unwantedSelectors.forEach(selector => {
        mainElement.querySelectorAll(selector).forEach(el => el.remove());
    });

    const title = doc.querySelector('title')?.textContent || '';

    const textContent = mainElement.textContent
        .replace(/\s+/g, ' ')
        .trim()
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .join('\n\n');

    return {
        title,
        content: textContent,
        html: mainElement.innerHTML
    };
}

async function main() {
    const url = process.argv[2];
    const outputFile = process.argv[3];

    if (!url || !outputFile) {
        console.error('Usage: node scripts/fetch-url.js <url> <output-file>');
        console.error('   or: bun scripts/fetch-url.js <url> <output-file>');
        process.exit(1);
    }

    try {
        console.log(`Fetching content from: ${url}`);
        const html = await fetchUrl(url);
        const extracted = extractMainContent(html);

        const output = `# ${extracted.title}\n\n${extracted.content}\n\n---\nSource: ${url}`;
        const fs = require('fs');
        fs.writeFileSync(outputFile, output, 'utf8');

        console.log(`Success! Extracted content written to: ${outputFile}`);
        console.log(`Extracted ~${extracted.content.split(/\s+/).length} words`);
    } catch (err) {
        console.error('Error:', err.message);
        process.exit(1);
    }
}

main();
