const CANONICAL_ORIGIN = "https://vitablabla.com";
const SLUG_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/post.html" || url.pathname === "/post") {
      const slug = url.searchParams.get("slug") || "";
      if (SLUG_PATTERN.test(slug)) {
        return Response.redirect(`${CANONICAL_ORIGIN}/a/${slug}/`, 301);
      }
      return Response.redirect(`${CANONICAL_ORIGIN}/blog`, 302);
    }

    return env.ASSETS.fetch(request);
  },
};
