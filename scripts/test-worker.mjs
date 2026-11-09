import assert from 'node:assert/strict';
import { test } from 'node:test';
import worker from '../worker.js';

function assets(status = 200) {
  const calls = [];
  return {
    calls,
    ASSETS: {
      async fetch(request) {
        calls.push(request.url);
        return new Response('asset', { status });
      },
    },
  };
}

test('public HTTP and www aliases preserve paths and queries on HTTPS redirects', async () => {
  for (const origin of ['http://vitablabla.com', 'http://www.vitablabla.com', 'https://www.vitablabla.com']) {
    const env = assets();
    const response = await worker.fetch(new Request(`${origin}/a/coffee-candy-guide/?utm_source=test&next=%2Fblog`), env);
    assert.equal(response.status, 308);
    assert.equal(response.headers.get('location'), 'https://vitablabla.com/a/coffee-candy-guide/?utm_source=test&next=%2Fblog');
    assert.equal(env.calls.length, 0);
  }
});

test('canonical requests and local previews pass through without a redirect loop', async () => {
  for (const origin of ['https://vitablabla.com', 'http://localhost:8787', 'http://127.0.0.1:8787', 'https://vitablabla-site.example.workers.dev']) {
    const env = assets();
    const request = new Request(`${origin}/styles.css`);
    const response = await worker.fetch(request, env);
    assert.equal(response.status, 200);
    assert.equal(response.headers.get('location'), null);
    assert.deepEqual(env.calls, [request.url]);
  }
});

test('legacy article aliases redirect directly to their canonical article', async () => {
  for (const path of ['/post', '/post.html']) {
    const response = await worker.fetch(new Request(`http://www.vitablabla.com${path}?slug=coffee-candy-guide`), assets());
    assert.equal(response.status, 301);
    assert.equal(response.headers.get('location'), 'https://vitablabla.com/a/coffee-candy-guide/');
  }
});

test('invalid legacy slugs cannot redirect to a supplied origin or path', async () => {
  for (const slug of ['', '../about', '//example.com', 'https://example.com', 'coffee_candy']) {
    const response = await worker.fetch(new Request(`https://vitablabla.com/post.html?slug=${encodeURIComponent(slug)}`), assets());
    assert.equal(response.status, 302);
    assert.equal(response.headers.get('location'), 'https://vitablabla.com/blog');
  }
});

test('missing assets keep their 404 response', async () => {
  const response = await worker.fetch(new Request('https://vitablabla.com/missing-page'), assets(404));
  assert.equal(response.status, 404);
});
